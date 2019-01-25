# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import copy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def general_pacman_search(strategy, maze):
    nodes_explored = 0
    start = maze.getStart()
    frontier = [ ([(start[0], start[1])], set()) ]
    objectives = maze.getObjectives()
    forbidden_states = []
    
    while len(frontier) > 0:
        exploring_node = frontier.pop(0)
        nodes_explored += 1
        
        if len(exploring_node[1]) == len(objectives):
            return_path = [(step[0], step[1]) for step in exploring_node[0]]
            return return_path, nodes_explored
        
        new_neighbors = maze.getNeighbors(exploring_node[0][-1][0], exploring_node[0][-1][1])
        neighbor_states = []
        for neighbor in new_neighbors:
            captured_objectives = copy.deepcopy(exploring_node[1])
            if neighbor in objectives:
                captured_objectives.add(neighbor)
            neighbor_states.append((neighbor, captured_objectives))
                
        
        frontier, forbidden_states = strategy(neighbor_states, exploring_node, frontier, maze, objectives, forbidden_states)

    raise Exception("No route found")



def bfs_strategy(neighbor_states, exploring_node, frontier, maze, objectives, forbidden_states):
    allowable_neighbor_states = [neighbor for neighbor in neighbor_states if neighbor not in forbidden_states]
    forbidden_states = forbidden_states + allowable_neighbor_states
    allowable_neighbor_nodes = [(exploring_node[0] + [state[0]], state[1]) for state in allowable_neighbor_states]
    frontier = frontier + allowable_neighbor_nodes
    return frontier, forbidden_states


def dfs_strategy(allowable_neighbor_states, exploring_node, frontier, maze, objectives, forbidden_states):
    forbidden_states = forbidden_states + allowable_neighbor_states
    allowable_neighbor_nodes = [(exploring_node[0] + [state[0]], state[1]) for state in allowable_neighbor_states]
    frontier = allowable_neighbor_nodes + frontier
    return frontier, forbidden_states


def greedy_strategy(allowable_neighbor_states, exploring_node, frontier, maze, objectives, forbidden_states):
    allowable_neighbor_nodes = [(exploring_node[0] + [state[0]], state[1]) for state in allowable_neighbor_states]
    frontier = allowable_neighbor_nodes + frontier
    frontier = sorted(frontier, key = lambda node:  heuristic(node, maze, objectives))
    return frontier, forbidden_states


def astar_strategy(neighbor_states, exploring_node, frontier, maze, objectives, forbidden_states):
    forbidden_states = forbidden_states + allowable_neighbor_states
    allowable_neighbor_nodes = [(exploring_node[0] + [state[0]], state[1]) for state in allowable_neighbor_states]
    frontier = allowable_neighbor_nodes + frontier
    frontier = sorted(frontier, key = lambda node: len(node[0]) + heuristic(node, maze, objectives))
    return frontier, forbidden_states



def dot_heuristic(node, maze, objectives):
    return len(objectives) - len(node[1])

def heuristic(node, maze, objectives):
    manhattan_sum = 0
    current_square = node[0][-1]
    remaining_objectives = [objective for objective in objectives if objective not in node[1]]
    for objective in remaining_objectives:
        manhattan_sum += abs(current_square[0] - objective[0])
        manhattan_sum += abs(current_square[1] - objective[1])
    return manhattan_sum



def bfs(maze):
    
    # return path, num_states_explored
    return general_pacman_search(bfs_strategy, maze)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(dfs_strategy, maze)


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(greedy_strategy, maze)


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(astar_strategy, maze)
