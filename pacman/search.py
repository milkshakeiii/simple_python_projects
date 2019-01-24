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
        exploring_path = frontier.pop(0)
        nodes_explored += 1
        
        if len(exploring_path[1]) == len(objectives):
            return_path = [(step[0], step[1]) for step in exploring_path[0]]
            return return_path, nodes_explored
        
        new_neighbors = maze.getNeighbors(exploring_path[0][-1][0], exploring_path[0][-1][1])
        neighbor_states = []
        for neighbor in new_neighbors:
            captured_objectives = copy.deepcopy(exploring_path[1])
            if neighbor in objectives:
                captured_objectives.add(neighbor)
            neighbor_states.append((neighbor, captured_objectives))
                
        allowable_neighbor_states = [neighbor for neighbor in neighbor_states if neighbor not in forbidden_states]
        forbidden_states = forbidden_states + allowable_neighbor_states
        frontier = strategy(allowable_neighbor_states, exploring_path, frontier, maze)

    raise Exception("No route found")



def bfs_strategy(append_us, exploring_path, frontier, maze):
    for state in append_us:
        frontier = frontier + [(exploring_path[0] + [state[0]], state[1])]
    return frontier

def dfs_strategy(append_us, exploring_path, frontier, maze):
    for state in append_us:
        frontier = [(exploring_path[0] + [state[0]], state[1])] + frontier
    return frontier

    

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
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
