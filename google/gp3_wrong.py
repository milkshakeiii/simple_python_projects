T = int(input())

def do_topological_sort(current, edges, sort, explored):
    if current in explored:
        return
    sort.append(current)
    explored.add(current)
    for child in edges.get(current, []):
        do_topological_sort(child, edges, sort, explored)

def do_connected_components(current, root, edges, components, explored):
    if current in explored:
        return
    components[root] = components.get(root, []) + [current]
    explored.add(current)
    for child in edges.get(current, []):
        do_connected_components(child, root, edges, components, explored)

for i in range(T):
    M = int(input())
    pairs = {}
    backwards_pairs = {}
    for j in range(M):
        pair = input().split()
        pairs[pair[0]] = pairs.get(pair[0], []) + [pair[1]]
        backwards_pairs[pair[1]] = backwards_pairs.get(pair[1], []) + [pair[0]]
    topological_sort = []
    already_sorted = set()
    for pair in pairs.keys():
        do_topological_sort(pair,
                            pairs,
                            topological_sort,
                            already_sorted)
    connected_components = {}
    already_connected = set()
    for node in topological_sort:
        do_connected_components(node,
                                node,
                                backwards_pairs,
                                connected_components,
                                already_connected)
    component_lengths = [len(component) for component in connected_components.values()]
    splitable = all([length==1 or length%2==0 for length in component_lengths])
    print("Yes" if splitable else "No")
        
