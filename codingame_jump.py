import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def triangular_number(n):
    return sum(range(1, n+1))
def nearest_lower_triangular_number(after_me):
    nth_triangle = 0
    while triangular_number(nth_triangle) <= after_me:
        nth_triangle += 1
    return nth_triangle-1

road = int(input())  # the length of the road before the gap.
gap = int(input())  # the length of the gap.
platform = int(input())  # the length of the landing platform.
start_speed = int(input())  # the motorbike's speed.
start_coord_x = int(input())  # the position on the road of the motorbike.

min_jump_speed = gap+1
max_jump_speed = nearest_lower_triangular_number(platform)

needed_runway = triangular_number(jump_speed)
print(jump_speed, file=sys.stderr)
print(needed_runway, file=sys.stderr)
print("SPEED")
for i in range(road-needed_runway-1):
    print("WAIT")

for i in range(jump_speed-1):
    print("SPEED")

print("JUMP")
    
for i in range(jump_speed):
    print("SLOW")
