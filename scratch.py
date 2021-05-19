def insert_m_into_n(m: int, n: int, j, i):
    m = m << i
    mask = int((n.bit_length()-j)*"1" + (j-i+1)*"0" + i*"1", 2)
    n = n & mask
    n = n + m
    return n


def put_m_into_n(m: int, n: int, j, i):
    mask = 2**(j-i+1)-1
    mask <<= i
    mask = ~mask
    n &= mask
    m <<= i
    n += m
    return n


def within_1_edit(a: str, b: str):
    if abs(len(a)-len(b)) >= 2:
        return False
    offset = 0
    infractions = 0
    for i in range(len(a)):
        a_char = a[i]
        b_char = b[i+offset]
        if a_char == b_char:
            continue
        infractions += 1
        if infractions > 1:
            return False
        if len(a) > i+1 and a[i+1]==b_char:
            offset = -1
        if len(b) > i+1 and b[i+1]==a_char:
            offset = 1
    return True


import numpy
from collections import deque


def find_most_apples_path(apple_matrix: numpy.ndarray):
    partial_solutions = {}
    m = apple_matrix.shape[0]
    n = apple_matrix.shape[1]
    frontier = deque([(0, 0)])
    planned = set(frontier)
    for _ in range(m*n):
        current = frontier.popleft()
        right = (current[0]+1, current[1])
        down = (current[0], current[1]+1)
        left =(current[0]-1, current[1])
        up = (current[0], current[1]-1)
        parents = [left, up]
        parent_solutions = [partial_solutions.get(parent, 0) for parent in parents]
        best_parent_solution = max(parent_solutions)
        partial_solutions[current] = best_parent_solution + apple_matrix[current]
        if (right[0] < m and right not in planned):
            frontier.append(right)
            planned.add(right)
        if (down[1] < n and down not in planned):
            frontier.append(down)
            planned.add(down)
    return partial_solutions[(m-1, n-1)]


class Node:
    def __init__(self, children: list, value: int):
        self.children = children
        self.value = value


def does_a_path_exist_between(a: Node, b: Node):
    nodes_ever_put_on_frontier = set()
    frontier = deque()
    frontier.append(a)
    nodes_ever_put_on_frontier.add(a)
    while (len(frontier) > 0):
        new_explored_node = frontier.popleft()
        if new_explored_node == b:
            return True
        for child in new_explored_node.children:
            if child not in nodes_ever_put_on_frontier:
                nodes_ever_put_on_frontier.add(child)
                frontier.append(child)
    return False


def collect_sums_recursively(node: Node):
    active_sums = []
    finished_sums = []
    for child in node.children:
        sums = collect_sums_recursively(child)
        active_sums += sums[0]
        finished_sums += sums[1]
    new_sums = []
    for active_sum in active_sums:
        new_sums.append(active_sum+node.value)
    finished_sums += active_sums
    active_sums = new_sums
    active_sums.append(node.value)
    return active_sums, finished_sums


def count_sums_matching(sum_to_match: int, head: Node):
    sums = collect_sums_recursively(head)
    all_sums = sums[0] + sums[1]
    #print(all_sums)
    return all_sums.count(sum_to_match)


def count_sums_recursively(current_node: Node, running_sum: int, running_sum_dict: dict, sum_to_match:int, matching_count: int):
    running_sum += current_node.value
    #print(running_sum)
    matching_count += running_sum_dict.get(running_sum-sum_to_match, 0)
    #print("match: " + str(matching_count))
    running_sum_dict[running_sum] = running_sum_dict.get(running_sum, 0) + 1
    for child in current_node.children:
        matching_count = count_sums_recursively(child, running_sum, running_sum_dict, sum_to_match, matching_count)
    running_sum_dict[running_sum] -= 1
    return matching_count


def better_count_sums_matching(sum_to_match: int, head: Node):
    running_sum_dict = {0: 1}
    count = count_sums_recursively(head, 0, running_sum_dict, sum_to_match, 0)
    return count


import random
import math


def fluff(times):
    head = Node([], random.randint(-20, 20))
    nodes = [head]
    for i in range(times):
        new_nodes = []
        while len(nodes) > 0:
            node = nodes.pop()
            a, b = Node([], random.randint(-20, 20)), Node([], random.randint(-20, 20))
            node.children += [a, b]
            new_nodes += [a, b]
        nodes = new_nodes
    return head


def test():
    for i in range(1000):
        head = fluff(i)
        result = better_count_sums_matching(2, head)
        n = 2**(i+1)
        nlogn = n * math.log(n, 2)
        #second_result = count_sums_matching(2, head)
        print(i, result)


def decimal_to_binary(r):
    fractional_part = r - int(r)
    bits = ["0"]*32
    continue_while = True
    while (continue_while):
        continue_while = False
        for i in range(1, 32):
            invpot = (1/2**i)
            if fractional_part != 0 and fractional_part%invpot == 0:
                fractional_part -= invpot
                print(invpot)
                bits[i] = "1"
                continue_while = True
                break
    if fractional_part != 0:
        print("ERROR")
    else:
        print("0."+''.join(bits[1:]))



            
