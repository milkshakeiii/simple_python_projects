import kaggle_environments.envs.halite.helpers as halite

import queue, random

####################
# Helper functions #
####################

#returns None if no directin gets closer to toPos
def get_dir_to(fromPos, toPos, board, forbidden_positions):
    if (manhattan(fromPos, toPos) == 0):
        return None
    size = board.configuration.size
    y_sign = toPos.y > fromPos.y
    x_sign = toPos.x > fromPos.x
    y_wrap = abs(fromPos.y - toPos.y) < size/2
    y_match = fromPos.y == toPos.y
    x_wrap = abs(fromPos.x - toPos.x) < size/2
    x_match = fromPos.x == toPos.x
    north_occupied = (fromPos + (0, 1)) in forbidden_positions
    south_occupied = (fromPos + (0, -1)) in forbidden_positions
    west_occupied = (fromPos + (-1, 0)) in forbidden_positions
    east_occupied = (fromPos + (1, 0)) in forbidden_positions
    if (not y_match) and y_wrap == (not y_sign) and (not south_occupied):
        return halite.ShipAction.SOUTH
    elif (not y_match) and (not north_occupied):
        return halite.ShipAction.NORTH
    elif (not x_match) and x_wrap == (not x_sign) and (not west_occupied):
        return halite.ShipAction.WEST
    elif (not x_match) and (not east_occupied):
        return halite.ShipAction.EAST
    else:
        return None

def get_cell_in_dir(start, direction, board):
    if direction == halite.ShipAction.WEST:
        return board[start].west
    if direction == halite.ShipAction.NORTH:
        return board[start].north
    if direction == halite.ShipAction.EAST:
        return board[start].east
    if direction == halite.ShipAction.SOUTH:
        return board[start].south
    if direction == None:
        return board[start]

def find_halite(board, ship, taken_halite_positions):
    frontier = queue.Queue()
    frontier.put(ship.position)
    explored = {}

    for i in range(500):
        search_spot = frontier.get()
        for next_spot in [board[search_spot].west.position,
                          board[search_spot].north.position,
                          board[search_spot].east.position,
                          board[search_spot].south.position]:
            if (next_spot not in explored):
                frontier.put(next_spot)
                explored[next_spot] = True

        if board[search_spot].halite >= 100 and search_spot not in taken_halite_positions:
            taken_halite_positions[search_spot] = True
            return search_spot

    print ("no halite found")
    return None

def find_shipyard(board, ship, shipyard_positions):
    if len(shipyard_positions) == 0:
        print("no shipyards")
        return None

    nearest_shipyard = None
    nearest_distance = 99999

    for shipyard in shipyard_positions.keys():
        distance = manhattan(ship.position, shipyard)
        if distance < nearest_distance:
            nearest_shipyard = shipyard
            nearest_distance = distance

    return nearest_shipyard

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)
    
def forbidable_move(ship, direction, forbidden_positions, board):
    target_pos = get_cell_in_dir(ship.position, direction, board).position
    #print("fm-")
    #print(target_pos)
    #print(forbidden_positions)
    #print("---")
    if (target_pos not in forbidden_positions):
        forbidden_positions[target_pos] = True
        if (direction != None):
            ship.next_action = direction
    elif (ship.position not in forbidden_positions):
        forbidden_positions[ship.position] = True
    else:
        #print("last minute step off")
        ship.next_action = step_off_direction(ship, board, forbidden_positions)
        #print(ship.next_action)
        cell = get_cell_in_dir(ship.position, ship.next_action, board)
        forbidden_positions[cell.position] = True

def step_off_direction(ship, board, forbidden_positions):
    cells = [board[ship.position].west,
             board[ship.position].north,
             board[ship.position].east,
             board[ship.position].south]
    random.shuffle(cells)
    stepoff_dir = get_dir_to(ship.position,
                             cells[0].position,
                             board,
                             forbidden_positions)
    if stepoff_dir == None:
        stepoff_dir = get_dir_to(ship.position,
                                 cells[1].position,
                                 board,
                                 forbidden_positions)
    if stepoff_dir == None:
        stepoff_dir = get_dir_to(ship.position,
                                 cells[2].position,
                                 board,
                                 forbidden_positions)
    if stepoff_dir == None:
        stepoff_dir = get_dir_to(ship.position,
                                 cells[3].position,
                                 board,
                                 forbidden_positions)
    #print(stepoff_dir)
    return stepoff_dir

#############
# The agent #
#############

def stranger_danger(board, ship, forbidden_positions):
    occupied_directions = []
    must_run = False
    direction_list = [(board[ship.position].west, halite.ShipAction.WEST),
                      (board[ship.position].north, halite.ShipAction.NORTH),
                      (board[ship.position].east, halite.ShipAction.EAST),
                      (board[ship.position].south, halite.ShipAction.SOUTH)]
    random.shuffle(direction_list)
    for directions in direction_list:
        direction = directions[0]
        chase_command = directions[1]
        occupant = direction.ship
        enemy_here = occupant != None and occupant.player_id != board.current_player.id
        ally_here = occupant != None and occupant.player_id == board.current_player.id
        if enemy_here and ship.halite < 500 and ship.halite < occupant.halite:
            forbidable_move(ship, chase_command, forbidden_positions, board)
            return True
        occupied_directions.append(enemy_here or ally_here)
        must_run = must_run or (enemy_here and occupant.halite < ship.halite)
        if (enemy_here and occupant.halite < ship.halite) and ship.halite > 1000:
            ship.next_action = halite.ShipAction.CONVERT
            return True
    if must_run:
        for i in range(4):
            if not occupied_directions[i]:
                forbidable_move(ship, direction_list[i][1], forbidden_positions, board)
                #print(occupied_directions)
                return True
    return False

def collect(board, ship, forbidden_positions, taken_halite_positions):
    target_position = find_halite(board, ship, taken_halite_positions)
    if target_position is None:
        forbidable_move(ship, None, forbidden_positions, board)
        return True
    dir_to = get_dir_to(ship.position, target_position, board, forbidden_positions)
    target_cell = get_cell_in_dir(ship.position, dir_to, board)
    rich = target_cell.halite >= 400
    on_top = manhattan(ship.position, target_position) == 0
    close = manhattan(ship.position, target_position) == 1
    if on_top and rich:
        forbidable_move(ship, None, forbidden_positions, board)
        #print("harvest " + str(ship.position))
        return True
    elif on_top:
        waiting_dir = step_off_direction(ship, board, forbidden_positions)
        forbidable_move(ship, waiting_dir, forbidden_positions, board)
        #print("step off" + str(ship.position) + " " + str(waiting_dir))
        return True
    elif (close and rich) or (not close):
        #print("go to " + str(target_position))
        forbidable_move(ship, dir_to, forbidden_positions, board)
        return True
    elif (close and not rich):
        forbidable_move(ship, None, forbidden_positions, board)
        #print("grow " + str(target_cell.halite) + " " + str(target_position))
        return True
    return False

@halite.board_agent
def agent(board):
    
    forbidden_positions = {}
    shipyard_positions = {}
    taken_halite_positions = {}
                
    #spawn
    for shipyard in board.current_player.shipyards:
        shipyard_positions[shipyard.position] = True
        free = (board[shipyard.position].north.ship_id == None) or (board[shipyard.position].south.ship_id == None) or (board[shipyard.position].west.ship_id == None) or (board[shipyard.position].east.ship_id == None)
        have_money = board.current_player.halite >= 500
        not_late = board.step < 300
        if free and have_money and not_late:
            shipyard.next_action = halite.ShipyardAction.SPAWN
            forbidden_positions[shipyard.position] = True
            #print("spawn")

    backup_built = False
    for ship in board.current_player.ships:
        #print(ship.id)
        #convert on the furst turn
        if (board.step == 0):
            ship.next_action = halite.ShipAction.CONVERT
            continue

        if (len(board.current_player.shipyards) == 0) and not backup_built and (ship.halite > 500 or board.current_player.halite > 500):
            backup_built = True
            ship.next_action = halite.ShipAction.CONVERT
            continue

        #convert on last turn if cargo big enough
        if (board.step == 398 and ship.halite > 500):
            ship.next_action = halite.ShipAction.CONVERT
            continue

        #dont block shipyards
        if (ship.position in shipyard_positions):
            stepoff_dir = step_off_direction(ship, board, forbidden_positions)
            #print("don't block shipyards" + str(stepoff_dir))
            #print(forbidden_positions)
            forbidable_move(ship, stepoff_dir, forbidden_positions, board)
            continue
        
        #stranger danger
        if (stranger_danger(board, ship, forbidden_positions)):
            continue

        #deposit
        if (ship.halite > 500 or (board.step > 380 and ship.halite != 0)):
            shipyard_position = find_shipyard(board, ship, shipyard_positions)
            if shipyard_position is None:
                forbidable_move(ship, None, forbidden_positions, board)
                continue
            deposit_dir = get_dir_to(ship.position, shipyard_position, board, forbidden_positions)
            forbidable_move(ship, deposit_dir, forbidden_positions, board)
            continue

        #collect
        if (collect(board, ship, forbidden_positions, taken_halite_positions)):
            #print("collect")
            continue
            
    #if(board.step < 10 or board.step % 50 == 0):
    #print("step " + str(board.step))
                
    return board
