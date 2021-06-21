import sys
import math



def reachable_neighbors(board, x, y, z, h, w):
    #(x, y), is_vertical
    neighbors = [((x+1, y), False),
                 ((x-1, y), False),
                 ((x, y+1), True),
                 ((x, y-1), True)]
    legal_transition = {'.': ['.', '|', '-', 'X'],
                        '+': ['+', '|', '-', 'X'],
                        '|': ['.', '+', '-', 'X'],
                        '-': ['.', '+', '|', 'X'],
                        'X': ['+', '.', '-', '|']}
    reachable_neighbors = []
    
    #returns (is_reachable, reachable_coords)
    def reachable_and_coords(neighbor):
        if x >= w or x < 0 or y >= w or y < 0:
            return (False, None)
        
        is_vertical = neighbor[1]
        nx, ny = neighbor[0]
        source_char = board[y][x]
        target_char = board[ny][nx]
        nz = 0
        if target_char == '+':
            nz = 1
        if target_char == 'X':
            nz = z
        if target_char not in legal_transition[source_char]:
            return (False, None)
        if is_vertical and (target_char == '-' or source_char == '-'):
            return (False, None)
        if not is_vertical and (target_char == '|' or source_char == '|'):
            return (False, None)
        if source_char == 'X' and nz != z:
            return (False, None)
        
        return (True, (nx, ny, nz))
        
    
    for neighbor in neighbors:
        reachable = reachable_and_coords(neighbor)
        reachable_neighbor = reachable[1]
        is_reachable = reachable[0]
        
        if (is_reachable):
            reachable_neighbors.append(reachable_neighbor)
            
    return reachable_neighbors
    
    
    


def bfs(board, startx, starty, endx, endy, h, w):
    #(x, y, z), depth
    frontier = [((startx, starty, 0), 0)]
    explored_squares = [[[False for i in range(w)] for i in range(h)] for i in range(2)]
    explored_squares[0][starty][startx] = True

    while len(frontier) != 0:
        current = frontier.pop(0)
        x, y, z = current[0]
        depth = current[1]
        if (x, y, z) == (endx, endy, 0):
            return depth
        for neighbor in reachable_neighbors(board, x, y, z, h, w):
            nx, ny, nz = neighbor
            if not explored_squares[nz][ny][nx]:
                explored_squares[nz][ny][nx] = True
                frontier.append((neighbor, depth+1))
        


        



starty, startx = [int(i) for i in input().split()]
endy, endx = [int(i) for i in input().split()]
h, w = [int(i) for i in input().split()]

board = []

for i in range(h):
    line = input()
    board.append(line)
    print(line, file=sys.stderr)



print(bfs(board, startx, starty, endx, endy, h, w))
