import math

def n_choose_m(n, m):
    return math.factorial(n)/(math.factorial(n-m)*math.factorial(m))

class TreeNode():
    def __init__(self, value, left, right):
        self.left = left
        self.right = right
        self.value = value

    def build_order_possibilities(self):
        #one side of the tree doesn't care about the order of the other
        #so one side's nodes can be inserted in to the build array at
        #any point between the other side- simply total nodes choose one side (left or right)
        #this gives us the number of possibilities for build orders of the combined tree

        #but that side could already be a combined tree with multiple posible build orders
        #so, recursively factor in the possibilities of the left and right trees!
        
        child_count = self.size() - 1
        left_size = 0
        if (self.left != None):
            left_size = self.left.size()

        left_possibilities = 1
        if (self.left != None):
            left_possibilities = self.left.build_order_possibilities()

        right_possibilities = 1
        if (self.right != None):
            right_possibilities = self.right.build_order_possibilities()

        return n_choose_m(child_count, left_size) * left_possibilities * right_possibilities

    def size(self):
        if (self.left == None and self.right == None):
            return 1
        if (self.left == None):
            return self.right.size() + 1
        if (self.right == None):
            return self.left.size() + 1
        return self.left.size() + self.right.size() + 1

    def insert(self, node):
        if (node.value < self.value):
            if (self.left == None) :
                self.left = node
            else:
                self.left.insert(node)
        else:
            if (self.right == None):
                self.right = node
            else:
                self.right.insert(node)

def answer(seq):
    if (len(seq) == 1):
        return 1

    root = TreeNode(seq[0], None, None)

    for bunny_age in seq[1:]:
        root.insert(TreeNode(bunny_age, None, None))

    return str(int(root.build_order_possibilities()))
