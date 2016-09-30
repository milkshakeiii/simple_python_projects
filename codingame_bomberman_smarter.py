import sys
import math

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]

COUNTDOWN = 8

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

def explosion_hits(position, square_x, square_y, radius):
    box_squares = []
    victims = []
    for x in range(square_x+1, square_x+radius):
        victims += contained_victims(position, x, square_y)
        if contains_box(position, x, square_y):
            box_squares.append((x, square_y))
        if contains_blocker(position, x, square_y):
            break
                        
    for x in reversed(range(square_x-radius+1, square_x)):
        victims += contained_victims(position, x, square_y)
        if contains_box(position, x, square_y):
            box_squares.append((x, square_y))
        if contains_blocker(position, x, square_y):
            break
                        
    for y in range(square_y+1, square_y+radius):
        victims += contained_victims(position, square_x, y)
        if contains_box(position, square_x, y):
            box_squares.append((square_x, y))
        if contains_blocker(position, square_x, y):
            break
                        
    for y in reversed(range(square_y-radius+1, square_y)):
        victims += contained_victims(position, square_x, y)
        if contains_box(position, square_x, y):
            box_squares.append((square_x, y))
        if contains_blocker(position, square_x, y):
            break

    return (box_squares, victims)

def contains_wall(postion, x, y):
    return (x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT or postion.board[y][x] == WALL)

def contains_box(position, x, y):
    return (not contains_wall(position, x, y)) and position.board[y][x] != EMPTY_CELL

def contains_blocker(position, x, y):
    non_player_victims = [victim for victim in contained_victims(position, x, y) if not victim.is_any_player()]
    return contains_wall(position, x, y) or contains_box(position, x, y) or len(non_player_victims) > 0

def contains_movement_blocker(position, x, y):
    bombs = [victim for victim in contained_victims(position, x, y) if victim.is_bomb()]
    return contains_wall(position, x, y) or contains_box(position, x, y) or len(bombs) > 0

def contained_victims(position, x, y):
    return [entity for entity in position.entities if entity.x == x and entity.y == y]

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])

class Move():
    def __init__(self, move_type, x, y, player):
        self.move_type = move_type
        self.x = x
        self.y = y
        self.player = player

    def __repr__(self):
        return self.get_string()

    def __gt__(a, b):
        return a.x > b.x

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
        self.player_points = {}
        for entity in entities:
            if entity.is_any_player():
                self.player_points[entity.owner] = 0

    def move_result(self, moves):
        board_copy = [row[:] for row in self.board]
        entities_copy = [entity.copy() for entity in self.entities]
        result = Position(board_copy, entities_copy)

        new_items = []
        cells_to_empty = []
        destroyed_entities = []
        new_bombs = []

        #####################################collect items
        for entity in result.entities:
            if (entity.is_any_player()):
                colocated_entities = [colo for colo in result.entities if colo.x == entity.x and colo.y == entity.y]
                for colocated_entity in colocated_entities:
                    if colocated_entity.is_item():
                        if colocated_entity.item_type() == EXTRA_BOMB:
                            entity.bomb_capacity_upgrade()
                        if colocated_entity.item_type() == EXTRA_RANGE:
                            entity.explosion_range_upgrade()
                        result.entities.remove(colocated_entity)
        
        ####################################do bombs
        for entity in result.entities:
            if entity.is_bomb():
                entity.tick_tock()

        exploding_bombs = [entity for entity in result.entities if (entity.is_bomb() and entity.countdown() == 0)]
        #while there are still bombs left to explode
        while (len(exploding_bombs) != 0):
            bomb = exploding_bombs.pop(0)
            #explode them
            destroyed_entities.append(bomb)
            hits = explosion_hits(result, bomb.x, bomb.y, bomb.explosion_range())
            
            #replace boxes with items on empty cells
            for box_spot in hits[0]:
                x, y = box_spot
                box_type = int(result.board[y][x])
                #award points
                result.player_points[bomb.owner] = result.player_points[bomb.owner] + 1
                cells_to_empty.append((x, y))
                if (box_type != EMPTY_BOX):
                    new_items.append(Entity([ITEM, 0, x, y, box_type, 0]))

            #remove vitims
            for victim in hits[1]:
                if victim.is_bomb() and victim not in exploding_bombs and victim not in destroyed_entities:
                    #or explode victim bombs
                    exploding_bombs.append(victim)
                elif not victim.is_bomb() and victim not in destroyed_entities and not (victim.is_any_player() and victim.owner == bomb.owner):
                    destroyed_entities.append(victim)

                
        ###################################do moves
        movers = [entity for entity in result.entities if entity.is_any_player()]

        for mover in movers:
            player_moves = [move for move in moves if move.player == mover.owner]
            if len(player_moves) == 0:
                raise TypeError("A player had no move given!")

            move = player_moves[0]

            if move.move_type == BOMB_MOVE:
                new_bombs.append(Entity([BOMB, move.player, mover.x, mover.y, COUNTDOWN, mover.explosion_range()]))

            if (not contains_movement_blocker(result, move.x, move.y)):
                mover.x = move.x
                mover.y = move.y

        ###################################clean up
        for item in new_items:
            result.entities.append(item)

        for cell in cells_to_empty:
            result.board[cell[1]][cell[0]] = EMPTY_CELL

        for entity in destroyed_entities:
            result.entities.remove(entity)
            if (entity.is_bomb()):
                player = [entity for entity in result.entities if entity.is_player(entity.owner)][0]
                player.bomb_ready()

        for bomb in new_bombs:
            player = [entity for entity in result.entities if entity.is_player(bomb.owner)][0]
            player.bomb_used()
            result.entities.append(bomb)
            
        return result

    def display(self):
        display_board = [row[:] for row in self.board]
        for entity in self.entities:
            if entity.is_any_player():
                display_board[entity.y][entity.x] = '@'
            if entity.is_bomb():
                display_board[entity.y][entity.x] = '!'
            if entity.is_item():
                display_board[entity.y][entity.x] = '#'
        for row in display_board:
            print(row)

    def evaluate(self):
        my_players = [entity for entity in self.entities if entity.is_me()]
        if len(my_players) == 0:
            return float('-inf')
        all_players = [entity for entity in self.entities if entity.is_any_player()]
        if len(all_players) == 1:
            return float('inf')

        return self.player_points[MY_ID]
        

class Entity():
    def __init__(self, parameters):
        self.entity_type = parameters[0]
        self.owner = parameters[1]
        self.x = parameters[2]
        self.y = parameters[3]
        self.param_1 = parameters[4]
        self.param_2 = parameters[5]
        if self.is_any_player():
            self.bomb_capacity = self.param_1

    def copy(self):
        copy = Entity([self.entity_type, self.owner, self.x, self.y, self.param_1, self.param_2])
        if copy.is_any_player():
            copy.bomb_capacity = self.bomb_capacity
        return copy
        
    def countdown(self):
        if self.is_bomb():
            return self.param_1
        else:
            raise TypeError("This is not a bomb.")

    def tick_tock(self):
        if self.is_bomb():
            self.param_1 -= 1
        else:
            raise TypeError("This is not a bomb.")

    def zero_countdown(self):
        if self.is_bomb():
            self.param_1 = 0
        else:
            raise TypeError("This is not a bomb.")

    def bombs_remaining(self):
        if self.is_any_player():
            return self.param_1
        else:
            raise TypeError("This is not a player.")

    def bomb_ready(self):
        if (self.is_any_player()):
            self.param_1 += 1
        else:
            raise TypeError("This is not a player.")    

    def bomb_used(self):
        if (self.is_any_player()):
            self.param_1 -= 1
        else:
            raise TypeError("This is not a player.")    


    def bomb_capacity_upgrade(self):
        if (self.is_any_player()):
            self.param_1 += 1
            self.bomb_capacity += 1
        else:
            raise TypeError("This is not a player.")        

    def explosion_range(self):
        if (self.is_bomb() or self.is_any_player()):
            return self.param_2
        else:
            raise TypeError("This is not a bomb or player.")

    def explosion_range_upgrade(self):
        if (self.is_any_player()):
            self.param_2 += 1
        else:
            raise TypeError("This is not a player.")

    def item_type(self):
        if self.is_item():
            return self.param_1
        else:
            raise TypeError("This is not an item.")

    def is_bomb(self):
        return self.entity_type == BOMB

    def is_player(self, player_id):
        return self.is_any_player() and self.owner == player_id

    def is_any_player(self):
        return self.entity_type == PLAYER

    def is_item(self):
        return self.entity_type == ITEM

    def is_me(self):
        return self.is_player(MY_ID)

    def explosion_victims(self, board):
        return explosion_blockers(board, self.x, self.y, self.explosion_range())

    def distance_to(self, point_b):
        return distance((self.x, self.y), point_b)

def possible_moves_for_player(position, player):
    possible_moves = []
    for direction in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        target = (player.x+direction[0], player.y+direction[1])
        if not contains_movement_blocker(position, target[0], target[1]):
            possible_moves.append(Move(MOVE_MOVE, target[0], target[1], player.owner))
            if (player.bombs_remaining() > 0):
                possible_moves.append(Move(BOMB_MOVE, target[0], target[1], player.owner))
    if len(possible_moves) == 0:
        possible_moves.append(Move(MOVE_MOVE, player.x, player.y, player.owner))
    return possible_moves

def possible_moves(position):
    me = [entity for entity in position.entities if entity.is_me()][0]
    my_possible_moves = possible_moves_for_player(position, me)
    
    them = [entity for entity in position.entities if (not entity.is_me()) and entity.is_any_player()][0]
    their_possible_moves = possible_moves_for_player(positon, them)

    possible_moves = {}
    for move in my_possible_moves:
        possible_moves[move] = their_possible_moves

    return possible_moves
    
#returns (evaluation, move)
def minimax(position, depth):
    
    evaluation = position.evaluate()
    if depth == 0 or evaluation == float('-inf') or evaluation == float('inf'):
        return (evaluation, None)

    my_move_evaluations = []
    these_possible_moves = possible_moves(position)
    for my_move in these_possible_moves.keys():
        their_moves = these_possible_moves[my_move]
        evaluations = []
        for their_move in their_moves:
            result_position = position.move_result([my_move] + [their_move])
            evaluations.append(minimax(result_position, depth-1)[0])
        my_move_evaluations.append((min(evaluations), my_move))
    my_best_move = max(my_move_evaluations)
    return my_best_move

def maximax(position, depth):
    evaluation = position.evaluate()
    if depth == 0 or evaluation == float('-inf') or evaluation == float('inf'):
        return (evaluation, None)

    my_move_evaluations = []
    me = [entity for entity in position.entities if entity.is_me()][0]
    them = [entity for entity in position.entities if (not entity.is_me()) and entity.is_any_player()][0]
    my_possible_moves = possible_moves_for_player(position, me)
    evaluations = []
    for my_move in my_possible_moves:
        result_position = position.move_result([my_move] + [Move(MOVE_MOVE, them.x, them.y, them.owner)])
        evaluations.append((maximax(result_position, depth-1)[0], my_move))
    my_best_move = max(evaluations)
    return my_best_move

    

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


    position = Position(board, entities)

            
    print(maximax(position, 9)[1].get_string())

