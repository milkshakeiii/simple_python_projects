import sys
import math

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]

BOMB = 1
PLAYER = 0
EMPTY_CELL = '.'
BOX = '0'

def explosion_victims(board, square_x, square_y, radius):
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

def contains_box(board, x, y):
    result = False
    if (x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT and board[y][x] == BOX):
        result = True
#    print ((x, y, result))
    return result

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])

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

    def is_bomb(self):
        return self.entity_type == BOMB
    
    def bombs_remaining(self):
        if self.is_player():
            return self.param_1
        else:
            raise TypeError("This is not a player.")

    def is_player(self):
        return self.entity_type == PLAYER

    def is_me(self):
        return self.entity_type == PLAYER and self.owner == MY_ID
    
    def explosion_range(self):
        return self.param_2

    def boxes_within_range(self, board):
        return explosion_victims(board, self.x, self.y, self.explosion_range())

    def distance_to(self, point_b):
        return distance((self.x, self.y), point_b)

def abstract_in_bomb(entity):
    victims = entity.boxes_within_range(board)
    for victim in victims:
        abstracted_board[victim[1]][victim[0]] = EMPTY_CELL
    return abstracted_board

def abstractify_board(board):
    abstracted_board = [row[:] for row in board]
    
    for entity in entities:
        if entity.is_bomb():
            abstracted_board = abstract_in_bomb(entity)

    return abstracted_board

def compute_square_values(board):
    square_values = [row[:] for row in board]

    for i in range(HEIGHT):
        for j in range(WIDTH):
            square_values[i][j] = len(explosion_victims(abstracted_board, j, i, 3))

    return square_values

#unused
def find_maximums(square_values):
    row_maxes = []
    for i in range(HEIGHT):
        row = square_values[i]
        max_value = max(row)
        for j in range(WIDTH):
            cell = row[j]
            if cell == max_value:
                row_maxes.append((max_value, j, i))
    true_max = max(row_maxes)[0]
    true_maxes = []
    for i in range(len(row_maxes)):
        row_max = row_maxes[i]
        if row_max[0] == true_max:
            true_maxes.append(row_max)

    return true_maxes

#square value tuplets come in form (value, x, y)
def squares_by_value(square_values):
    value_squares = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            value_squares.append((square_values[i][j], j, i))
    return value_squares

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
            
    #account for bombs and find the square with the highest value
    abstracted_board = abstractify_board(board)
    square_values = compute_square_values(abstracted_board)
    value_squares = squares_by_value(square_values)
    value_squares.sort(key=lambda maximum: (-maximum[0], me.distance_to((maximum[1], maximum[2]))))
    nearest_maximum = value_squares[0]

    x, y = nearest_maximum[1], nearest_maximum[2]
    if (me.x == x and me.y == y and me.bombs_remaining() > 0):
        
        #account for the bomb i'm about to place to figure out where to go next
        abstracted_board = abstract_in_bomb(Entity([1, 1, x, y, 8, 3]))
        square_values = compute_square_values(abstracted_board)
        value_squares = squares_by_value(square_values)
        value_squares.sort(key=lambda maximum: (-maximum[0], me.distance_to((maximum[1], maximum[2]))))
        next_maximum = value_squares[0]

        print ("BOMB " + str(next_maximum[1]) + " " + str(next_maximum[2]))
    else:
        print ("MOVE " + str(x) + " " + str(y))
