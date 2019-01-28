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

import copy, itertools, collections


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
    frontier = collections.OrderedDict([(start_state, heuristic(start_state, objectives))])
    explored_states = {}
    best_paths = {start_state: [start]}

    while len(frontier) > 0:
        exploring_state = frontier.popitem(0)[0]
        nodes_explored += 1
        print (nodes_explored)
        explored_states[exploring_state] = True

        if (exploring_state[1].count('1') == len(objectives)):
            return best_paths[exploring_state], nodes_explored

        neighbors = maze.getNeighbors(exploring_state[0][0], exploring_state[0][1])
        neighbor_states = []
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
            frontier[state] = 0
            frontier.move_to_end(state)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def dfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier[state] = 0
            frontier.move_to_end(state, last=False)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def greedy_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            best_paths[state] = best_paths[exploring_state] + [state[0]]
            frontier[state] = heuristic(state, objectives) #greedy evaluation
    frontier = OrderedDict([(key, frontier[key]) for key in sorted(frontier, key = lambda state: frontier[state])])
    return frontier, best_paths


def astar_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, objectives):
    for state in reversed(neighbor_states):
        if state not in explored_states:
            if state not in frontier:
                best_paths[state] = best_paths[exploring_state] + [state[0]]
                frontier[state] = len(best_paths[state]) + ts_heuristic(state, objectives) #astar evaluation
            else:
                old_best_path = best_paths[state]
                current_path = best_paths[exploring_state] + [state[0]]
                if len(current_path) < len(old_best_path):
                    best_paths[state] = current_path
                else:
                    continue
            
    frontier = collections.OrderedDict([(key, frontier[key]) for key in sorted(frontier, key = lambda state: frontier[state])])
    return frontier, best_paths

def dot_heuristic(state, objectives):
    return state[1].count("0")


#based on the held-karp algorithm
def ts_heuristic(state, objectives):
    print(state, objectives)
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 0

    subset_endpoints_to_pathlengths = {("0"*len(remaining_objectives), state[0]): 0}
    for num_to_eat in range(1, len(remaining_objectives)+1):
        for subset in itertools.combinations(remaining_objectives, num_to_eat):
            subset = set(subset)
            for endpoint in subset:
                subsubset = copy.deepcopy(subset)
                subsubset.remove(endpoint)
                if len(subsubset) == 0:
                    subsubset = set([state[0]])
                best_option_cost = float('inf')
                for preendpoint in subsubset:
                    this_option_cost = subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, subsubset), preendpoint] + manhattan(preendpoint, endpoint)
                    if this_option_cost < best_option_cost:
                        best_option_cost = this_option_cost
                subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, subset), endpoint] = best_option_cost

    return min([subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, remaining_objectives), endpoint] for endpoint in remaining_objectives])

def objective_subset_string(objectives, subset):
    return ''.join('1' if objective in subset else '0' for objective in objectives)
            
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
        

#from python docs https://docs.python.org/3/library/itertools.html#recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def heuristic(state, objectives):
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 0
    
    nearest_objective = (-1, -1)
    nearest_manhattan = float('inf')
    for objective in remaining_objectives:
        this_manhattan = abs(state[0][0] - objective[0]) + abs(state[0][1] - objective[1])
        if this_manhattan < nearest_manhattan:
            nearest_manhattan = this_manhattan
            nearest_objective = objective

    remaining_objectives.remove(nearest_objective)
    farthest_objective = (-1, -1)
    farthest_manhattan = 0
    for objective in remaining_objectives:
        this_manhattan = abs(nearest_objective[0] - objective[0]) + abs(nearest_objective[1] - objective[1])
        if this_manhattan > farthest_manhattan:
            farthest_manhattan = this_manhattan
            farthest_objective = objective

    return nearest_manhattan + farthest_manhattan
    #return 0 if len(manhattan_sums) == 0 else sum(manhattan_sums)






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
