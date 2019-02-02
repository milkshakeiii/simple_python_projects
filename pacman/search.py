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

import copy, itertools, collections, heapq


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
    frontier = [start_state]
    frontier_evaluations = {start_state: heuristic(start_state, maze)}
    explored_states = {}
    best_paths = {start_state: [start]}

    while len(frontier) > 0:
        exploring_state = frontier.pop(0)
        nodes_explored += 1
        if not quiet:
            print(nodes_explored)
            print(frontier_evaluations[exploring_state], exploring_state)
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

        frontier, best_paths = strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, frontier_evaluations, maze, objectives, heuristic)

    raise Exception("No route found")


def bfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, frontier_evaluations, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in frontier_evaluations and state not in explored_states:
            frontier.append(state)
            frontier_evaluations[state] = 0
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def dfs_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, frontier_evaluations, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in frontier and state not in explored_states:
            frontier.insert(0, state)
            frontier_evaluations[state] = 0
            best_paths[state] = best_paths[exploring_state] + [state[0]]
    return frontier, best_paths


def frontier_insertion(insert_me, evaluation, frontier, frontier_evaluations):
    frontier_evaluations[insert_me] = evaluation
    for i in range(len(frontier)):
        state = frontier[i]
        if frontier_evaluations[state] <= evaluation:
            continue
        else:
            frontier.insert(i, insert_me)
            return
    frontier.append(insert_me)


def greedy_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, frontier_evaluations, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in frontier_evaluations and state not in explored_states:
            best_paths[state] = best_paths[exploring_state] + [state[0]]
            frontier_insertion(state, heuristic(state, maze), frontier, frontier_evaluations)
    
    return frontier, best_paths


def astar_strategy(neighbor_states, exploring_state, best_paths, explored_states, frontier, frontier_evaluations, maze, objectives, heuristic):
    for state in reversed(neighbor_states):
        if state not in explored_states and state not in frontier:
                best_paths[state] = best_paths[exploring_state] + [state[0]]
                evaluation = len(best_paths[exploring_state]) + heuristic(state, maze)
                frontier_insertion(state, evaluation, frontier, frontier_evaluations)
        elif state in frontier:
            old_best_path = best_paths[state]
            current_path = best_paths[exploring_state] + [state[0]]
            if len(current_path) < len(old_best_path):
                best_paths[state] = current_path
                frontier.remove(state)
                del frontier_evaluations[state]
                evaluation = len(best_paths[exploring_state]) + heuristic(state, maze)
                frontier_insertion(state, evaluation, frontier, frontier_evaluations)
        elif state in explored_states:
            old_best_path = best_paths[state]
            current_path = best_paths[exploring_state] + [state[0]]
            if len(current_path) < len(old_best_path):
                best_paths[state] = current_path
                del explored_states[state]
                del frontier_evaluations[state]
                evaluation = len(best_paths[exploring_state]) + heuristic(state, maze)
                frontier_insertion(state, evaluation, frontier, frontier_evaluations)
            
    return frontier, best_paths

trips = {}
def near_plus_mst_heuristic(state, maze):
    objectives = maze.getObjectives()
    start = maze.getStart()
    
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 1 #since even if pacman starts at the goal, paths are defined to include both starting point and goal

    nearest_objective = (-1, -1)
    nearest_manhattan = float('inf')
    for objective in remaining_objectives:
        this_manhattan = abs(state[0][0] - objective[0]) + abs(state[0][1] - objective[1])
        if this_manhattan < nearest_manhattan:
            nearest_manhattan = this_manhattan
            nearest_objective = objective

    cities = remaining_objectives

    if len(trips) == 0:
        for i in range(len(cities)):
            city1 = cities[i]
            for city2 in cities[i+1:]:
                maze.setStart(city1)
                maze.setObjectives([city2])
                this_path, new_nodes_explored = general_pacman_search(astar_strategy, near_far_heuristic, maze, quiet=True)
                #nodes_explored += new_nodes_explored #since this is not really part of the astar search, I don't count it towards nodes_explored
                #as a result, if there are a small number of dots, nodes_explored will be quite low.  that is because the bulk of the work was done here
                trips[city1, city2] = this_path
                trips[collections, city1] = list(reversed(this_path))

        maze.setStart(start)
        maze.setObjectives(objectives)

    #print(mst_heuristic(cities, trips))
    return mst_heuristic(cities, trips) + nearest_manhattan
    


def dot_heuristic(state, maze):
    return state[1].count("0")


def ts_astar(maze):

    ###all optimal paths will be sequences of optimal paths between two dots.
    ###the optimal path from one dot to another is much easier to find than the whole many-dot problem.
    ###so we begin by creating a dictionary of dot pairs to optimal paths
    nodes_explored = 0
    objectives = maze.getObjectives()
    start = maze.getStart()
    cities = [maze.getStart()] + maze.getObjectives()
    trips = {}
    for i in range(len(cities)):
        city1 = cities[i]
        for city2 in cities[i+1:]:
            maze.setStart(city1)
            maze.setObjectives([city2])
            this_path, new_nodes_explored = general_pacman_search(astar_strategy, near_far_heuristic, maze, quiet=True)
            nodes_explored += new_nodes_explored #since this is not really part of the astar search, I don't count it towards nodes_explored
            #as a result, if there are a small number of dots, nodes_explored will be quite low.  that is because the bulk of the work was done here
            trips[city1, city2] = this_path
            trips[city2, city1] = list(reversed(this_path))

    maze.setStart(start)
    maze.setObjectives(objectives)
    print("Done with parsing into TSP")

    ###after we obtain the dictionary of optimal paths, the problem simply becomes the traveling salesperson
    ###so we simply do astar on the weighted graph, for part of this I referenced the wikipedia page on A* search
    
    start_state = (start, "0" + "0"*len(objectives))
    
    closed_set = []
    open_set = [start_state]
    came_from = {start_state: [start_state]}
    g_score = {}
    f_score = {}

    f_score[start_state] = mst_heuristic(cities, trips)
    g_score[start_state] = 0

    while(len(open_set) > 0):
        current = min(open_set, key = lambda state: f_score[state])
        nodes_explored += 1
        
        if current[1].count('1') == len(objectives):
            path = [came_from[current][0][0]]
            previous = came_from[current][0]
            for state in came_from[current][1:]:
                path = path + trips[(previous[0], state[0])][1:]
                previous = state
            return path, nodes_explored

        open_set.remove(current)
        closed_set.append(current)
        remaining_cities = [cities[i] for i in range(len(cities)) if current[1][i] == "0" and cities[i] != current[0]]

        for neighbor in remaining_cities:
            neighbor_state = (neighbor, ''.join([current[1][i] if cities[i] != current[0] else "1" for i in range(len(cities))]))

            #mst_heuristic is not consistent so if the state is in the closed set we might need to update its best path and explore it agin
            tentative_gscore = g_score.get(current, float('inf')) + len(trips[(current[0], neighbor_state[0])]) - 1
            if neighbor_state not in open_set and (neighbor_state not in closed_set or tentative_gscore < g_score[neighbor_state]):
                open_set.append(neighbor_state)
            elif tentative_gscore >= g_score[neighbor_state]:
                continue

            came_from[neighbor_state] = came_from[current] + [neighbor_state]
            g_score[neighbor_state] = tentative_gscore
            f_score[neighbor_state] = g_score[neighbor_state] + mst_heuristic(remaining_cities, trips)
                
    raise Exception("No path found")


#based on Kruskal's algorithm
#this heuristic is admissable because the true best path is a spanning tree,
#so the minimum spanning tree must be less than or equal to it in weight
def mst_heuristic(cities, trips):
    edges = sorted(trips.keys(), key = lambda key: len(trips[key]))
    subset = set()
    forest = {}
    for city in cities:
        forest[city] = set([city])
    
    for edge in edges:
        if edge[0] in forest and edge[1] in forest and forest[edge[0]] != forest[edge[1]]:
            subset.add(edge)
            for city in forest[edge[0]]:
                forest[city] = forest[city].union(forest[edge[1]])
            for city in forest[edge[1]]:
                forest[city] = forest[city].union(forest[edge[0]])
            if len(forest[edge[0]]) == len(cities):
                break

    result = sum([len(trips[edge]) for edge in subset]) - len(cities) + 1
    return result


def objective_subset_string(objectives, subset):
    return ''.join('1' if objective in subset else '0' for objective in objectives)

            
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def no_heuristic(state, maze):
    return 0


def near_far_heuristic(state, maze):
    objectives = maze.getObjectives()
    
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 1 #since even if pacman starts at the goal, paths are defined to include both starting point and goal
    
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

    return nearest_manhattan + farthest_manhattan + 1




def bfs(maze):
    # return path, num_states_explored
    return general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(dfs_strategy, no_heuristic, maze, quiet=True)


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(greedy_strategy, near_far_heuristic, maze, quiet=True)


def o_astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(astar_strategy, near_plus_mst_heuristic, maze, quiet=True)


def astar(maze):
    return ts_astar(maze)
