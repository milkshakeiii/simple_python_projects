import sys
import math
import heapq
import time

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]

COUNTDOWN = 8

ITEM = 2
BOMB = 1
PLAYER = 0

EMPTY_CELL = '.'
WALL = 'X'
DEATH_CELL = 'Z'
DEATH_CELL_WAS_BOX0 = 'z'
DEATH_CELL_WAS_BOX1 = 'Y'
DEATH_CELL_WAS_BOX2 = 'y'
DEATH_CELLS = [DEATH_CELL, DEATH_CELL_WAS_BOX0, DEATH_CELL_WAS_BOX1, DEATH_CELL_WAS_BOX2]

EMPTY_BOX = 0
EXTRA_RANGE = 1
EXTRA_BOMB = 2

BOMB_MOVE = 0
MOVE_MOVE = 1

def explosion_hits(position, square_x, square_y, radius):
    box_squares = []
    victims = []
    death_squares = [(square_x, square_y)]
    for x in range(square_x+1, square_x+radius):
        victims += contained_victims(position, x, square_y)
        if not contains_wall(position, x, square_y):
            death_squares.append((x, square_y))
        if contains_box(position, x, square_y):
            box_squares.append((x, square_y))
        if contains_blocker(position, x, square_y):
            break
                        
    for x in reversed(range(square_x-radius+1, square_x)):
        victims += contained_victims(position, x, square_y)
        if not contains_wall(position, x, square_y):
            death_squares.append((x, square_y))
        if contains_box(position, x, square_y):
            box_squares.append((x, square_y))
        if contains_blocker(position, x, square_y):
            break
                        
    for y in range(square_y+1, square_y+radius):
        victims += contained_victims(position, square_x, y)
        if not contains_wall(position, square_x, y):
            death_squares.append((square_x, y))
        if contains_box(position, square_x, y):
            box_squares.append((square_x, y))
        if contains_blocker(position, square_x, y):
            break
        
    for y in reversed(range(square_y-radius+1, square_y)):
        victims += contained_victims(position, square_x, y)
        if not contains_wall(position, square_x, y):
            death_squares.append((square_x, y))
        if contains_box(position, square_x, y):
            box_squares.append((square_x, y))
        if contains_blocker(position, square_x, y):
            break

    return (box_squares, victims, death_squares)

def contains_wall(postion, x, y):
    return (x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT or postion.board[y][x] == WALL or postion.board[y][x] in DEATH_CELLS)

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

def open_bordering_squares(position, x, y):
    result = []
    for direction in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
        if not contains_movement_blocker(position, x+direction[0], y+direction[1]):
            result.append((x+direction[0], y+direction[1]))
    return result

def open_squares(position, x, y):
    if (contains_movement_blocker(position, x, y)):
        return []
    result = []
    frontier = []
    frontier.append((x, y))
    while len(frontier) != 0:
        current = frontier.pop(0)
        result.append(current)
        for neighbor in open_bordering_squares(position, current[0], current[1]):
            if not neighbor in result and (not neighbor in frontier):
                frontier.append(neighbor)
    return result

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
        
        self.explosion_board = [[False for cell in row] for row in self.board]
        


    def move_result(self, moves, skip_tick = False):
        
        board_copy = [row[:] for row in self.board]
        entities_copy = [entity.copy() for entity in self.entities]
        result = Position(board_copy, entities_copy)

        new_items = []
        cells_to_empty = []
        destroyed_entities = []
        new_bombs = []

        #clean up death cells
        for i in range(len(result.board)):
            row = result.board[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == DEATH_CELL:
                    result.board[i][j] = EMPTY_CELL
                if cell == DEATH_CELL_WAS_BOX0:
                    result.board[i][j] = EMPTY_BOX
                if cell == DEATH_CELL_WAS_BOX1:
                    result.board[i][j] = EXTRA_RANGE
                if cell == DEATH_CELL_WAS_BOX2:
                    result.board[i][j] = EXTRA_BOMB

        

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
            if entity.is_bomb() and not skip_tick:
                entity.tick_tock()

        #mark no-entry death squares and elimination explosion squares
        result.mark_death_squares()
        result.mark_explosions()

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
                if bomb.owner in result.player_points:
                    result.player_points[bomb.owner] = result.player_points[bomb.owner] + 1
                cells_to_empty.append((x, y))
                if (box_type != EMPTY_BOX):
                    new_items.append(Entity([ITEM, 0, x, y, box_type, 0]))

            #remove vitims
            for victim in hits[1]:
                if victim.is_bomb() and victim not in exploding_bombs and victim not in destroyed_entities:
                    #or explode victim bombs
                    exploding_bombs.append(victim)
                elif not victim.is_bomb() and victim not in destroyed_entities:
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
                players = [entity for entity in result.entities if entity.is_player(entity.owner)]
                if (len(players) > 0):
                    player = players[0]
                    player.bomb_ready()

        for bomb in new_bombs:
            players = [entity for entity in result.entities if entity.is_player(bomb.owner)]
            if len(players) > 0:
                player = players[0]
                player.bomb_used()
            result.entities.append(bomb)


        
        return result

    def mark_death_squares(self):
        cells_to_death = []
        
        almost_exploding_bombs = [entity for entity in self.entities if (entity.is_bomb() and entity.countdown() == 2)]
        hypothetically_destroyed_entities = []
        while (len(almost_exploding_bombs) != 0):
            bomb = almost_exploding_bombs.pop(0)
            hypothetically_destroyed_entities.append(bomb)
            hits = explosion_hits(self, bomb.x, bomb.y, bomb.explosion_range())
            
            for victim in hits[1]:
                if victim.is_bomb() and victim not in almost_exploding_bombs and victim not in hypothetically_destroyed_entities:
                    #hypothetically explode victim bombs
                    almost_exploding_bombs.append(victim)
                elif not victim.is_bomb() and victim not in hypothetically_destroyed_entities:
                    hypothetically_destroyed_entities.append(victim)

            #mark death squares
            for death_square in hits[2]:
                cells_to_death.append(death_square)

        for cell in cells_to_death:
            if cell == EMPTY_CELL:
                self.board[cell[1]][cell[0]] = DEATH_CELL
            if cell == EMPTY_BOX:
                self.board[cell[1]][cell[0]] = DEATH_CELL_WAS_BOX0
            if cell == EXTRA_RANGE:
                self.board[cell[1]][cell[0]] = DEATH_CELL_WAS_BOX1
            if cell == EXTRA_BOMB:
                self.board[cell[1]][cell[0]] = DEAHT_CELL_WAS_BOX2

    def mark_explosions(self):
        cells_to_explode = []
        
        exploding_bombs = [entity for entity in self.entities if (entity.is_bomb() and entity.countdown() == 1)]
        destroyed_entities = []
        while (len(exploding_bombs) != 0):
            bomb = exploding_bombs.pop(0)
            destroyed_entities.append(bomb)
            hits = explosion_hits(self, bomb.x, bomb.y, bomb.explosion_range())
            
            for victim in hits[1]:
                if victim.is_bomb() and victim not in exploding_bombs and victim not in destroyed_entities:
                    exploding_bombs.append(victim)
                elif not victim.is_bomb() and victim not in destroyed_entities:
                    destroyed_entities.append(victim)

            #mark death squares
            for death_square in hits[2]:
                cells_to_explode.append(death_square)

        for cell in cells_to_explode:
            self.explosion_board[cell[1]][cell[0]] = True

            

    def display(self):
        display_board = [row[:] for row in self.board]
        for entity in self.entities:
            if entity.is_any_player():
                display_board[entity.y][entity.x] = '@'
            if entity.is_bomb():
                display_board[entity.y][entity.x] = '!'
            if entity.is_item():
                display_board[entity.y][entity.x] = '#'
        for i in range(len(self.explosion_board)):
            row = self.explosion_board[i]
            for j in range(len(row)):
                if (row[j]):
                    display_board[i][j] = '%'
                
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

    def distance_to(self, point_b):
        return distance((self.x, self.y), point_b)

def abstract_in_bomb(position, entity):
    hits = explosion_hits(position, entity.x, entity.y, entity.explosion_range())
    hits = hits[0] + [(item.x, item.y) for item in hits[1]]
    for hit in hits:
        position.board[hit[1]][hit[0]] = EMPTY_CELL
    return position

def abstractified_position(position):
    board_copy = [row[:] for row in position.board]
    entities_copy = [entity.copy() for entity in position.entities]
    result = Position(board_copy, entities_copy)
    
    for entity in result.entities:
        if entity.is_bomb():
            abstract_in_bomb(result, entity)

    return result

def compute_square_values(position, squares):
    square_values = [[-1 for i in range(WIDTH)] for i in range(HEIGHT)]

    for (x, y) in squares:
        square_values[y][x] = len(explosion_hits(position, x, y, me.explosion_range())[0])

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
    their_possible_moves = possible_moves_for_player(position, them)

    possible_moves = {}
    for move in my_possible_moves:
        possible_moves[move] = their_possible_moves

    return possible_moves
    
#returns (evaluation, move, critical bool)
def minimax(position, depth):
    
    evaluation = position.evaluate()
    end_state = (evaluation == float('-inf') or evaluation == float('inf'))
    if depth == 0 or end_state:
        return (evaluation, None, end_state)

    my_move_evaluations = []
    these_possible_moves = possible_moves(position)
    for my_move in these_possible_moves.keys():
        their_moves = these_possible_moves[my_move]
        evaluations = []
        for their_move in their_moves:
            result_position = position.move_result([my_move] + [their_move])
            child = minimax(result_position, depth-1)
            evaluation = child[0]
            critical = child[2]
            if (critical):
                end_state = True
            evaluations.append(evaluation)
        my_move_evaluations.append((min(evaluations), my_move, end_state))
    my_best_move = max(my_move_evaluations)
    return my_best_move


#evaluation, this move
def maximax(position, depth):
    evaluation = position.evaluate()
    end_state = (evaluation == float('-inf') or evaluation == float('inf'))
    if depth == 0 or end_state:
        return (evaluation, None)

    my_move_evaluations = []
    me = [entity for entity in position.entities if entity.is_me()][0]
    thems = [entity for entity in position.entities if (not entity.is_me()) and entity.is_any_player()]
    dummy_moves = [Move(MOVE_MOVE, them.x, them.y, them.owner) for them in thems]
    my_possible_moves = possible_moves_for_player(position, me)
    evaluations = []
    for my_move in my_possible_moves:
        result_position = position.move_result([my_move] + dummy_moves)
        child = maximax(result_position, depth-1)
        evaluations.append((child[0], my_move))
    my_best_move = max(evaluations)
    return my_best_move



def psychic_pathfinding(the_future, a):
    
    first_steps = open_bordering_squares(the_future[0], a[0], a[1])
    frontier = [(step[0], step[1], 0, [step]) for step in first_steps]
    full_paths = []

    while len(frontier) != 0:
        #x, y, frame, path
        current = frontier.pop()


        #######NEW SUNDAY
        current_frame = the_future[current[2]]
        items = [item for item in current_frame.entities if item.is_item() and item.x == current[0] and item.y == current[1]]
        if len(items) > 0:
            for frame in the_future[current[2]:]:
                items = [item for item in frame.entities if item.is_item() and item.x == current[0] and item.y == current[1]]
                if len(items) > 0:
                    frame.entities.remove(items[0])
        #######
    

        next_frame = current[2]+1
        if (next_frame >= len(the_future)):
            full_paths.append(current)
            continue

        if the_future[next_frame].explosion_board[current[1]][current[0]]:
            continue

        next_steps = open_bordering_squares(the_future[next_frame], current[0], current[1])
        
        for next_step in next_steps:
            frontier.append((next_step[0], next_step[1], next_frame, current[3] + [next_step]))

    

    #x, y, frame, path      
    return full_paths



def sorted_paths(paths, destination):
    def arrival_index(path):
        arrival_index = float('inf')
        if (destination in path[3]):
            arrival_index = path[3].index(destination)
        return arrival_index

    paths = [(arrival_index(path), distance((path[0], path[1]), destination)) + path for path in paths]
    paths.sort()
    return paths


#square value tuplets come in form (value, x, y)
def first_nonsuicidal_square(position, value_squares, me):
    
    nonsuicidal_square = value_squares[0]
    suicidal = True
    i = 0
    while (square_is_suicidal(position, nonsuicidal_square[1], nonsuicidal_square[2], me)):
        i += 1
        if i == len(value_squares):
            raise TypeError("All squares are suicidal!")
        nonsuicidal_square = value_squares[i]
        

    return nonsuicidal_square

def square_is_suicidal(position, x, y, me):
    open_squares_here = open_squares(position, x, y)
    if len(open_squares_here) == 0:
        return False
    death_squares = explosion_hits(position, x, y, me.explosion_range())[2]
    suicidal = False
    for square in death_squares:
        if square in open_squares_here:
            open_squares_here.remove(square)
    if len(open_squares_here) == 0:
        suicidal = True
    return suicidal
    

def good_destination(position, reachable_squares, me):
    abstracted_position = abstractified_position(position)
    square_values = compute_square_values(abstracted_position, reachable_squares)
    value_squares = squares_by_value(square_values)
    value_squares.sort(key=lambda maximum: (-maximum[0], me.distance_to((maximum[1], maximum[2])))) 
    nearest_maximum = first_nonsuicidal_square(position, value_squares, me)
    destination = nearest_maximum[1], nearest_maximum[2]
    return destination


def select_path(the_future, all_paths, destination):

    #arrival index, distance, x, y, frame, path
    all_paths = sorted_paths(all_paths, destination)

    earliest_bomb = 0
    for i in range(len(the_future)):
        frame = the_future[i]
        future_me = -1
        for entity in frame.entities:
            if entity.is_me():
                future_me = entity
        if (future_me == -1):
            earliest_bombs = len(the_future)
            break
        if (future_me.bombs_remaining() > 0):
            earliest_bombs = i
            break

    next_square = all_paths[0][5][0]
    for path_tuple in all_paths:
        if path_tuple[0] >= earliest_bomb:
            next_square = path_tuple[5][0]
            break

    return next_square


def squares_with_threats(position, me):
    thems = [them for them in position.entities if not them.is_me()]
    squares = []
    for them in thems:
        hits = explosion_hits(position, them.x, them.y, me.explosion_range())
        squares = squares + hits[2]
    return squares


# game loop
global_player_points = {}
while True:
##
#    print(time.time())
##


    
    ################SETUP#############
    board = []
    for i in range(HEIGHT):
        row = list(input())
        board.append(row)
        

    entities_count = int(input())
    entities = []
    for i in range(entities_count):
        parameters = [int(j) for j in input().split()]
        entities.append(Entity(parameters))


#    print(time.time())
    position = Position(board, entities)
    dummy_moves = [Move(MOVE_MOVE, them.x, them.y, them.owner) for them in position.entities if them.is_any_player()]
    position = position.move_result(dummy_moves, skip_tick = True)


    #ugly point counting
    point_counter = position.move_result(dummy_moves)
    if global_player_points == {}:
        for key in point_counter.player_points.keys():
            global_player_points[key] = 0
    for key in point_counter.player_points.keys():
        global_player_points[key] = global_player_points[key] + point_counter.player_points[key]
    sorted_points = [point for point in reversed(sorted(global_player_points.values()))]
    
    me = -1
    for entity in entities:
        if entity.is_me():
            me = entity



    #####PREDICT THE FUTURE############
    vision_depth = 5

    the_future = [position]
    dummy_moves = [Move(MOVE_MOVE, them.x, them.y, them.owner) for them in position.entities if them.is_any_player()]
    for i in range(vision_depth):
        the_future.append(the_future[-1].move_result(dummy_moves))


    
    #######DIRECTIONLESS PATHFINDING###
    all_paths = psychic_pathfinding(the_future, (me.x, me.y))
    if (len(all_paths)) == 0:
        print ("We're doomed.", file=sys.stderr)
        print(Move(BOMB_MOVE, 6, 4, MY_ID).get_string())
        continue
    reachable_squares = set([(path[0], path[1]) for path in all_paths])



    #####FIND A GOOD DESTINATION#######
    destination = good_destination(position, reachable_squares, me)
    #an agressive destination if i'm losing and the boxes are gone
    if (sorted_points[0] != global_player_points[MY_ID] and remaining_boxes == 0):
        sorted_threats = squares_with_threats(position, me)
        sorted_threats.sort(key=lambda square: distance((me.x, me.y), square))
        destination = sorted_threats[0]        
        print("grr...", destination, file=sys.stderr)


    #############FIND THE PATH#########
    next_square = select_path(the_future, all_paths, destination)



    #####UPDATE THE FUTURE FOR BOMBING##########
    bombing = ((me.x, me.y) == destination and me.bombs_remaining() > 0)
    
    the_future = [position]
    my_dummy_move = Move(MOVE_MOVE, next_square[0], next_square[1], MY_ID)
    my_first_move = my_dummy_move
    if (bombing):
        my_first_move = Move(BOMB_MOVE, next_square[0], next_square[1], MY_ID)
    dummy_moves = [Move(MOVE_MOVE, them.x, them.y, them.owner) for them in position.entities if them.is_any_player() and not them.is_me()]
    for i in range(vision_depth):
        together_dummy_moves = dummy_moves + [my_dummy_move]
        if i == 0:
            together_dummy_moves = dummy_moves + [my_first_move]
        the_future.append(the_future[-1].move_result(together_dummy_moves))




    #####FIND NEW DESTINATION AFTER BOMBING######
        #but don't bomb if we see trouble
    if bombing:
        all_paths = psychic_pathfinding(the_future, (me.x, me.y))
        if len(all_paths) == 0:
            print ("Careful of the future!", file=sys.stderr)
            bombing = False
        else:
            reachable_squares = set([(path[0], path[1]) for path in all_paths])
            destination = good_destination(the_future[1], reachable_squares, me)
            next_square = select_path(the_future, all_paths, destination)
            if square_is_suicidal(the_future[1], next_square[0], next_square[1], me):
                print ("Careful of small rooms!", file=sys.stderr)
                bombing = False
        
        
        
        





    final_move = None

    #stop dropping bombs if i'm going to win on time
    remaining_boxes = 0
    for row in position.board:
        for cell in row:
            if cell in [str(box) for box in [EMPTY_BOX, EXTRA_BOMB, EXTRA_RANGE]]:
                remaining_boxes += 1
    im_winning = (sorted_points[0] == global_player_points[MY_ID] and abs(sorted_points[0] - sorted_points[1]) > remaining_boxes)
    its_tied = sorted_points[0] == sorted_points[1] and (sorted_points[0] == global_player_points[MY_ID]) and remaining_boxes == 0
    if len(sorted_points) > 1 and (im_winning or its_tied):
        print("Dance dance dance", file=sys.stderr)
        bombing = False
    
    
    if bombing:
        final_move = Move(BOMB_MOVE, next_square[0], next_square[1], MY_ID)
    else:
        final_move = Move(MOVE_MOVE, next_square[0], next_square[1], MY_ID)



    print (final_move.get_string())



##
#    print(time.time())
##


    

