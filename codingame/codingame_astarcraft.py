import sys
import math

def direction_tuple(direction):
    if direction == "R":
        return (1, 0)
    if direction == "L":
        return (-1, 0)
    if direction == "U":
        return (0, -1)
    if direction == "D":
        return (0, 1)
        
def add_spot(spot1, spot2):
    x = (spot1[0]+spot2[0])%19
    y = (spot1[1]+spot2[1])%10
    return (x, y)

def get_mod_lines(lines, x, y):
    return lines[y%10][x%19]

lines = []
for i in range(10):
    line = input()
    lines.append(line)
    
output = ""
robot_count = int(input())
for i in range(robot_count):
    x, y, direction = input().split()
    x = int(x)
    y = int(y)
    direction = direction_tuple(direction)
    
    robot_future = [((x, y), direction)]
    while True:
        current_spot = robot_future[-1][0]
        x = current_spot[0]
        y = current_spot[1]
        next_spot = add_spot(current_spot, direction)
        nx = next_spot[0]
        ny = next_spot[1]
        
        if get_mod_lines(lines, nx, ny) == "#":
            if lines[y][x] != ".":
                break
            for tryy in ["R", "L", "D", "U"]:
                possible_next = add_spot(current_spot, direction_tuple(tryy))
                px = possible_next[0]
                py = possible_next[1]
                if (lines[py][px] != "#"):
                    output = output + str(x) + " " + str(y) + " " + tryy + " "
                    direction = direction_tuple(tryy)
                    lines[y] = lines[y][:x] + tryy + lines[y][x+1:]
                    break
        elif get_mod_lines(lines, nx, ny) == ".":
            pass
        elif get_mod_lines(lines, nx, ny) in ["U", "D", "L", "R"]:
            direction = direction_tuple(get_mod_lines(lines, nx, ny))
        
        next_heading = add_spot(current_spot, direction), direction
        if next_heading in robot_future:
            break
        robot_future = robot_future + [next_heading]
    

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(output)
