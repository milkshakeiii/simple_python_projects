import kaggle_environments.envs.halite.helpers as halite
from kaggle_environments.envs.halite.helpers import *

import random, time, cProfile, copy


########################
# Simulation functions #
########################


def turn(obs, configuration, ships_by_position, shipyards_by_position, moves):
    ship_moves, shipyard_moves = moves

    convert_cost = configuration.convert_cost
    spawn_cost = configuration.spawn_cost
    uid_counter = 0

    # This is a consistent way to generate unique strings to form ship and shipyard ids
    def create_uid():
        nonlocal uid_counter
        uid_counter += 1
        return f"{self.step + 1}-{uid_counter}"

    # Process actions and store the results in the ships and shipyards lists for collision checking
    for player in obs['players']:
        player_halite, player_shipyards, player_ships = player
        leftover_convert_halite = 0

        for shipyard, position in player_shipyards.items():
            if shipyard_moves[shipyard] == "SPAWN" and player_halite >= spawn_cost:
                # Handle SPAWN actions
                player_halite -= spawn_cost
                player_ships[create_uid()] = [position, 0]

        for ship, value in player_ships:
            position, ship_halite = value
            if ship_moves[ship] == "CONVERT":
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

def evaluate(obs, config):
    halite_store, shipyards, ships = obs['players'][obs['player']]
    evaluation = 0
    evaluation += len(ships) * 1000
    evaluation += halite_store
    for ship in ships.values():
        position_num, halite_cargo = ship
        evaluation += halite_cargo * 0.1
    return evaluation

def randomMove(obs, config, player_id):
    ship_actions = [action.name for action in halite.ShipAction]
    shipyard_actions = [action.name for action in halite.ShipyardAction]
    random_ship_actions = {}
    random_shipyard_actions = {}
    for ship_id in obs['players'][player_id][2].keys():
        if (obs['step'] == 0):
            random_ship_actions[ship_id] = halite.ShipAction.CONVERT.name
        else:
            random_action = random.choice(ship_actions + [None])
            if random_action is not None:
                random_ship_actions[ship_id] = random_action
    for shipyard_id in obs['players'][player_id][1].keys():
        if (obs['step'] < 300):
            random_action = random.choice(shipyard_actions + [None])
            if random_action is not None:
                random_shipyard_actions[shipyard_id] = random_action
    return (random_ship_actions, random_shipyard_actions)

#returns best moves after a random sampling
def randomSearch(depth, width, obs, config):
    my_moves = doRandomSearch(depth, width, obs, config)[1]
    my_moves[0].update(my_moves[1])
    return my_moves[0]

#returns (evaluation, best_move)
def doRandomSearch(depth, width, obs, config, ships_by_position, shipyards_by_position):
    if depth == 0:
        return (evaluate(obs, config), {})

    random_moves = []
    start_time = time.time()
    loops = 0
    while (time.time() - start_time < 5):
        loops += 1
        my_moves = randomMove(obs, config, obs['player'])
        turn(obs, config, my_moves)
        random_moves.append((doRandomSearch(depth-1, width, obs, config)[0], my_moves))

    best_move = max(random_moves, key=lambda move: move[0])
    print(loops)
    return best_move
        

def restructure_halite(halite_list, size):
    halite_dict = {}
    for i in range(size):
        for j in range(size):
            halite_amount = halite_list[j * size + i]
            if halite_amount != 0:
                halite_dict[(i, j)] = halite_amount
    return halite_dict


#############
# The agent #
#############

def agent(obs, config):
    board = halite.Board(obs, config)
    obs = dict(obs)
    config = dict(config)
    print(obs['players'][obs['player']])

    obs['halite'] = restructure_halite(obs['halite'], config['size'])

    actions = randomSearch(1, 60, obs, config)
    #cProfile.runctx('randomSearch(1, 60, obs, config)', globals(), locals(), filename=None)

    #if(board.step < 10 or board.step % 50 == 0):
    print("turn " + str(board.step))
    print(actions)

    return actions
