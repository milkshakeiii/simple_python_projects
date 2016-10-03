import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def distance(a, b):
    da = a[0]-b[0]
    db = a[1]-b[1]
    d = math.sqrt(da**2 + db**2)
    return d

boost_used = False
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    print(distance((x, y), (opponent_x, opponent_y)), file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    thrust = -1
    if abs(next_checkpoint_angle) > 90:
        thrust = "0"
    elif not boost_used and next_checkpoint_dist > 6000 and abs(next_checkpoint_angle) < 10:
        thrust = "BOOST"
        boost_used = True
    else:
        thrust = "100"

    move_string = str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + thrust
    

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print()
