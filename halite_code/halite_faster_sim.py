import kaggle_environments.envs.halite.helpers as halite
from kaggle_environments.envs.halite.helpers import *

import random, time, cProfile


########################
# Simulation functions #
########################


def turn(obs, config, moves):
    ship_moves, shipyard_moves = moves
    print(moves)




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
    ship_actions = [action for action in halite.ShipAction]
    shipyard_actions = [action for action in halite.ShipyardAction]
    random_ship_actions = {}
    random_shipyard_actions = {}
    for ship_id in obs['players'][player_id][2].keys():
        if (obs['step'] == 0):
            random_ship_actions[ship_id] = halite.ShipAction.CONVERT
        else:
            random_action = random.choice(ship_actions + [None])
            if random_action is not None:
                random_ship_actions[ship_id] = random_action
    for shipyard_id in obs['players'][player_id][1].keys():
        if (obs['step'] > 300):
            random_action = random.choice(shipyard_actions + [None])
            if random_action is not None:
                random_shipyard_actions[shipyard_id] = random_action
    return (random_ship_actions, random_shipyard_actions)

#returns best moves after a random sampling
def randomSearch(depth, width, obs, config):
    my_moves = doRandomSearch(depth, width, obs, config)[1]
    return my_moves[0].update(my_moves[1])

#returns (evaluation, best_move)
def doRandomSearch(depth, width, obs, config):
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

    return actions
