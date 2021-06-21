import math, itertools

def answer(N, K):
    return str(int(recursive_answer(N, K)))

#memoized recursive method will perform similarly to tabular method
memoized_calls = {}
def recursive_answer(N, K):
    if (N, K) in memoized_calls:
        return memoized_calls[N, K]

    if K == N-1:
        memoized_calls[N, K] = int(math.pow(N, N-2))
        return int(math.pow(N, N-2))

    #there are n(n-1)/2 possible tunnels
    #there are n(n-1)/2 choose k choices of tunnel possible
    #subtract the number of choices that exclude warrens to find answer

    possible_tunnels = N*(N-1)//2
    possible_choices = n_choose_m(possible_tunnels, K)

    unconnected_choices = 0
    for i in range(0, N-1):
        for j in range(max ( [( K - int ((1/2) * (i+1) * i) ), 0] ), K-i+1):
            unconnected_choices += n_choose_m(N - 1, i) * n_choose_m( (N-1-i)*(N-2-i)//2, j ) * blob_answer(i + 1, K - j)

    connected_choices = possible_choices - unconnected_choices
    memoized_calls[N, K] = connected_choices
    return connected_choices


#memoized recursive method will perform similarly to tabular method
memoized_calls = {}
def other_recursive_answer(N, K):
    if (N, K) in memoized_calls:
        return memoized_calls[N, K]
    
    if K == N-1:
        minimally_connected_solution = math.pow(N, N-2)
        memoized_calls[N, K] = minimally_connected_solution
        return minimally_connected_solution

    #there are n(n-1)/2 possible tunnels
    #there are n(n-1)/2 choose k choices of tunnel possible
    #subtract the number of choices that exclude warrens to find answer

    possible_tunnels = N*(N-1)//2
    possible_choices = n_choose_m(possible_tunnels, K)
    #possible_choices = n_choose_m(N*(N-1)//2, K) - sum( [n_choose_m( N-1, i) * sum( [n_choose_m( (N-1-i)*(N-2-i)//2, j) * recursive_answer(i+1, K-j) for j in range(K+1)]) for i in range(N-1)] )

    unconnected_choices = 0
    for i in range(N-1):
        #we can shave off unnecessary solutions
        #i referenced Marko Riedel's math stackexchange post
        #(http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges/690422#690422)
        for j in range(max ( [( K - int ((1/2) * (i+1) * i) ), 0] ), K-i+1):
            unconnected_choices += n_choose_m(N-1, i)*n_choose_m( (N-1-i)*(N-2-i)/2, j ) * other_recursive_answer(i + 1, K - j)

        
    

    connected_choices = possible_choices - unconnected_choices
    memoized_calls[N, K] = connected_choices
    return connected_choices


#memoized recursive method will perform similarly to tabular method
memoized_calls = {}
def recursive_answer(N, K):
    
    if (N, K) in memoized_calls:
        return memoized_calls[N, K]
    
    if K < N-1 or K > N*(N-1)/2:
        memoized_calls[N, K] = 0
        return 0
    if K == N-1:
        memoized_calls[N, K] = math.pow(N, N-2)
        return math.pow(N, N-2)

    #there are n(n-1)/2 possible tunnels
    #there are n(n-1)/2 choose k choices of tunnel possible
    #subtract the number of choices that exclude warrens to find answer

    possible_tunnels = N*(N-1)/2
    possible_choices = n_choose_m(possible_tunnels, K)

    unconnected_choices = 0
    for i in range(0, N-1):
        inner_unconnected_choices = 0
        for j in range(0, K+1):
            #i got help from Marko Riedel's math stackexchange post for this part
            #(http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges/690422#690422)

            inner_unconnected_choices += n_choose_m((N-1-i)*(N-2-i)/2, j)*recursive_answer(i+1, K-j)

        unconnected_choices += inner_unconnected_choices * n_choose_m(N-1, i)

    possible_connected_choices = possible_choices - unconnected_choices
    memoized_calls[N, K] = possible_connected_choices
    return possible_connected_choices



def n_choose_m(n, m):
    if (m > n):
        return 0
    return math.factorial(n) // (math.factorial(n-m)*math.factorial(m))

def brute_answer(N, K):
    

    all_links = [i for i in range(N*(N-1))]

    links = []
    for link in all_links:
        if (link % (N-1) ) == 0:
            node = all_links[link:link+N-1]
            node_number = math.floor(link/(N-1))
            for i in range(node_number):
                node.remove(node_number*(N-1) + i)
            links = links + node
        
    #print(links)

    link_combinations = itertools.combinations(links, K)

    ok_combinations = 0

    for chosen_links in link_combinations:
        nodes = [[False for i in range(N)] for i in range(N)]
        
        for link in chosen_links:
            from_index = math.floor(link/(N-1))
            to_index = link%(N-1)

            if to_index >= from_index:
                to_index += 1

            #print (link)
            #print("from: " + str(from_index))
            #print("to: " + str(to_index))
            nodes[from_index][to_index] = True
            nodes[to_index][from_index] = True

        #print (nodes)
        connected_nodes = [0]
        frontier = [0]
        while len(frontier) != 0:
            #print (frontier)
            node_index = frontier.pop()
            node = nodes[node_index]
            for linked_node_index in range(len(node)):
                if linked_node_index in connected_nodes:
                    #print ("i know")
                    continue
                if node[linked_node_index]:
                    connected_nodes.append(linked_node_index)
                    frontier.append(linked_node_index)

        #print (len(connected_nodes))
        if len(connected_nodes) == N:
            #print ("ok")
            ok_combinations += 1


    return ok_combinations

'''
Undercover underground
======================

As you help the rabbits establish more and more resistance groups to fight against Professor Boolean, you need a way to pass messages back and forth.

Luckily there are abandoned tunnels between the warrens of the rabbits, and you need to find the best way to use them. In some cases, Beta Rabbit wants a high level of interconnectedness, especially when the groups show their loyalty and worthiness. In other scenarios the groups should be less intertwined, in case any are compromised by enemy agents or zombits.

Every warren must be connected to every other warren somehow, and no two warrens should ever have more than one tunnel between them. Your assignment: count the number of ways to connect the resistance warrens.

For example, with 3 warrens (denoted A, B, C) and 2 tunnels, there are three distinct ways to connect them:

A-B-C
A-C-B
C-A-B

With 4 warrens and 6 tunnels, the only way to connect them is to connect each warren to every other warren.

Write a function answer(N, K) which returns the number of ways to connect N distinctly labelled warrens with exactly K tunnels, so that there is a path between any two warrens. 

The return value must be a string representation of the total number of ways to do so, in base 10.
N will be at least 2 and at most 20. 
K will be at least one less than N and at most (N * (N - 1)) / 2

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) N = 2
    (int) K = 1
Output:
    (string) "1"

Inputs:
    (int) N = 4
    (int) K = 3
Output:
    (string) "16"
    '''
