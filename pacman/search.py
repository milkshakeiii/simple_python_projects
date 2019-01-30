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


class PriorityFrontier:
    def __init__(self):
        self.heap = []
        self.evaluations = {}
        
    def __len__(self):
        return len(self.heap)
    
    def add(self, state, evaluation):
        state_item = heapq.heappush(self.heap, (evaluation, state))
        self.evaluations[state] = evaluation
        
    def pop(self):
        popped = heapq.heappop(self.heap)[1]
        del self.evaluations[popped]
        return popped

    def contains(self, state):
        return state in self.evaluations

    def value_of(self, state):
        return self.evaluations[state]

    def change_evaluation(self, state, new_evaluation):
        for i in range(len(self.heap)):
            item = self.heap[i]
            if item[1] == state:
                self.heap[i] = (new_evaluation, state)
        heapq.heapify(self.heap)
        



def third_astar(frontier, heuristic, maze):
    nodes_explored = 0
    start_state = (maze.getStart(), ''.join("1" if maze.getStart()==objective else "0" for objective in maze.getObjectives()))
    frontier.add(start_state, heuristic(start_state, maze))
    
    path_map = {start_state: [start_state[0]]}
    explored_states = {}

    while len(frontier) > 0:
        exploring_state = frontier.pop()
        nodes_explored += 1
        explored_states[exploring_state] = True
        print (nodes_explored, heuristic(exploring_state, maze))

        if (exploring_state[1].count('1') == len(maze.getObjectives())):
            return path_map[exploring_state], nodes_explored

        neighbors = maze.getNeighbors(exploring_state[0][0], exploring_state[0][1])
        for neighbor in neighbors:
            objectives_string = exploring_state[1]
            for i in range(len(maze.getObjectives())):
                if neighbor == maze.getObjectives()[i]:
                    objectives_string = objectives_string[:i] + "1" + objectives_string[i+1:]
            neighbor_state = (neighbor, objectives_string)
            evaluation = len(path_map[exploring_state]) + heuristic(neighbor_state, maze)

            if neighbor_state in explored_states:
                old_path = path_map[neighbor_state]
                new_path = path_map[exploring_state] + [neighbor_state[0]]
                if len(old_path) > len(new_path):
                    path_map[neighbor_state] = new_path
                else:
                    continue
                
            if not frontier.contains(neighbor_state):
                frontier.add(neighbor_state, evaluation)
                path_map[neighbor_state] = path_map[exploring_state] + [neighbor_state[0]]
            elif evaluation < frontier.value_of(neighbor_state):
                frontier.change_evaluation(neighbor_state, evaluation)
                path_map[neighbor_state] = path_map[exploring_state] + [neighbor_state[0]]
                             

    raise Exception("No path found.")


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
            pass
            #print(nodes_explored)
            #print(frontier_evaluations[exploring_state], exploring_state)
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
            frontier_insertion(state, heuristic(state, maze, objectives), frontier, frontier_evaluations)
    
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

def dot_heuristic(state, maze):
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
def ts_heuristic(state, maze):
    objectives = maze.getObjectives()
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


def ts_astar(maze):

    ###create a dict of shortest routes
    nodes_explored = 0
    objectives = maze.getObjectives()
    start = maze.getStart()
    cities = [maze.getStart()] + maze.getObjectives()
    trips = {}
    for city1 in cities:
        for city2 in cities:
            maze.setStart(city1)
            maze.setObjectives([city2])
            this_path, new_nodes_explored = general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)
            nodes_explored += new_nodes_explored
            trips[city1, city2] = this_path

    maze.setStart(start)
    maze.setObjectives(objectives)

    ###do astar on the weighted graph
    #nodes_explored = 0
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

            #if neighbor_state in closed_set:
                #continue

            tentative_gscore = g_score.get(current, float('inf')) + len(trips[(current[0], neighbor_state[0])]) - 1
            if neighbor_state not in open_set:
                open_set.append(neighbor_state)
            elif tentative_gscore >= g_score[neighbor_state]:
                continue

            came_from[neighbor_state] = came_from[current] + [neighbor_state]
            g_score[neighbor_state] = tentative_gscore
            f_score[neighbor_state] = g_score[neighbor_state] + mst_heuristic(remaining_cities, trips)
                
    raise Exception("No path found")


#based on Kruskal's algorithm
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

    return sum([len(trips[edge]) for edge in subset]) - len(cities) + 1

    


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
        return 1
    
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


def bfs_near_far_heuristic(state, maze, objectives):
    true_start = maze.getStart()
    
    remaining_objectives = []
    for i in range(len(objectives)):
        if state[1][i] == "0":
            remaining_objectives.append(objectives[i])

    if len(remaining_objectives) == 0:
        return 1
    
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

def near_plus_one_heuristic(state, maze):
    objectives = maze.getObjectives()
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


def bfs_heuristic(state, maze):
    true_start = maze.getStart()
    true_objectives = maze.getObjectives()
    maze.setStart(state[0])
    maze.setObjectives([objective for objective in true_objectives if state[1][true_objectives.index(objective)] == '0'])
    true_distance = len(general_pacman_search(bfs_strategy, no_heuristic, maze, quiet=True)[0])
    maze.setStart(true_start)
    maze.setObjectives(true_objectives)
    return true_distance


def subproblem_heuristic(state, maze):
    actual_start = maze.getStart()
    objectives = maze.getObjectives()

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
def astar_search(maze, heuristic):
    nodes_explored = 0
    start = maze.getStart()
    objectives = maze.getObjectives()
    start_state = (start, "0"*len(objectives))
    
    closed_set = []
    open_set = [start_state]
    came_from = {}
    g_score = {}
    f_score = {}

    f_score[start_state] = heuristic(start_state, maze, objectives)
    g_score[start_state] = 0

    while(len(open_set) > 0):
        current = min(open_set, key = lambda state: f_score[state])
        nodes_explored += 1
        print (g_score[current])
        
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
            f_score[neighbor_state] = g_score[neighbor_state] + heuristic(neighbor_state, maze, objectives)
                
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
    return general_pacman_search(greedy_strategy, dot_heuristic, maze)


def o_astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return general_pacman_search(astar_strategy, near_far_heuristic, maze)


def p_astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return astar_search(maze, near_far_heuristic)

def t_astar(maze):
    return third_astar(PriorityFrontier(), near_far_heuristic, maze)

def astar(maze):
    return ts_astar(maze)
