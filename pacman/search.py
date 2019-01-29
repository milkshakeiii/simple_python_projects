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
        "astar": astar
    }.get(searchMethod)(maze)


def general_pacman_search(strategy, heuristic, maze, quiet=False):
    nodes_explored = 0
    start = maze.getStart()
    objectives = maze.getObjectives()

    start_state = (start, ''.join("1" if maze.getStart()==objective else "0" for objective in objectives))
    frontier = collections.OrderedDict([(start_state, heuristic(start_state, maze, objectives))])
    explored_states = {}
    best_paths = {start_state: [start]}

    while len(frontier) > 0:
        exploring_state_item = frontier.popitem(0)
        exploring_state = exploring_state_item[0]
        nodes_explored += 1
        if not quiet:
            pass
            #print(nodes_explored)
            print(exploring_state_item[1])
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

        frontier, best_paths = strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, maze, objectives, heuristic)

    raise Exception("No route found")


def bfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier[state] = 0
            frontier.move_to_end(state)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def dfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, maze, objectives, heuristic):
    for state in neighbor_states:
        if state not in frontier and state not in explored_states:
            frontier[state] = 0
            frontier.move_to_end(state, last=False)
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def greedy_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            best_paths[state] = best_paths[exploring_state] + [state[0]]
            frontier[state] = dot_heuristic(state, maze, objectives) #greedy evaluation
    frontier = collections.OrderedDict([(key, frontier[key]) for key in sorted(frontier, key = lambda state: frontier[state])])
    return frontier, best_paths


def astar_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in explored_states:
            if state not in frontier:
                best_paths[state] = best_paths[exploring_state] + [state[0]]
                frontier[state] = len(best_paths[exploring_state]) + heuristic(state, maze, objectives) #astar evaluation
            else:
                old_best_path = best_paths[state]
                current_path = best_paths[exploring_state] + [state[0]]
                if len(current_path) < len(old_best_path):
                    best_paths[state] = current_path
                else:
                    continue
            
    frontier = collections.OrderedDict([(key, frontier[key]) for key in sorted(frontier, key = lambda state: frontier[state])])
    return frontier, best_paths

def dot_heuristic(state, maze, objectives):
    return state[1].count("0")


def naive_ts_heuristic(state, maze, objectives):
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 0

    start = state[0]
    total_steps = 0
    while len(remaining_objectives) > 0:
        nearest_objective = (-1, -1)
        nearest_manhattan = float('inf')
        for objective in remaining_objectives:
            this_manhattan = manhattan(start, objective)
            if this_manhattan < nearest_manhattan:
                nearest_manhattan = this_manhattan
                nearest_objective = objective
        remaining_objectives.remove(nearest_objective)
        total_steps += nearest_manhattan
        start = nearest_objective

    return total_steps


#based on the held-karp algorithm
def ts_heuristic(state, maze, objectives):
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 0

    subset_endpoints_to_pathlengths = {}

    for objective in remaining_objectives:
        subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, [objective]), objective] = manhattan(state[0], objective)
    
    for num_to_eat in range(2, len(remaining_objectives)+1):
        for subset in itertools.combinations(remaining_objectives, num_to_eat):
            subset_string = objective_subset_string(objectives, subset)
            for endpoint in subset:
                subsubset = [square for square in subset if square != endpoint]
                subsubset_string = objective_subset_string(remaining_objectives, subsubset)
                best_option_cost = float('inf')
                for preendpoint in subset:
                    if preendpoint == endpoint:
                        continue
                    this_option_cost = subset_endpoints_to_pathlengths[subsubset_string, preendpoint] + manhattan(preendpoint, endpoint)
                    if this_option_cost < best_option_cost:
                        best_option_cost = this_option_cost
                subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, subset), endpoint] = best_option_cost

    return min([subset_endpoints_to_pathlengths[objective_subset_string(remaining_objectives, remaining_objectives), endpoint] for endpoint in remaining_objectives])


def objective_subset_string(objectives, maze, subset):
    return ''.join('1' if objective in subset else '0' for objective in objectives)

            
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def no_heuristic(state, maze, objectives):
    return 0


def near_far_heuristic(state, maze, objectives):
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


def bfs_near_far_heuristic(state, maze, objectives):
    true_start = maze.getStart()
    
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 0
    
    nearest_objective = (-1, -1)
    nearest_distance = float('inf')
    for objective in remaining_objectives:
        maze.setStart(state[0])
        maze.setObjectives([objective])
        this_distance = len(general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)[0])
        if this_distance < nearest_distance:
            nearest_distance = this_distance
            nearest_objective = objective
        maze.setStart(true_start)
        maze.setObjectives(objectives)

    remaining_objectives.remove(nearest_objective)
    if len(remaining_objectives) == 0:
        return nearest_distance
    
    farthest_distance = float('-inf')
    for objective in remaining_objectives:
        maze.setStart(nearest_objective)
        maze.setObjectives([objective])
        this_distance = len(general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)[0])
        if this_distance > farthest_distance:
            farthest_distance = this_distance
            farthest_objective = objective
        maze.setStart(true_start)
        maze.setObjectives(objectives)

    return nearest_distance + farthest_distance

def near_plus_one_heuristic(state, maze, objectives):
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
    return nearest_manhattan + len(remaining_objectives)


def bfs_heuristic(state, maze, objectives):
    actual_start = maze.getStart()

    real_distances = []
    for objective in objectives:
        maze.setStart(state[0])
        maze.setObjectives([objective])
        real_dist = len(general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)[0])
        #print(maze.getStart())
        #print(real_dist)
        real_distances.append(real_dist)

    maze.setStart(actual_start)
    maze.setObjectives(objectives)
    return min(real_distances) + state[1].count('0') - 1
    


#based on pseudocode from wikipedia A* page
def reconstruct_path(came_from, state):
    total_path = [state]
    while state in came_from:
        state = came_from[state]
        total_path.append(state)

    return [state[0] for state in total_path]


#also based on pseudocode from wikipedia A* page
def astar_search(maze):
    nodes_explored = 0
    start = maze.getStart()
    objectives = maze.getObjectives()
    start_state = (start, "0"*len(objectives))
    
    closed_set = []
    open_set = [start_state]
    came_from = {}
    g_score = {}
    f_score = {}

    f_score[start_state] = bfs_heuristic(start_state, maze, objectives)
    g_score[start_state] = 0

    while(len(open_set) > 0):
        current = min(open_set, key = lambda state: f_score[state])
        nodes_explored += 1
        print(nodes_explored)
        
        if current[1].count('1') == len(objectives):
            print (reconstruct_path(came_from, current), nodes_explored)
            return reconstruct_path(came_from, current), nodes_explored

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in maze.getNeighbors(current[0][0], current[0][1]):
            objective_string = current[1]
            neighbor_state = (neighbor, objective_string)
            if neighbor in objectives:
                index = objectives.index(neighbor)
                objective_string = objective_string[:index] + "1" + objective_string[index+1:]
                neighbor_state = (neighbor, objective_string)

            if neighbor_state in closed_set:
                continue

            tentative_gscore = g_score.get(current, float('inf')) + 1
            if neighbor_state not in open_set:
                open_set.append(neighbor_state)
            elif tentative_gscore >= g_score[neighbor_state]:
                continue

            came_from[neighbor_state] = current
            g_score[neighbor_state] = tentative_gscore
            f_score[neighbor_state] = g_score[neighbor_state] + bfs_heuristic(neighbor_state, maze, objectives)
                
    raise Exception("No path found")



def bfs(maze):
    
    # return path, num_states_explored
    return general_pacman_search(bfs_strategy, no_heuristic, maze)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(dfs_strategy, no_heuristic, maze)


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(greedy_strategy, no_heuristic, maze)


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(astar_strategy, near_far_heuristic, maze)


def pure_astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return astar_search(maze)
