import kaggle_environments.envs.halite.helpers as halite

import random, time


####################
# Helper functions #
####################

# Helper function we'll use for getting adjacent position with the most halite
def argmax(arr, key=None):
    return arr.index(max(arr, key=key)) if key else arr.index(max(arr))

# Converts position from 1D to 2D representation
def get_col_row(size, pos):
    return (pos % size, pos // size)

# Returns the position in some direction relative to the current position (pos) 
def get_to_pos(size, pos, direction):
    col, row = get_col_row(size, pos)
    if direction == "NORTH":
        return pos - size if pos >= size else size ** 2 - size + col
    elif direction == "SOUTH":
        return col if pos + size >= size ** 2 else pos + size
    elif direction == "EAST":
        return pos + 1 if col < size - 1 else row * size
    elif direction == "WEST":
        return pos - 1 if col > 0 else (row + 1) * size - 1

# Get positions in all directions relative to the current position (pos)
# Especially useful for figuring out how much halite is around you
def getAdjacent(pos, size):
    return [
        get_to_pos(size, pos, "NORTH"),
        get_to_pos(size, pos, "SOUTH"),
        get_to_pos(size, pos, "EAST"),
        get_to_pos(size, pos, "WEST"),
    ]

# Returns best direction to move from one position (fromPos) to another (toPos)
# Example: If I'm at pos 0 and want to get to pos 55, which direction should I choose?
def getDirTo(fromPos, toPos, size):
    fromY, fromX = divmod(fromPos, size)
    toY,   toX   = divmod(toPos,   size)
    if fromY < toY: return "SOUTH"
    if fromY > toY: return "NORTH"
    if fromX < toX: return "EAST"
    if fromX > toX: return "WEST"



#######################
# strategic functions #
#######################

def evaluate(board):
    evaluation = 0
    evaluation += len(board.current_player.ships) * 1000
    evaluation += board.current_player.halite
    for ship in board.current_player.ships:
        evaluation += ship.halite * 0.02
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
    while (time.time() - start_time < 0.1):
        loops += 1
        setRandomMove(board)
        action = board.current_player.next_actions.copy()
        advanced_board = board.next()
        random_moves.append((doRandomSearch(depth-1, width, advanced_board)[0], action))

    best_move = max(random_moves, key=lambda move: move[0])
    #print(loops)
    return best_move
        




#############
# The agent #
#############

def agent(obs, config):
    board = halite.Board(obs, config)

    actions = randomSearch(1, 60, board)

    #if(board.step < 10 or board.step % 50 == 0):
        #print("turn " + str(board.step))

    del_us = []
    for key in actions.keys():
        if actions[key] == None:
            del_us.append(key)
    for key in del_us:
        del actions[key]

    return actions
