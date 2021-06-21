from collections import deque

class Node():
    def __init__(self, children, value):
        self.children = children
        self.value = value
        self.marked = False
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

class FibHeap():            
    def __init__(self):
        self.trees = deque()
        self.nodes = {}

    def __repr__(self):
        rep = ""
        for tree in self.trees:
            rep += str((tree.value, len(tree.children)))
            rep += "\n"
        return rep

    def __str__(self):
        return self.__repr__()

    def find_minimum(self):
        return self.trees[-1].value
    
    def merge(self, other_heap):
        self.trees += other_heap.trees

    def insert(self, inserted_value):
        new_node = Node([], inserted_value)
        if len(self.trees) == 0 or inserted_value < self.find_minimum():
            self.trees.append(new_node)
        else:
            self.trees.appendleft(new_node)
        self.nodes[inserted_value] = new_node
        
    def extract_minimum(self):
        min_node = self.trees.pop()
        self.trees += min_node.children
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

        new_minimum = Node([], float('inf'))
        new_minimum_key = None
        for key in new_trees.keys():
            trees = list(new_trees[key])
            if len(trees) == 0:
                continue
            tree = trees[0]
            if tree.value < new_minimum.value:
                new_minimum = tree
                new_minimum_key = key
        del new_trees[new_minimum_key]
        self.trees = [list(trees)[0] for trees in new_trees.values() if len(trees)>0]
        self.trees.append(new_minimum)
        del self.nodes[min_node.value]
        return min_node.value

    def decrease_key(self, old, new):
        node = self.nodes[old]
        del self.nodes[old]
        node.value = new
        self.nodes[new] = node
        if new.parent != None:
            parent = new.parent
            new.parent.children.remove(new)
            new.parent = None
            while parent.marked:
                parent.marked = False
                child = parent
                parent = parent.parent
                parent.children.remove(child)
                child.parent = None

    def delete(self, value):
        self.decrease_key(value, float('-inf'))
        self.extract_minimum()

def djikstras(source, destination, turbolifts):
    if source == destination:
        return 0
    if source not in turbolifts:
        return -1

    frontier = {}
    frontier[source] = 0

    while len(frontier) > 0:
        minimum_key = min(frontier.items(), key=lambda item: item[1])[0]
        children = turbolifts.get(minimum_key, {})
        for child in children.items():
            previous_distance = frontier.get(child[0], float('inf'))
            new_best = min(frontier[minimum_key]+child[1], previous_distance)
            frontier[child[0]] = new_best
        if minimum_key == destination:
            return frontier[minimum_key]
        del frontier[minimum_key]

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
