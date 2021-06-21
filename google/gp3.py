def paint_graph_two_colors(current, children, color_a, color_b, depth):
    color = depth%2 == 0
    #print(depth, current)
    if (current in color_a and not color) or (current in color_b and color):
        #print("conflict with " + current)
        return False
    if (current in color_a and color) or (current in color_b and not color):
        return True
    if color:
        #print(current + " goes into group a")
        color_a.add(current)
    else:
        #print(current + " goes into group b")
        color_b.add(current)
    child_results = []
    for child in children.get(current, []):
        result = paint_graph_two_colors(child,
                                        children,
                                        color_a,
                                        color_b,
                                        depth+1)
        child_results.append(result)
    return all(child_results)
        
T = int(input())

for i in range(T):
    M = int(input())
    children = {}
    for j in range(M):
        pair = input().split()
        children[pair[0]] = children.get(pair[0], set()).union(set([pair[1]]))
        children[pair[1]] = children.get(pair[1], set()).union(set([pair[0]]))
    cycle_lengths = []
    group_a = set()
    group_b = set()
    splitable = True
    for node in children.keys():
        if node in group_a or node in group_b:
            continue
        splitable = splitable and paint_graph_two_colors(node,
                                                         children,
                                                         group_a,
                                                         group_b,
                                                         0)

    answer = "Yes" if splitable else "No"
    print("Case #" + str(i+1) + ": " + answer)
