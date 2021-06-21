import sys
import math
from dataclasses import dataclass


@dataclass
class Tree:
    cell_index: int
    size: int
    is_dormant: bool


def harvest_value(tree: Tree, nutrients: int) -> int:
    bonus = 0
    if tree.cell_index <= 6:
        bonus = 6
    if tree.cell_index <= 18:
        bonus = 4
    if tree.cell_index <= 36:
        bonus = 2
    return nutrients + bonus


def action(my_trees: list, nutrients: int) -> str:
    # GROW cellIdx | SEED sourceIdx targetIdx | COMPLETE cellIdx | WAIT <message>
    if len(my_trees) > 0:
        best_tree = min(my_trees, key=lambda tree: tree.cell_index)
        if (best_tree.size == 3 and harvest_value(best_tree, nutrients)) > 4:
            return "COMPLETE " + str(best_tree.cell_index)
        elif (best_tree.size < 3):
            return "GROW " + str(best_tree.cell_index)
    return "WAIT"


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_of_cells = int(input())  # 37
for i in range(number_of_cells):
    # index: 0 is the center cell, the next cells spiral outwards
    # richness: 0 if the cell is unusable, 1-3 for usable cells
    # neigh_0: the index of the neighbouring cell for each direction
    index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]

# game loop
while True:
    day = int(input())  # the game lasts 24 days: 0-23
    nutrients = int(input())  # the base score you gain from the next COMPLETE action
    # sun: your sun points
    # score: your current score
    sun, score = [int(i) for i in input().split()]
    inputs = input().split()
    opp_sun = int(inputs[0])  # opponent's sun points
    opp_score = int(inputs[1])  # opponent's score
    opp_is_waiting = inputs[2] != "0"  # whether your opponent is asleep until the next day
    number_of_trees = int(input())  # the current amount of trees
    my_trees = []
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])  # location of this tree
        size = int(inputs[1])  # size of this tree: 0-3
        is_mine = inputs[2] != "0"  # 1 if this is your tree
        is_dormant = inputs[3] != "0"  # 1 if this tree is dormant
        if is_mine:
            my_trees.append(Tree(cell_index, size, is_dormant))
    number_of_possible_moves = int(input())
    for i in range(number_of_possible_moves):
        possible_move = input()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print(action(my_trees, nutrients))
        
