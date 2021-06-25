from collections import deque
from heapq import heappush, heappop

class Node():
    def __init__(self, children, value):
        self.children = children
        self.value = value
        self.marked = False
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __lt__(self, other):
        return self.value < other.value

class PriorityQueue():
    def __init__(self):
        self.heap = []
        self.nodes = {}

    def empty(self):
        return len(self.nodes) == 0

    def decrease_key_or_insert(self, old_value, new_value):
        if old_value in self.nodes:
            self.decrease_key(old_value, new_value)
        else:
            self.insert(new_value)

    def decrease_key(self, old, new):
        if old == new:
            return
        
        self.nodes[old].marked = True
        del self.nodes[old]
        self.insert(new)

    def insert(self, inserted_value):
        new_node = Node([], inserted_value)
        heappush(self.heap, new_node)
        self.nodes[inserted_value] = new_node

    def extract_minimum(self):
        popped = None
        while popped == None or popped.marked:
            popped = heappop(self.heap)
        del self.nodes[popped.value]
        return popped.value


class FibHeap():            
    def __init__(self):
        self.trees = deque()
        self.nodes = {}

    def __repr__(self):
        rep = ""

        def print_tree(tree, level):
            print("--"*level + str(tree.value))
            for child in tree.children:
                print_tree(child, level+1)
        
        for tree in self.trees:
            print_tree(tree, 1)
                
        return rep

    def __str__(self):
        return self.__repr__()

    def empty(self):
        return len(self.trees) == 0

    def find_minimum(self):
        return self.trees[-1].value

    def insert(self, inserted_value):
        if (inserted_value in self.nodes):
            raise Exception("Duplicate values not allowed")
        
        new_node = Node([], inserted_value)
        if len(self.trees) == 0 or inserted_value < self.find_minimum():
            self.trees.append(new_node)
        else:
            self.trees.appendleft(new_node)
        self.nodes[inserted_value] = new_node

    def decrease_key_or_insert(self, old_value, new_value):
        if old_value in self.nodes:
            self.decrease_key(old_value, new_value)
        else:
            self.insert(new_value)
        
    def extract_minimum(self):
        min_node = self.trees.pop()    
        self.trees += min_node.children
        for child in min_node.children:
            child.parent = None

        if (len(self.trees) == 0):
            del self.nodes[min_node.value]
            return min_node.value
        
        new_trees = {}
        for tree in self.trees:
            degree = len(tree.children)
            new_trees[degree] = new_trees.get(degree, set()).union(set([tree]))
        while not all(len(trees) <= 1 for trees in new_trees.values()):
            trees_to_update = []
            for item in new_trees.items():
                if len(item[1]) > 1:
                    trees_to_update.append(item[1])
            for trees in trees_to_update:
                both = [trees.pop(), trees.pop()]
                smaller_tree = min(both, key=lambda t: t.value)
                smaller_tree_degree = len(smaller_tree.children)
                both.remove(smaller_tree)
                bigger_tree = both[0]
                bigger_tree_degree = len(bigger_tree.children)
                smaller_tree.add_child(bigger_tree)
                new_trees[smaller_tree_degree+1] = new_trees.get(smaller_tree_degree+1, set())
                new_trees[smaller_tree_degree+1].add(smaller_tree)

        new_minimum = None
        new_minimum_key = None
        for key in new_trees.keys():
            trees = list(new_trees[key])
            if len(trees) == 0:
                continue
            tree = trees[0]
            if new_minimum == None or tree.value < new_minimum.value:
                new_minimum = tree
                new_minimum_key = key
        del new_trees[new_minimum_key]
        self.trees = deque([list(trees)[0] for trees in new_trees.values() if len(trees)>0])
        self.trees.append(new_minimum)
        del self.nodes[min_node.value]
        return min_node.value

    def decrease_key(self, old, new):
        if old == new:
            return
        
        if new in self.nodes:
            raise Exception("Second argument to decrease_key must not already exist in the heap")
        
        self.nodes[old].value = new
        self.nodes[new] = self.nodes[old]
        del self.nodes[old]
        parent = self.nodes[new].parent
        if parent != None and parent.value > new:
            parent.children.remove(self.nodes[new])
            self.nodes[new].parent = None
            if not parent.marked:
                parent.marked = True
            else:
                while parent.marked and parent.parent != None:
                    child = parent
                    parent = parent.parent
                    parent.children.remove(child)
                    self.trees.appendleft(child)
                    child.marked = False
                    child.parent = None
                parent.marked = True
            self.nodes[new].marked = False
            self.trees.appendleft(self.nodes[new])
        if new < self.find_minimum():
            self.trees.remove(self.nodes[new])
            self.trees.append(self.nodes[new])


def djikstras(source, destination, turbolifts):
    if source == destination:
        return 0
    if source not in turbolifts:
        return -1

    frontier = PriorityQueue()
    frontier.insert((0, source))
    distances = {source: 0}
    explored = set()

    while not frontier.empty():
        minimum_key = frontier.extract_minimum()[1]
        explored.add(minimum_key)
        children = turbolifts.get(minimum_key, {})
        for child in children.items():
            if child[0] in explored:
                continue
            previous_distance = distances.get(child[0], float('inf'))
            new_best = min(distances[minimum_key]+child[1], previous_distance)
            frontier.decrease_key_or_insert((previous_distance, child[0]), (new_best, child[0]))
            distances[child[0]] = new_best
        if minimum_key == destination:
            return distances[minimum_key]

    return -1

T = int(input())

for i in range(T):
    N = int(input())
    colors = []
    for j in range(N):
        #room colors
        colors.append(input())
    M = int(input())
    turbolifts = {}
    sources = []
    destinations = []
    for j in range(M):
        room1, room2, weight = map(int,input().split())
        color1 = colors[room1-1]
        color2 = colors[room2-1]
        sources.append(color1)
        destinations.append(color2)
        adjacencies = turbolifts.get(color1, {})
        turbolifts[color1] = adjacencies
        previous_weight = adjacencies.get(color2, 1001)
        adjacencies[color2] = min(previous_weight, weight)

    print("Case #" + str(i+1) + ":")
    S = int(input())
    for j in range(S):
        source, destination = map(int,input().split())
        source = colors[source-1]
        destination = colors[destination-1]
        best_path = djikstras(source, destination, turbolifts.copy())
        print(best_path)
