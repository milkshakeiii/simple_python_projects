def process_connected_component(start_variable,
                                determined_variables,
                                explored,
                                graph):
    if start_variable in explored:
        return
    explored[start_variable] = 0
    if len(graph[start_variable]) == 0:
        return
    frontier = []
    for edge in graph[start_variable]:
        frontier.append([start_variable])
    while len(frontier) > 0:
        current_path = frontier.pop()
        for next_vertex in graph[current_path[-1]].keys():
            next_path = current_path[:]
            next_path.append(next_vertex)
            parity = len(next_path)%2
            if next_vertex in explored and explored[next_vertex] != parity:
                determine_variables(graph, determined_variables, next_path)
                return
            elif next_vertex not in explored:
                frontier.append(next_path)
                explored[next_vertex] = parity

def determine_variables(graph, determined_variables, cycle):
    pass
    

T = int(input())
for i in range(T):
    N = int(input())
    graph = {}
    for j in range(N):
        left, right = input().split("=")
        result = int(right)
        a, b = left.split("+")
        graph[a] = graph.get(a, {})
        graph[a][b] = result
        graph[b] = graph.get(b, {})
        graph[b][a] = result
    
    determined_variables = {}
    explored = {}
    for variable in graph.keys():
        process_connected_component(variable,
                                    determined_variables,
                                    explored,
                                    graph)
    
    Q = int(input())
    for j in range(Q):
        explored = set()
        frontier = []
        
