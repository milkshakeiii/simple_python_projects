import kaggle_environments.envs.halite.helpers as halite
from kaggle_environments.envs.halite.helpers import *

import random, time, cProfile, copy
import numpy as np


########################
# Simulation functions #
########################

#ship dict is (x, y) position: list of (halite, owner) pairs (list len is 1 between turns)
#shipyard dict is (x, y) position: owner
def battle_board(obs, config, start_pos, width, height):
    board = Board(obs, config)
    ship_box = {}
    shipyard_box = {}
    for i in range(start_pos[0], width):
        for j in range(start_pos[1], height):
            ship = board[i, j].ship
            if ship != None:
                ship_box[i, j] = [(ship.halite, ship.player.id)]
            shipyard = board[i, j].shipyard
            if shipyard != None:
                shipyard_box[i, j] = shipyard.player.id

    return (ship_box, shipyard_box)    

#we want this to be performant
def turn(dict_boards, moves):
    ship_box, shipyard_box = dict_boards
    ship_actions, shipyard_actions = moves
    new_ship_box = {}
    new_shipyard_box = {}

    #move ships into lists and convert
    for ship_position, ship_action in ship_actions.items():
        if ship_action == "CONVERT":
            if ship_position not in shipyard_box:
                new_shipyard_box[ship_position] = ship_box[ship_position][0][1]
                continue
            else:
                move_direction = (0, 0)
        elif ship_action == "STAY":
            move_direction = (0, 0)
        elif ship_action == "WEST":
            move_direction = (-1, 0)
        elif ship_action == "EAST":
            move_direction = (1, 0)
        elif ship_action == "NORTH":
            move_direction = (0, 1)
        elif ship_action == "SOUTH":
            move_direction = (0, -1)
        else:
            raise Exception("Unrecognized ship command: " + ship_action)
        target_position = (ship_position[0] + move_direction[0],
                           ship_position[1] + move_direction[1])
        moving_ship = ship_box[ship_position][0]
        new_ship_box[target_position] = new_ship_box.get(target_position, []) + [moving_ship]

    #spawn ships into lists and copy shipyards
    for shipyard_position, shipyard_action in shipyard_actions.items():
        new_shipyard_box[shipyard_position] = shipyard_box[shipyard_position]
        if shipyard_action == "SPAWN":
            new_ship = (0, shipyard_box[shipyard_position])
            new_ship_box[shipyard_position] = new_ship_box.get(shipyard_position, []) + [new_ship]
        elif shipyard_action != "SLEEP":
            raise Exception("Unrecognized ship command: " + ship_action)

    #collide ships
    explode_us = []
    for ship_position, ship_list in new_ship_box.items():
        min_halite, min_owner = min(ship_list)
        halites = [ship[0] for ship in ship_list]
        if halites.count(min_halite) > 1:
            explode_us.append(ship_position)
        else:
            new_ship_box[ship_position] = (sum(halites), min_owner)
    for explode_me in explode_us:
        del new_ship_box[explode_me]

    #ship-shipyard interaction
    explode_us = []
    for shipyard_position, shipyard_owner in new_shipyard_box.items():
        if shipyard_position in new_ship_box:
            ship_halite, ship_owner = new_ship_box[shipyard_position]
            if ship_owner == shipyard_owner:
                new_ship_box[shipyard_position] = (0, ship_owner) #HALITE COLLECTED
            else:
                explode_us.append(shipyard_position)
    for explode_me in explode_us:
        del new_shipyard_box[explode_me]

    return new_ship_box, new_shipyard_box

    
        

    
        
        
        


def tuple_location(location):
    return location%21, 20-location//21
    





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

#move dicts are (x, y) position: "NORTH", "SOUTH", "EAST", "WEST", "STAY"
#or "SPAWN", "SLEEP"
def randomMove(obs, config, player_id):
    ship_actions = [action.name for action in halite.ShipAction]
    shipyard_actions = [action.name for action in halite.ShipyardAction]
    random_ship_actions = {}
    random_shipyard_actions = {}
    for ship in obs['players'][player_id][2].values():
        ship_location, ship_halite = ship
        ship_location = tuple_location(ship_location)
        if (obs['step'] == 0):
            random_ship_actions[ship_location] = halite.ShipAction.CONVERT.name
        else:
            random_action = random.choice(ship_actions + ["STAY"])
            if random_action is not None:
                random_ship_actions[ship_location] = random_action
    for shipyard_position in obs['players'][player_id][1].values():
        shipyard_position = tuple_location(shipyard_position)
        if (obs['step'] < 300):
            random_action = random.choice(shipyard_actions + ["SLEEP"])
            random_shipyard_actions[shipyard_position] = random_action
    return (random_ship_actions, random_shipyard_actions)

#returns best moves after a random sampling
def randomSearch(depth, width, obs, config, board_dicts):
    my_moves = doRandomSearch(depth, width, obs, config, board_dicts)[1]
    return my_moves

#returns (evaluation, best_move)
def doRandomSearch(depth, width, obs, config, board_dicts):
    if depth == 0:
        return (evaluate(obs, config), ({}, {}))

    random_moves = []
    start_time = time.time()
    loops = 0
    while (time.time() - start_time < 5):
        loops += 1
        my_moves = randomMove(obs, config, obs['player'])
        new_board_dicts = turn(board_dicts, my_moves)
        random_moves.append((doRandomSearch(depth-1,
                                            width,
                                            obs,
                                            config,
                                            new_board_dicts)[0], my_moves))

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

    halite_dict = restructure_halite(obs['halite'], config['size'])

    board_dicts = battle_board(obs, config, (0, 0), 21, 21)
    actions = randomSearch(1, 60, obs, config, board_dicts)
    #cProfile.runctx('randomSearch(1, 60, obs, config)', globals(), locals(), filename=None)

    print(actions)

    #if(board.step < 10 or board.step % 50 == 0):
    print("turn " + str(board.step))

    return_actions = {}
    for position, action in actions[0].items(): #ships
        if action != "STAY":
            return_actions[board[position].ship.id] = action
    for position, action in actions[1].items(): #shipyards
        if action != "SLEEP":
            return_actions[board[position].shipyard.id] = action

    print (return_actions)
    return return_actions
