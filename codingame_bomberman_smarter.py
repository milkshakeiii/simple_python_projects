import sys
import math

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]

ITEM = 2
BOMB = 1
PLAYER = 0

EMPTY_CELL = '.'
WALL = 'X'

EMPTY_BOX = 0
EXTRA_RANGE = 1
EXTRA_BOMB = 2

BOMB_MOVE = 0
MOVE_MOVE = 1

def explosion_blockers(board, square_x, square_y, radius):
    box_squares = []
    for x in range(square_x+1, square_x+radius):
        if contains_box(board, x, square_y):
            box_squares.append((x, square_y))
            break
    for x in reversed(range(square_x-radius+1, square_x)):
        if contains_box(board, x, square_y):
            box_squares.append((x, square_y))
            break
    for y in range(square_y+1, square_y+radius):
        if contains_box(board, square_x, y):
            box_squares.append((square_x, y))
            break
    for y in reversed(range(square_y-radius+1, square_y)):
        if contains_box(board, square_x, y):
            box_squares.append((square_x, y))
            break
    return box_squares

def contains_blocker(board, x, y):
    result = False
    if (x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT and board[y][x] != EMPTY_CELL):
        result = True
#    print ((x, y, result))
    return result

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])

class Move():
    def __init__(self, move_type, x, y, player):
        self.move_type = move_type
        self.x = x
        self.y = y
        self.player = player

    def get_string(self):
        move_string = ""
        if self.move_type == MOVE_MOVE:
            move_string += "MOVE "
        else:
            move_string += "BOMB "
        move_string += str(self.x)
        move_string += " "
        move_string += str(self.y)
        return move_string

class Position():
    def __init__(self, board, entities):
        self.board = board
        self.entities = entities

    def do_move(self, player, move):
        return False

class Entity():
    def __init__(self, parameters):
        self.entity_type = parameters[0]
        self.owner = parameters[1]
        self.x = parameters[2]
        self.y = parameters[3]
        self.param_1 = parameters[4]
        self.param_2 = parameters[5]
        
    def countdown(self):
        if self.is_bomb():
            return self.param_1
        else:
            raise TypeError("This is not a bomb.")

    def bombs_remaining(self):
        if self.is_player():
            return self.param_1
        else:
            raise TypeError("This is not a player.")

    def item_type(self):
        if self.is_item():
            return self.param_1
        else:
            raise TypeError("This is not an item.")

    def is_bomb(self):
        return self.entity_type == BOMB

    def is_player(self):
        return self.entity_type == PLAYER

    def is_item(self):
        return self.entity_type == ITEM

    def is_me(self):
        return self.entity_type == PLAYER and self.owner == MY_ID
    
    def explosion_range(self):
        if (self.is_bomb() or self.is_player()):
            return self.param_2
        else:
            raise TypeError("This is not a bomb or player.")

    def blockers_within_range(self, board):
        return explosion_blockers(board, self.x, self.y, self.explosion_range())

    def distance_to(self, point_b):
        return distance((self.x, self.y), point_b)

# game loop
while True:
    board = []
    for i in range(HEIGHT):
        row = list(input())
        board.append(row)
        
    entities_count = int(input())
    entities = []
    for i in range(entities_count):
        parameters = [int(j) for j in input().split()]
        entities.append(Entity(parameters))
    
    me = -1
    for entity in entities:
        if entity.is_me():
            me = entity
            
    print(Move(BOMB_MOVE, 6, 5, MY_ID).get_string())
