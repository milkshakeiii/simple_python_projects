import sys
import math
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Set

# Save humans, destroy zombies!
BOARD_WIDTH = 16000
BOARD_HEIGHT = 9000

Point = namedtuple('Point', ['x', 'y'])

@dataclass
class Turn:
    target: Point

@dataclass
class Gamestate:
    ash_position: Point = Point(0, 0)
    zombie_positions: List[Point] = field(default_factory=list)
    human_positions: Set[Point] = field(default_factory=set)
    points: int = 0


fibonacci_numbers = [
    0,
    1,
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    34,
    55,
    89,
    144,
    233,
    377,
    610,
    987,
    1597,
    2584,
    4181,
    6765,
    10946,
    17711,
    28657,
    46368,
    75025,
    121393,
    196418,
    317811,
    514229,
    832040,
    1346269,
    2178309,
    3524578,
    5702887,
    9227465,
    14930352,
    24157817,
    39088169,
    63245986,
    102334155,
    165580141,
    267914296,
    433494437,
    701408733,
    1134903170,
    1836311903,
    2971215073,
    4807526976,
    7778742049,
    12586269025,
    20365011074,
    32951280099,
    53316291173,
    86267571272,
    139583862445,
    225851433717,
    365435296162,
    591286729879,
    956722026041,
    1548008755920,
    2504730781961,
    4052739537881,
    6557470319842,
    10610209857723,
    17167680177565,
    27777890035288,
    44945570212853,
    72723460248141,
    117669030460994,
    190392490709135,
    308061521170129,
    498454011879264,
    806515533049393,
    1304969544928657,
    2111485077978050,
    3416454622906707,
    5527939700884757,
    8944394323791464,
    14472334024676221,
    23416728348467685,
    37889062373143906,
    61305790721611591,
    99194853094755497,
    160500643816367088,
    259695496911122585,
    420196140727489673,
    679891637638612258,
    1100087778366101931,
    1779979416004714189,
    2880067194370816120,
    4660046610375530309,
    7540113804746346429,
    12200160415121876738,
    19740274219868223167,
    31940434634990099905,
    51680708854858323072,
    83621143489848422977,
    135301852344706746049,
    218922995834555169026,
    354224848179261915075,
]
def fibonacci(n):
    return fibonacci_numbers[n]

def square_distance(a, b):
    return (a.x-b.x)**2 + (a.y-b.y)**2

def nearest_neighbor(query, positions):
    best_neighbor = None
    best_square_distance = float('inf')
    for this_position in positions:
        this_square_distance = square_distance(query, this_position)
        if this_square_distance < best_square_distance:
            best_neighbor = this_position
            best_square_distance = this_square_distance
    return best_neighbor

def advanced_toward(advancer, target, advance_distance):
    square_difference = square_distance(advancer, target)
    if (square_difference < advance_distance**2):
        return target

    difference_vector = Point(target.x-advancer.x, target.y-advancer.y)
    magnitude = math.sqrt(difference_vector.x**2 + difference_vector.y**2)
    result = Point(advancer.x + advance_distance*difference_vector.x/magnitude,
                   advancer.y + advance_distance*difference_vector.y/magnitude)
    return Point(math.floor(result.x), math.floor(result.y))

def points_for_zombie_kill(kill_number, humans_count):
    return (humans_count**2)*10*fibonacci(kill_number+2)

def advanced_gamestate(gamestate: Gamestate, turn: Turn):
    next_gamestate = Gamestate(points = gamestate.points)
    
    #advance zombies
    advanced_zombies = []
    gamestate.human_positions.add(gamestate.ash_position)
    for zombie_position in gamestate.zombie_positions:
        nearest_human = nearest_neighbor(zombie_position, gamestate.human_positions)
        advanced_zombies.append(advanced_toward(zombie_position, nearest_human, 400))
    gamestate.human_positions.remove(gamestate.ash_position)
    next_gamestate.zombie_positions = advanced_zombies

    #advance ash
    next_gamestate.ash_position = advanced_toward(gamestate.ash_position, turn.target, 1000)

    #shoot zombies
    surviving_zombies = []
    zombies_killed = 0
    for zombie_position in gamestate.zombie_positions:
        if square_distance(zombie_position, gamestate.ash_position) > 2000**2:
            surviving_zombies.append(zombie_position)
        else:
            zombies_killed += 1
            next_gamestate.points += points_for_zombie_kill(zombies_killed,
                                                       len(gamestate.human_positions))
    next_gamestate.zombie_positions = surviving_zombies

    #eat humans
    living_humans = gamestate.human_positions.copy()
    for zombie_position in gamestate.zombie_positions:
        if zombie_position in gamestate.human_positions:
            living_humans.remove(zombie_position)
    next_gamestate.human_positions = living_humans

    if len(living_humans) == 0:
        next_gamestate.points = 0

    return next_gamestate

    
    


# game loop
next_gamestate = None
while True:
    current_gamestate = Gamestate()
    
    x, y = [int(i) for i in input().split()]
    current_gamestate.ash_position = Point(x, y)
    
    human_count = int(input())
    human_positions = set()
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        human_positions.add(Point(human_x, human_y))
    current_gamestate.human_positions = human_positions
    
    zombie_count = int(input())
    zombie_positions = []
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombie_positions.append(Point(zombie_x, zombie_y))
    current_gamestate.zombie_positions = zombie_positions

    if next_gamestate and next_gamestate != current_gamestate:
        print(next_gamestate, current_gamestate)
        dog
    target = Point(human_x, human_y)
    next_gamestate = advanced_gamestate(current_gamestate, Turn(target=target))
    
    print(human_x, human_y)
