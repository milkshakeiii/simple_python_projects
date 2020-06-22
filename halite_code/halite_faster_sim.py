import kaggle_environments.envs.halite.helpers as halite
from kaggle_environments.envs.halite.helpers import *

import random, time, cProfile


########################
# Simulation functions #
########################


def turn(board) -> 'Board':

    configuration = board.configuration
    convert_cost = configuration.convert_cost
    spawn_cost = configuration.spawn_cost
    uid_counter = 0

    # This is a consistent way to generate unique strings to form ship and shipyard ids
    def create_uid():
        nonlocal uid_counter
        uid_counter += 1
        return f"{board.step + 1}-{uid_counter}"

    # Process actions and store the results in the ships and shipyards lists for collision checking
    for player in board.players.values():
        leftover_convert_halite = 0

        for shipyard in player.shipyards:
            if shipyard.next_action == ShipyardAction.SPAWN and player.halite >= spawn_cost:
                # Handle SPAWN actions
                player._halite -= spawn_cost
                board._add_ship(Ship(ShipId(create_uid()), shipyard.position, 0, player.id, board))
            # Clear the shipyard's action so it doesn't repeat the same action automatically
            shipyard.next_action = None

        for ship in player.ships:
            if ship.next_action == ShipAction.CONVERT:
                # Can't convert on an existing shipyard but you can use halite in a ship to fund conversion
                if ship.cell.shipyard_id is None and (ship.halite + player.halite) >= convert_cost:
                    # Handle CONVERT actions
                    delta_halite = ship.halite - convert_cost
                    # Excess halite leftover from conversion is added to the player's total only after all conversions have completed
                    # This is to prevent the edge case of chaining halite from one convert to fund other converts
                    leftover_convert_halite += max(delta_halite, 0)
                    player._halite += min(delta_halite, 0)
                    board._add_shipyard(Shipyard(ShipyardId(create_uid()), ship.position, player.id, board))
                    board._delete_ship(ship)
            elif ship.next_action is not None:
                # If the action is not None and is not CONVERT it must be NORTH, SOUTH, EAST, or WEST
                ship.cell._ship_id = None
                ship._position = ship.position.translate(ship.next_action.to_point(), configuration.size)
                ship._halite *= (1 - board.configuration.move_cost)
                # We don't set the new cell's ship_id here as it would be overwritten by another ship in the case of collision.
                # Later we'll iterate through all ships and re-set the cell._ship_id as appropriate.

        player._halite += leftover_convert_halite
        # Lets just check and make sure.
        assert player.halite >= 0

    def resolve_collision(ships: List[Ship]) -> Tuple[Optional[Ship], List[Ship]]:
        """
        Accepts the list of ships at a particular position (must not be empty).
        Returns the ship with the least halite or None in the case of a tie along with all other ships.
        """
        if len(ships) == 1:
            return ships[0], []
        ships_by_halite = group_by(ships, lambda ship: ship.halite)
        smallest_halite = min(ships_by_halite.keys())
        smallest_ships = ships_by_halite[smallest_halite]
        if len(smallest_ships) == 1:
            # There was a winner, return it
            winner = smallest_ships[0]
            return winner, [ship for ship in ships if ship != winner]
        # There was a tie for least halite, all are deleted
        return None, ships

    # Check for ship to ship collisions
    ship_collision_groups = group_by(board.ships.values(), lambda ship: ship.position)
    for position, collided_ships in ship_collision_groups.items():
        winner, deleted = resolve_collision(collided_ships)
        if winner is not None:
            winner.cell._ship_id = winner.id
        for ship in deleted:
            board._delete_ship(ship)
            if winner is not None:
                # Winner takes deleted ships' halite
                winner._halite += ship.halite

    # Check for ship to shipyard collisions
    for shipyard in list(board.shipyards.values()):
        ship = shipyard.cell.ship
        if ship is not None and ship.player_id != shipyard.player_id:
            # Ship to shipyard collision
            board._delete_shipyard(shipyard)
            board._delete_ship(ship)

    # Deposit halite from ships into shipyards
    for shipyard in list(board.shipyards.values()):
        ship = shipyard.cell.ship
        if ship is not None and ship.player_id == shipyard.player_id:
            shipyard.player._halite += ship.halite
            ship._halite = 0

    # Collect halite from cells into ships
    for ship in board.ships.values():
        cell = ship.cell
        delta_halite = int(cell.halite * configuration.collect_rate)
        if ship.next_action not in ShipAction.moves() and cell.shipyard_id is None and delta_halite > 0:
            ship._halite += delta_halite
            cell._halite -= delta_halite
        # Clear the ship's action so it doesn't repeat the same action automatically
        ship.next_action = None

    # Regenerate halite in cells
    for cell in board.cells.values():
        if cell.ship_id is None:
            next_halite = round(cell.halite * (1 + configuration.regen_rate), 3)
            cell._halite = min(next_halite, configuration.max_cell_halite)
            # Lets just check and make sure.
        assert cell.halite >= 0

    board._step += 1

    return board



#######################
# strategic functions #
#######################

def evaluate(board):
    evaluation = 0
    evaluation += len(board.current_player.ships) * 1000
    evaluation += board.current_player.halite
    for ship in board.current_player.ships:
        evaluation += ship.halite * 0.1
    return evaluation

def setRandomMove(board):
    ship_actions = [action for action in halite.ShipAction]
    shipyard_actions = [action for action in halite.ShipyardAction]
    for ship in board.current_player.ships:
        if (board.step == 0):
            ship.next_action = halite.ShipAction.CONVERT
        else:
            ship.next_action = random.choice(ship_actions + [None])
    for shipyard in board.current_player.shipyards:
        if (board.step > 300):
            shipyard.next_action = None
        else:
            shipyard.next_action = random.choice(shipyard_actions + [None])

#returns best moves after a random sampling
def randomSearch(depth, width, board):
    return doRandomSearch(depth, width, board)[1]

#returns (evaluation, best_move)
def doRandomSearch(depth, width, board):
    if depth == 0:
        return (evaluate(board), {})

    random_moves = []
    start_time = time.time()
    loops = 0
    while (time.time() - start_time < 5):
        loops += 1
        setRandomMove(board)
        action = board.current_player.next_actions.copy()
        turn(board)
        random_moves.append((doRandomSearch(depth-1, width, board)[0], action))

    best_move = max(random_moves, key=lambda move: move[0])
    print(loops)
    return best_move
        




#############
# The agent #
#############

def agent(obs, config):
    board = halite.Board(obs, config)

    cProfile.runctx('randomSearch(1, 60, board)', globals(), locals(), filename=None)

    #if(board.step < 10 or board.step % 50 == 0):
    print("turn " + str(board.step))

    del_us = []
    for key in actions.keys():
        if actions[key] == None:
            del_us.append(key)
    for key in del_us:
        del actions[key]

    return actions
