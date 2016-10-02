import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

boost_used = False
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    print(next_checkpoint_dist, file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    thrust = 50
    if abs(next_checkpoint_angle) > 90:
        thrust = "0"
    elif not boost_used and next_checkpoint_dist > 6000 and abs(next_checkpoint_angle) < 10:
        thrust = "BOOST"
        boost_used = True
    elif next_checkpoint_dist > 3000:
        thrust = "100"
    else:
        print (next_checkpoint_angle, file=sys.stderr)
        print (int(100* (next_checkpoint_angle / 90)), file=sys.stderr)
        thrust = str(max(0, 100-int(100* (next_checkpoint_angle**2 / 90**2))))
    

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + thrust)
