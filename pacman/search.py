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
    objectives = maze.getObjectives()

    start_state = (start, "0"*len(objectives))
    frontier = [start_state]
    explored_states = []
    best_paths = {start_state: [start]}

    while len(frontier) > 0:
        exploring_state = frontier.pop(0)
        nodes_explored += 1
        explored_states.append(exploring_state)

        if (exploring_state[1].count('1') == len(objectives)):
            return best_paths[exploring_state], nodes_explored

        neighbors = maze.getNeighbors(exploring_state[0][0], exploring_state[0][1])
        neighbor_states =[]
        for neighbor in neighbors:
            objectives_string = exploring_state[1]
            for i in range(len(objectives)):
                if neighbor == objectives[i]:
                    objectives_string = objectives_string[:i] + "1" + objectives_string[i+1:]
            neighbor_states.append((neighbor, objectives_string))

        frontier, best_paths = strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives)

    raise Exception("No route found")


def bfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier.append(state)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def dfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier.insert(0, state)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def greedy_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier.insert(0, state)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    frontier = sorted(frontier, key = lambda state: heuristic(state, objectives))
    return frontier, best_paths


def dot_heuristic(state, objectives):
    return state[1].count("0")


def heuristic(state, objectives):
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    manhattan_sum = 0
    for objective in remaining_objectives:
        manhattan_sum += abs(state[0][0] - objective[0])
        manhattan_sum += abs(state[0][1] - objective[1])

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
