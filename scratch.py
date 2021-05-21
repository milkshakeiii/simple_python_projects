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


def possible_ways_to_climb_stairs(n):
    possible_ways = [1, 1, 2]
    for i in range(3, n+1):
        possible_ways.append(possible_ways[i-3]+
                             possible_ways[i-2]+
                             possible_ways[i-1])
    return possible_ways[n]
            
def snarky_count(a):
    number_string = ''.join(map(str, a))
    incremented_number = int(number_string)+1
    incremented_number_string = ' '.join(str(incremented_number))
    return list(map(int, incremented_number_string.split()))

def guai_count(a: list):
    a = a.copy()
    digit_to_modify=a[-1]
    index = len(a)-1
    while(index >= 0 and a[index]==9):
        index -= 1
    if index == -1:
        index = 0
        a.insert(0, 0)
    for i in range(index, len(a)):
        a[i] = (a[i]+1)%10
    return a

import time

def test_count():
    cases = []
    for i in range(10000):
        a = []
        a.append(random.randint(1, 9))
        for i in range(1, 1000):
            a.append(random.randint(0, 9))
        cases.append(a)
    start = time.time()
    results1 = [snarky_count(a) for a in cases]
    middle = time.time()
    results2 = [guai_count(a) for a in cases]
    end = time.time()
    print("snarky time: " + str(middle-start))
    print("guai time: " + str(end-middle))
    print("all matching: " + str(results1==results2))
    for i in range(len(results1)):
        if results1[i]!=results2[i]:
            print("a, b")
            print(results1[i], results2[i])

from collections import Counter

def permutation_matches(short_string, long_string):
    short_string_letters = Counter(short_string)
    first_substring = long_string[0:len(short_string)]
    running_letters = Counter(first_substring[:-1]+long_string[-1])
    matches = 0
    for i in range(0, len(long_string)-len(short_string)+1):
        running_letters[long_string[i-1]] -= 1
        if running_letters[long_string[i-1]] == 0:
            del running_letters[long_string[i-1]]
        running_letters[long_string[i+len(short_string)-1]] += 1
        if running_letters == short_string_letters:
            print(long_string[i:i+len(short_string)])
            matches += 1
    return matches

'''
This isn't the way to do it- instead you should just:
1. remove all cycles
2. count parentless nodes
3. 
'''
def count_new_flights_needed_to_connect_airports(airports, flights):
    #preprocess edges
    edges = {}
    for flight in flights:
        edges[flight[0]] = flight[1]

    #find "connected components" unique tree heads
    parsed_airports = set()
    airports_to_sources = {}
    sources_to_children = {}
    connected_components = 0
    for airport in airports:
        if airport in parsed_airports:
            continue
        parse_branch(edges, airport, airports_to_sources, sources_to_children, parsed_airports)

    len(sources_to_children)

def parse_branch(edges, head, nodes_to_heads, heads_to_children, parsed_nodes):
    frontier = [head]
    while (len(frontier) > 0):
        current_node = frontier.pop()
        if current_node in parsed_nodes and current_node_head == current_node:
            current_node_head = nodes_to_heads[current_node]
            heads_to_children[head] = heads_to_children[head].union(heads_to_children[current_node])
            for node in heads_to_children[current_node]:
                nodes_to_heads[node] = head
            del heads_to_children[current_node]
        if current_node in parsed_nodes:
            return
        else:
            parsed_nodes.add(current_node)
            nodes_to_heads[current_node] = head
            frontier += [next_node for next_node in edges[current_node]]

def substrings(s):
    for i in range(2**len(s)):
        next_substring = ""
        for j in range(i.bit_length()):
            if i%2 == 1:
                next_substring += (s[j])
            i >>= 1
        yield next_substring

def recursive_substrings(s):
    if s == '':
        return []
    substrings = [s]
    for i in range(len(s)):
        substrings += recursive_substrings(s[:i]+s[i+1:])
    return substrings

def nonredundant_substrings(s):
    substrings = set()
    frontier = set([s])
    while len(frontier)>0:
        current = frontier.pop()
        substrings.add(current)
        children = [current[:i]+current[i+1:] for i in range(len(current))]
        frontier.update(children)
    return substrings

def hanoi(towers, number, source, target, third_tower):
    if number == 0:
        return
    hanoi(towers, number-1, source, third_tower, target)
    move_me = towers[source].pop()
    towers[target].append(move_me)
    print(towers)
    hanoi(towers, number-1, third_tower, target, source)

def print_parens(assigned, remaining):
    if (remaining == 0):
        print(assigned)
    else:
        for i in range(len(assigned)+1):
            for j in range(i+1, len(assigned)+2):
                old_chars = list(reversed(assigned))
                new_assigned = ""
                for k in range(len(assigned)+2):
                    if (k==i):
                        new_assigned += "("
                    elif (k==j):
                        new_assigned += ")"
                    else:
                        new_assigned += old_chars.pop()
                print_parens(new_assigned, remaining-1)
