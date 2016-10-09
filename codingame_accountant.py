import sys
import math
import random
import time



FIRST_TIME_LIMIT = 0.935
FIRST_TIME_CRIT = 0.960
SUBSEQUENT_TIME_LIMIT = 0.05
SUBSEQUENT_TIME_CRIT = 0.06
SUPER_CRIT_REMAINDER = 0.02


STODEPTH = 10
EVAL_DEPTH = float('inf')


MUTATE_COUNT = 9
MUTATE_TWEAK_CHANCE = 0.5
MUTATE_TWEAK_POWER = 0.25
MUTATE_RANDOMIZE_CHANCE = 1 - MUTATE_TWEAK_CHANCE


MOVE_BIAS = 0.7
FULL_SPEED_BIAS = 0.25
SHOOT_NEAREST_BIAS = 0.3


WIDTH = 16000
HEIGHT = 9000


MOVE = 0
SHOOT = 1





def dumb_strategy(game):

    return Move(SHOOT, game.enemies[0])


def do_nothing(game):
    
    return Move(MOVE, game.wolff.position)


def stand_and_deliver(game):

    nearest_enemy = (game.enemies[0], float('inf'))
    for enemy in game.enemies:
        distance_to_enemy = game.wolff.position.square_distance_to(enemy.position)
        if distance_to_enemy < nearest_enemy[1]:
            nearest_enemy = (enemy, distance_to_enemy)
    
    return Move(SHOOT, nearest_enemy[0])



class Individual():
    def __init__(self, depth):
        #every four genes represents one move
        #it consists of values from 0 to 1
        #(1st) for the first value: less than 0.5 means move, greater means shoot
        #(2nd) second value is ignored for shoot, it is angle to move from 0 to 2pi radians
        #(3rd) third value is ignored for shoot, it is distance to move,
        #linearally 0 to 1000 from 0 to 0.75, rest represents 1000
        #(4th) fourth represents which enemy to shoot, nearest enemy has 1/2 chance,
        #the rest is distributed evenly
        self.genes = []
        self.genes_read = 0

        
        self.depth = depth



        self.fitness = float('-inf')

    def copy(self):
        copy = Individual(self.depth)
        copy.genes = self.genes[:]
        copy.genes_read = self.genes_read
        copy.fitness = self.fitness
        return copy

    def reset_reading(self):
        self.genes_read = 0

    def read_a_gene(self):
        gene = self.genes[self.genes_read]
        self.genes_read += 1
        return gene

    def randomize(self):
        for i in range(self.depth):
            for j in range(4):
                self.genes.append(random.random())

    def spawn_from(self, parents):
        for i in range(len(parents[0].genes)):
            random_parent_i = int(random.random() * len(parents))
            random_parent = parents[random_parent_i]
            self.genes.append(random_parent.genes[i])

    def mutate(self):
        result = self.copy()
        mutate_me = []
        for i in range(MUTATE_COUNT):
            mutate_me.append(int(random.random()*len(result.genes)))
        for i in mutate_me:
            chance = random.random()
            if (chance < MUTATE_TWEAK_CHANCE):
                result.genes[i] = (result.genes[i] + random.random() * MUTATE_TWEAK_POWER - MUTATE_TWEAK_POWER/2)%1
            if (chance > 1 - MUTATE_RANDOMIZE_CHANCE):
                result.genes[i] = random.random()
        return result
        

    def evaluate_fitness_on_game(self, game, depth, time_limit, turn_start):
        self.reset_reading()
        if (not game.simulate(self.my_strategy, depth, time_limit, turn_start)):
            self.fitness = game.score()

        #print(time.time())
        return self.fitness

    def my_strategy(self, game):
        if self.genes_read < len(self.genes):
            next_four_genes = []
            for i in range(4):
                next_four_genes.append(self.read_a_gene())

            next_move_type = SHOOT
            if next_four_genes[0] < MOVE_BIAS:
                next_move_type = MOVE
            
            move_direction = math.pi * 2 * next_four_genes[1]

            move_magnitude = 1000
            if next_four_genes[2] > FULL_SPEED_BIAS:
                move_magnitude = 1000 * ( (next_four_genes[2] - FULL_SPEED_BIAS)/(1 - FULL_SPEED_BIAS) )


            move_target = game.wolff.position.point_distance_in(move_magnitude, move_direction)
            
            
            #enemy, distance
            nearest_enemy = (game.enemies[0], float('inf'))
            for enemy in game.enemies:
                distance_to_enemy = game.wolff.position.square_distance_to(enemy.position)
                if distance_to_enemy < nearest_enemy[1]:
                    nearest_enemy = (enemy, distance_to_enemy)
            #murderee = game.enemies[int(next_four_genes[3]*len(game.enemies))]
            murderee = nearest_enemy[0]
            if next_four_genes[3] > SHOOT_NEAREST_BIAS:
                unbiased_value = ( (next_four_genes[3] - SHOOT_NEAREST_BIAS)/(1 - SHOOT_NEAREST_BIAS) )
                random_enemy = int(next_four_genes[3] * len(game.enemies))
                murderee = game.enemies[random_enemy]

            next_move = None
            if next_move_type == MOVE:
                next_move = Move(MOVE, move_target)
            else:
                next_move = Move(SHOOT, murderee)
            return next_move
        else:
            return stand_and_deliver(game)





memoized_distance_to = {}
memoized_square_distance_to = {}
memoized_direction_to = {}
memoized_point_distance_towards = {}
memoized_point_distance_in = {}
class Point():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def distance_to(self, b):
        key = (self.x, self.y, b.x, b.y)
        if key in memoized_distance_to:
            return memoized_distance_to[key]
        d = math.sqrt(self.square_distance_to(b))
        memoized_distance_to[key] = d
        return d

    def square_distance_to(self, b):
        key = (self.x, self.y, b.x, b.y)
        if key in memoized_square_distance_to:
            return memoized_square_distance_to[key]
        a = self
        da = a.x-b.x
        db = a.y-b.y
        d = da**2 + db**2
        memoized_square_distance_to[key] = d
        return d
        
    def direction_to(self, b):
        key = (self.x, self.y, b.x, b.y)
        if key in memoized_direction_to:
            return memoized_direction_to[key]
        opposite = b.y-self.y
        adjacent = b.x-self.x
        angle = math.atan2(opposite, adjacent)
        memoized_direction_to[key] = angle
        return angle

    def point_distance_towards(self, units, target):
        key = (self.x, self.y, target.x, target.y, units)
        if key in memoized_point_distance_towards:
            return memoized_point_distance_towards[key]
        angle = self.direction_to(target)
        d = self.point_distance_in(units, angle)
        memoized_point_distance_towards[key] = d
        return d

    def point_distance_in(self, units, angle):
        key = (self.x, self.y, units, angle)
        if key in memoized_point_distance_in:
            return memoized_point_distance_in[key]
        y = self.y + math.sin(angle)*units
        x = self.x + math.cos(angle)*units
        point = (Point(x, y))
        memoized_point_distance_in[key] = point
        return point

    def copy(self):
        return Point(self.x, self.y)

    def __eq__(a, b):
        return (a.x == b.x) and (a.y == b.y)

    


class Unit():
    def __init__(self, game_id, position, speed):
        self.position = position
        self.speed = speed
        self.game_id = game_id

    def move_toward(self, target):
        end = None
        if self.position.square_distance_to(target) <= self.speed**2:
            end = target
        else:
            end = self.position.point_distance_towards(self.speed, target)
        if (end.x < 0):
            end.x = 0
        if (end.y < 0):
            end.y = 0
        if (end.x > WIDTH):
            end.x = WIDTH
        if (end.y > HEIGHT):
            end.y = HEIGHT
        self.position = end


class Enemy(Unit):
    def __init__(self, game_id, position, health):
        super().__init__(game_id, position, 500)
        self.health = health
        self.target_data_point = None
        self.facing = None
        self.distance_to_target = None

    def approach_target(self):
        end = None
        target_reached = False
        target = self.target_data_point.position
        if self.position.square_distance_to(target) <= self.speed**2:
            end = target
            target_reached = True
        else:
            #end = self.position.point_distance_in(self.speed, self.facing)
            end = self.position.point_distance_towards(self.speed, self.target_data_point.position)
        if (end.x < 0):
            end.x = 0
        if (end.y < 0):
            end.y = 0
        if (end.x > WIDTH):
            end.x = WIDTH
        if (end.y > HEIGHT):
            end.y = HEIGHT
        self.position = end
        return target_reached
##        self.distance_to_target -= self.speed
##        if self.distance_to_target < 0:
##            self.position = self.target_data_point.position
##            return True
##        else:
##            self.position = self.position.point_distance_in(self.speed, self.facing)
##            return False

    def set_target_data_point(self, data_points):
        def distance_to_data_point(data_point):
            return self.position.distance_to(data_point.position)
        self.target_data_point = min(data_points, key = distance_to_data_point)
        self.facing = self.position.direction_to(self.target_data_point.position)
        self.distance_to_target = self.position.distance_to(self.target_data_point.position)
        self.target_data_point.targeters.append(self)

    def copy(self):
        return Enemy(self.game_id, self.position, self.health)

        


class Wolff(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 1000)

    def shot_damage(self, enemy):
        damage = round(125000 / self.position.distance_to(enemy.position)**1.2)
        #print ("BANG! " + str(damage))
        return damage
        


class Data_Point(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 0)
        self.targeters = []

    def copy(self):
        return Data_Point(self.game_id, self.position)

    def clear_from_targeters(self):
        for targeter in self.targeters:
            targeter.target_data_point = None


class Game():
    def __init__(self, wolff, enemies, data_points):
        self.wolff = wolff
        self.enemies = enemies
        self.data_points = data_points
        self.L = sum([enemy.health for enemy in enemies])
        self.S = 0
        self.starting_enemy_count = len(self.enemies)
        self.lost = False
        self.won = False
        self.turns_simulated = 0
        self.turn_lost = None

    def copy(self):
        copy = Game(Wolff(self.wolff.game_id, Point(self.wolff.position.x, self.wolff.position.y)),
                    [enemy.copy() for enemy in self.enemies],
                    [data_point.copy() for data_point in self.data_points])
        copy.lost = self.lost
        copy.won = self.won
        copy.starting_enemy_count = self.starting_enemy_count
        copy.S = self.S
        copy.L = self.L
        return copy

    def score(self):
        if self.lost:
            return -300 + self.turn_lost
        DP = len(self.data_points)
        base = 100 * DP + 10 * (self.starting_enemy_count - len(self.enemies))
        bonus = DP * max(0, self.L - 3*self.S) * 3
        return base + bonus

    def do_move(self, move):
        self.turns_simulated += 1
        
        #enemies move towards their targets
        collecting_enemies = []
        for enemy in self.enemies:
            if enemy.target_data_point == None:
                enemy.set_target_data_point(self.data_points)
            if (enemy.approach_target()):
                collecting_enemies.append(enemy)
            #enemy.move_toward(enemy.target_data_point.position)
            
        #if a move command was given, Wolff moves towards his target            
        if (move.move_type == MOVE):
            self.wolff.move_toward(move.target)

        #game over if an enemy is close enough to Wolff
        for enemy in self.enemies:
            if self.wolff.position.square_distance_to(enemy.position) <= 2000**2:
                self.lost = True
                if self.turn_lost == None:
                    self.turn_lost = self.turns_simulated
                return

        murderee = None
        #if a shoot command was given, Wolff shoots an enemy
        if (move.move_type == SHOOT):
            damage = self.wolff.shot_damage(move.target)
            move.target.health -= damage
            self.S += 1

            #enemies with zero life points are removed from play
            if (move.target.health <= 0):
                self.enemies.remove(move.target)
                murderee = move.target

        #enemies collect data points they arrived at
        collected_data_points = set()
        for collecting_enemy in collecting_enemies:
            if collecting_enemy != murderee:
                collected_data_points.add(collecting_enemy.target_data_point)
        for collected_data_point in collected_data_points:
            self.data_points.remove(collected_data_point)
            collected_data_point.clear_from_targeters()

        #If all data points are collected by the enemies, the game ends.
        if len(self.data_points) == 0:
            self.won = True
            return

        #if there are no more enemies left, we win yay
        if len(self.enemies) == 0:
            self.won = True
                
    def simulate(self, strategy, depth, time_limit, turn_start):
        start_time = time.time()
        depth_simulated = 0
        while (not self.won and not self.lost and depth_simulated < depth):
            if (time.time() - turn_start > time_limit):
                #print ("Eep! Time!", time.time(), file=sys.stderr)
                return True

            #print(time.time())
            depth_simulated += 1
            next_move = strategy(self)
            self.do_move(next_move)

        return False
            
            


class Move():
    def __init__(self, move_type, target):
        self.move_type = move_type
        self.target = target

    def get_string(self):
        result = ""
        if self.move_type == MOVE:
            result = "MOVE" + " " + str(self.target.x) + " " + str(self.target.y)
        if self.move_type == SHOOT:
            result = "SHOOT" + " " + str(self.target.game_id)
        return result




def pure_random_spin(game, best_solution, time_limit, turn_start, loop_count):
    evaluated = 0
    print("start guessing " + str(time.time()), file=sys.stderr)
    while (time.time() - turn_start < time_limit):
        next_solution = Individual(STODEPTH)
        next_solution.randomize()
        next_solution.evaluate_fitness_on_game(game.copy(), EVAL_DEPTH, time_limit, turn_start)
        #print(time.time())
        next_solution.reset_reading()
        if (next_solution.fitness > best_solution.fitness):
            best_solution = next_solution
        evaluated += 1                    
    print("stop guessing " + str(time.time()), file=sys.stderr)
    print(str(evaluated) + " guesses evaluated", file=sys.stderr)
    print("best fitness: " + str(best_solution.fitness), file=sys.stderr)
    return best_solution



def simulated_annealing(game, best_s, time_limit, turn_start, loop_count):
    #print(best_s, best_s.genes[0])
    
    def T():
        if loop_count == 0:
            portion_remaining = (time_limit-(time.time()-turn_start))/time_limit
        else:
            overall_time_limit = 1
            overall_time_elapsed = ((loop_count-1)%10*0.1 + time.time()-turn_start)
            portion_remaining = (overall_time_limit-overall_time_elapsed)/overall_time_limit
        return 100*(portion_remaining**4)

    def P(sfit, snewfit, T):
        difference = snewfit-sfit
        if difference > 0:
            return 1
        return math.e**(difference/T)

    s = best_s
    s.evaluate_fitness_on_game(game.copy(), EVAL_DEPTH, time_limit, turn_start)
    s.reset_reading()
    
    evaluated = 0
#    print("start guessing " + str(time.time()), file=sys.stderr)
    while (time.time() - turn_start < time_limit):
        snew = s.mutate()
        snew.evaluate_fitness_on_game(game.copy(), EVAL_DEPTH, time_limit, turn_start)
        snew.reset_reading()
        evaluated += 1
        #print(snew.fitness)
        accept_chance = P(s.fitness, snew.fitness, T())
        #print(T())
        #print(P(10, 0, T()))
        if accept_chance >= random.random():
            s = snew
        if (s.fitness>best_s.fitness):
#            print ("found a new best s! ", s.fitness, file=sys.stderr)
            best_s = s
    #print("stop guessing " + str(time.time()), file=sys.stderr)
    #print(str(evaluated) + " guesses evaluated", file=sys.stderr)
    return best_s
        

def solution(spin_for_best):
    loop_count = 0
    my_next_game = None
    original_game = None
    time_failure = False
    while True:

        #while True:
        #    print(input(), file=sys.stderr)

        #############################READ INPUT##############
        x, y = [int(i) for i in input().split()]
        wolff_position = Point(x, y)
        wolff = Wolff(0, wolff_position)
        
        data_count = int(input())
        data_points = []
        for i in range(data_count):
            data_id, data_x, data_y = [int(j) for j in input().split()]
            data_position = Point(data_x, data_y)
            data_points.append(Data_Point(data_id, data_position))
            
        enemy_count = int(input())
        enemies = []
        for i in range(enemy_count):
            enemy_id, enemy_x, enemy_y, enemy_life = [int(j) for j in input().split()]
            enemy_position = Point(enemy_x, enemy_y)
            enemies.append(Enemy(enemy_id, enemy_position, enemy_life))

        turn_start = time.time()
#        print("turn begins at ", turn_start, file=sys.stderr)

        game = Game(wolff, enemies, data_points)
        input_game = game.copy()
        
        



        ############################ON THE FIRST CYCLE################
        if (loop_count == 0):

            original_game = game.copy()

            best_solution = Individual(0)
            best_solution.evaluate_fitness_on_game(original_game.copy(), EVAL_DEPTH, FIRST_TIME_LIMIT, turn_start)
#            print("stand and deliver: " + str(best_solution.fitness), file=sys.stderr)
            best_solution.reset_reading()

            best_spun_solution = Individual(STODEPTH)
            best_spun_solution.randomize()
            best_spun_solution = spin_for_best(original_game, best_spun_solution, FIRST_TIME_LIMIT, turn_start, loop_count)
            best_solution = max(best_spun_solution, best_solution, key=lambda solution: solution.fitness)
            
            best_solution.reset_reading()
            time_failure = game.simulate(best_solution.my_strategy, STODEPTH, FIRST_TIME_CRIT, turn_start)
            best_solution.reset_reading()
            
            my_next_game = game
            next_best_solution = best_solution
            best_spun_solution = Individual(STODEPTH)
            best_spun_solution.randomize()
            


        elif not time_failure:        


            ###################################ON SUBSEQUENT CYCLES###############
            best_spun_solution = spin_for_best(my_next_game, best_spun_solution, SUBSEQUENT_TIME_LIMIT, turn_start, loop_count)
            next_best_solution = max(best_spun_solution, next_best_solution, key=lambda solution: solution.fitness)
            #print(time.time())
            #################WHEN ITS TIME TO SWITCH TO OUR NEXT STOCHASTIC SOLUTION############
            #every STODEPTH loops
            if (loop_count % STODEPTH == 0):
#                print ("NEXT BEST GUESS", file=sys.stderr)
                best_solution = next_best_solution

                
                time_failure = my_next_game.simulate(next_best_solution.copy().my_strategy, STODEPTH, SUBSEQUENT_TIME_CRIT, turn_start)
                
                
                
                next_best_solution = best_solution
                best_spun_solution = Individual(STODEPTH)
                best_spun_solution.randomize()


 

#        print(len(input_game.enemies), len(original_game.enemies), file=sys.stderr)
#        print(len(input_game.data_points), len(original_game.data_points), file=sys.stderr)
#        for i in range(len(input_game.enemies)):
#            if input_game.enemies[i].position != original_game.enemies[i].position:
#            print (input_game.enemies[i].position.x,
#                   input_game.enemies[i].position.y,
#                   original_game.enemies[i].position.x,
#                   original_game.enemies[i].position.y,
#                   input_game.enemies[i].game_id,
#                   original_game.enemies[i].game_id,
#                   #original_game.enemies[i].target_data_point.game_id,
#                   file=sys.stderr)           
                

        if not time_failure:
            
            ######HORRIBLE BROKEN TEST!!!!!!!!!##########################
            # len(original_game.enemies) == 0:
            #    this_turn_move = stand_and_deliver(input_game)
            #    print(this_turn_move.get_string())
            #    loop_count += 1
            #    continue
            ######HORRIBLE BROKEN TEST!!!!!!!!!##########################
            
            #print(time.time())
            # MOVE x y or SHOOT id
            this_turn_move = best_solution.my_strategy(original_game)
            turn_time = 0.1
            if (loop_count == 0):
                turn_time = 1
            final_limit = turn_time - SUPER_CRIT_REMAINDER

            #print("started simulating one turn at: ", time.time())
            time_failure = original_game.simulate(lambda input_game: this_turn_move, 1, final_limit, turn_start)
#            print("turn over at ", time.time(), " score; ", original_game.score(), file=sys.stderr)
            print(this_turn_move.get_string())
            loop_count += 1
        else:
#            print("time failure: ", time.time(), file=sys.stderr)
            this_turn_move = stand_and_deliver(input_game)
            print(this_turn_move.get_string())
            loop_count += 1


    




solution(simulated_annealing)
