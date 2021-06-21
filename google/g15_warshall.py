T = int(input())

for i in range(T):
    N = int(input())
    colors = []
    for j in range(N):
        #room colors
        colors.append(input())
    M = int(input())
    best_paths = {}
    sources = []
    destinations = []
    for j in range(M):
        room1, room2, weight = map(int,input().split())
        color1 = colors[room1-1]
        color2 = colors[room2-1]
        sources.append(color1)
        destinations.append(color2)
        previous_weight = best_paths.get((color1, color2), float('inf'))
        best_paths[(color1, color2)] = min(previous_weight, weight)

    for source in sources:
        for destination in destinations:
            for middle in destinations:
                previous_best_path = best_paths.get((source, destination), float('inf'))
                best_path_through_middle = best_paths.get((source, middle), float('inf')) + best_paths.get((middle, destination), float('inf'))
                best_paths[(source, destination)] = min(previous_best_path, best_path_through_middle)
        
    print("Case #" + str(i+1) + ":")
    S = int(input())
    for j in range(S):
        source_room, destination_room = map(int,input().split())
        source_color = colors[source_room-1]
        destination_color = colors[destination_room-1]
        best_path = best_paths.get((source_color, destination_color), float('inf'))
        if source_color == destination_color:
            best_path = 0 
        print(-1 if best_path == float('inf') else best_path)
        
