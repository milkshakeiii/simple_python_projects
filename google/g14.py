
def next_step(current_x, current_y, direction, halt, board):
    top_leanable = current_y == 0 or board[current_y-1][current_x] == "#"
    right_leanable = current_x == len(board)-1 or board[current_y][current_x+1] == "#"
    bottom_leanable = current_y == len(board)-1 or board[current_y+1][current_x] == "#"
    left_leanable = current_x == 0 or board[current_y][current_x-1] == "#"
    leanables = [right_leanable, bottom_leanable, left_leanable, top_leanable]
    differences = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if all(leanables):
        halt = True
        return current_x, current_y, direction, halt

    directions = "ESWN"
    start_direction = directions.index(direction)-1
    for i in range(start_direction, start_direction+4):
        index = i%4
        direction = directions[index]
        if not leanables[index]:
            difference = differences[index]
            current_x += difference[0]
            current_y += difference[1]
            break

    return current_x, current_y, direction, halt
            

T = int(input())
for i in range(T):
    N = int(input())
    board = []
    for j in range(N):
        board.append(input())

    edison_y, edison_x, exit_y, exit_x = map(lambda c: int(c)-1,input().split())

    path = ""
    turns = 0
    halt = False
    direction = "E"
    for _ in range(10001):
        turns += 1
        edison_x, edison_y, direction, halt = next_step(edison_x,
                                                        edison_y,
                                                        direction,
                                                        halt,
                                                        board)
        path += direction
        #print(direction, end="")
        if halt:
            break
        if (edison_x, edison_y) == (exit_x, exit_y):
            break

    print ("Case #" + str(i+1) + ": ", end="")
    if halt or turns == 10001:
        print("Edison ran out of energy.")
    else:
        print(turns)
        print(path)
