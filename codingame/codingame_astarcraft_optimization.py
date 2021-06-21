import sys
import math
import time
import random

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

def run_robot(lines, x, y, direction, output, debug=False):
    modded_lines = [line for line in lines]
    output_list = output[:-1].split(' ')
    ax = -1
    ay = -1
    for i in range(len(output_list)):
        entry = output_list[i]
        if i%3==0:
            ax = int(entry)
        elif i%3==1:
            ay = int(entry)
        elif i%3==2:
            if (modded_lines[ay][ax] == "."):
                modded_lines[ay] = modded_lines[ay][:ax] + entry + modded_lines[ay][ax+1:]
    
    if modded_lines[y][x] in ["U", "D", "L", "R"]:
        direction = direction_tuple(modded_lines[y][x])
    robot_future = [((x, y), direction)]
    history_dict = {}
    history_dict[(x, y)] = [direction]
    while True:
        current_spot = robot_future[-1][0]
        x = current_spot[0]
        y = current_spot[1]
        next_spot = add_spot(current_spot, direction)
        nx = next_spot[0]
        ny = next_spot[1]

        if get_mod_lines(modded_lines, nx, ny) in ["U", "D", "L", "R"]:
            direction = direction_tuple(get_mod_lines(modded_lines, nx, ny))
        if get_mod_lines(modded_lines, nx, ny) == "#" or direction in history_dict.get((nx, ny), []):
            break
        
        next_heading = next_spot, direction
        robot_future = robot_future + [next_heading]
        history_dict[next_spot] = history_dict.get(next_spot, []) + [direction]
    if debug:
        print(robot_future, file=sys.stderr)
    return len(robot_future)

def run_robots(lines, robots, output, debug=False):
    score = 0
    for robot in robots:
        score = score + run_robot(lines, robot[0], robot[1], robot[2], output, debug=debug)
    return score

def make_random_output(max_arrows, lines):
    random_output = ""
    random_arrow_count = random.randint(1, max_arrows)
    random_xs = [random.randint(0, 18) for i in range(random_arrow_count)]
    random_ys = [random.randint(0, 9) for i in range(random_arrow_count)]
    random_directions = [["U", "D", "L", "R"][random.randint(0, 3)] for i in range(random_arrow_count)]
    for i in range(random_arrow_count):
        if lines[random_ys[i]][random_xs[i]] == ".":
            random_output = random_output + str(random_xs[i]) + " " + str(random_ys[i]) + " " + random_directions[i] + " "
    return random_output
    
def mutate_output(output, lines):
    split_output = output.split(' ')[:-1]
    mutated_output = ""
    for i in range(len(split_output)):
        if i%3 == 0:
            mutated_output = mutated_output + str((int(split_output[i]) + random.randint(-1, 1))%19) + " "
        elif i%3 == 1:
            mutated_output = mutated_output + str((int(split_output[i]) + random.randint(-1, 1))%10) + " "
        else:
            mutated_output = mutated_output + split_output[i] + " "
            
    arrow_change = random.randint(-1, 1) if len(mutated_output)>8 else random.randint(0, 1)
    if arrow_change == -1:
        return ' '.join(mutated_output.split(' ')[:-4]) + " "
    elif arrow_change == 0:
        return mutated_output
    else:
        return mutated_output + make_random_output(1, lines)

tick = 0
def P(score, max_score, time_elapsed):
    global tick
    threshhold = (10*(0.9-time_elapsed)/0.9)
    tick = tick + 1
    #if (tick%200 == 0):
    #    print(threshhold, file=sys.stderr)
    if score > max_score - threshhold:
        return True

lines = []
for i in range(10):
    line = input()
    lines.append(line)
    
robot_count = int(input())
robots = []
for i in range(robot_count):
    x, y, direction = input().split()
    x = int(x)
    y = int(y)
    direction = direction_tuple(direction)
    robots.append((x, y, direction))

start_time = time.time()
acc_score = 0
acc_output = ""
max_score = 0
max_output = ""
fixed_output = ""
iters = 0
random_output = make_random_output(1, lines)
while (time.time() - start_time < 0.9):
    iters = iters + 1
    random_output = fixed_output + make_random_output(1, lines)
    if len(random_output) == 0:
        random_output = "0 0 D "
    score = run_robots(lines, robots, random_output)
    if score > acc_score:
        acc_score = score
        acc_output = random_output
        fixed_output = acc_output
    if score > max_score:
        max_output = random_output
        max_score = score
        print(str(max_score) + ": " + max_output, file=sys.stderr)
    

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print("iterations: " + str(iters), file=sys.stderr)
print("max score: " + str(max_score), file=sys.stderr)
#print("predicted score: " + str(run_robots(lines, robots, max_output, debug=True)), file=sys.stderr)
#print(max_output, file=sys.stderr)
#print(mutate_output(max_output), file=sys.stderr)
print(max_output)
