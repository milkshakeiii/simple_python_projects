class RBTreeNode:
    def __init__(self, value):
        self.color = False
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None

    def add_child(self, value):
        if value == self.value:
            raise "Duplicate values not allowed"
        elif value < self.value and self.left_child != None:
            raise "There is already a left child"
        elif value < self.value:
            self.left_child = RBTreeNode(value)
            self.left_child.parent = self
        elif value > self.value and self.right_child != None:
            raise "There is already a right child"
        else:
            self.right_child = RBTreeNode(value)
            self.right_child.parent = self

    def __lt__(self, other):
        return self.value < other.value

class RBTree:
    def __init__(self, head_value):
        self.head = RBTreeNode(head_value)

    def __repr__(self):
        lines = []
        frontier = [self.head]
        while len(frontier) > 0:
            lines.append(' '.join([str(node.value) for node in frontier]))
            new_frontier = []
            for node in frontier:
                if node.left_child != None:
                    new_frontier.append(node.left_child)
                if node.right_child != None:
                    new_frontier.append(node.right_child)
            frontier = new_frontier

        return '\n'.join(lines)

    def find(self, value):
        current = self.head
        while (current.value != value):
            if current.value > value and current.left_child != None:
                current = current.left_child
            elif current.value < value and current.right_child != None:
                current = current.right_child
            elif current.value < value:
                return current
            elif current.parent != None: #current.value will be > value
                return min(current, current.parent)
            else:
                return current
        return current

    def insert(self, value):
        predecessor = find(value)
           
        

T = int(input())
for i in range(T):
    N, M = map(int,input().split())
    
    problem_sets = []
    for j in range(N):
        A, B = map(int,input().split())
        problem_sets.append([A, B])
    problem_sets = sorted(problem_sets)
    
    students = list(map(int,input().split()))
    best_problems = []
    for student in students:

                #use tree
        
                best_problems.append(str(best_problem))

    print("Case #" + str(i+1) + ": " + ' '.join(best_problems))

            
