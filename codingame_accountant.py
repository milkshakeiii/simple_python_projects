import sys
import math
import random
import time



MOVE = 0
SHOOT = 1



GADEPTH = 20
GATURNOVER = 0.8

MOVE_BIAS = 0.5
FULL_SPEED_BIAS = 0.25
SHOOT_NEAREST_BIAS = 0.5


MUTATE_TWEAK_CHANCE = 0.15
MUTATE_TWEAK_POWER = 0.08
MUTATE_RANDOMIZE_CHANCE = 0.14



def dumb_strategy(game):

    return Move(SHOOT, game.enemies[0])




def stand_and_deliver(game):

    nearest_enemy = (game.enemies[0], float('inf'))
    for enemy in game.enemies:
        distance_to_enemy = game.wolff.position.distance_to(enemy.position)
        if distance_to_enemy < nearest_enemy[1]:
            nearest_enemy = (enemy, distance_to_enemy)
    
    return Move(SHOOT, nearest_enemy[0])



class GAIndividual():
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



        self.fitness = -1

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
        for i in range(len(self.genes)):
            chance = random.random()
            if (chance < MUTATE_TWEAK_CHANCE):
                self.genes[i] = (self.genes[i] + random.random() * MUTATE_TWEAK_POWER - MUTATE_TWEAK_POWER/2)%1
            if (chance > 1 - MUTATE_RANDOMIZE_CHANCE):
                self.genes[i] = random.random()
        

    def evaluate_fitness_on_game(self, game):
        self.reset_reading()
        game.simulate(self.my_strategy)
        self.fitness = game.score()
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
                distance_to_enemy = game.wolff.position.distance_to(enemy.position)
                if distance_to_enemy < nearest_enemy[1]:
                    nearest_enemy = (enemy, distance_to_enemy)
                    
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


    


class GAGeneration():
    def __init__(self, size):
        self.size = size
        self.members = []

    def randomize(self):
        for i in range(self.size):
            new_individual = GAIndividual(GADEPTH)
            new_individual.randomize()
            self.members.append(new_individual)

    def revolve(self, game):
        individuals_to_keep = int((1-GATURNOVER) * len(self.members))
        
        fitness_sum = 0
        for member in self.members:
            new_game = game.copy()
            member.evaluate_fitness_on_game(new_game)
            #print(member.fitness)
            fitness_sum += member.fitness


        self.members.sort(key=lambda member: -member.fitness)

        print("sum: " + str(fitness_sum), file=sys.stderr)
        print("max: " + str(self.members[0].fitness), file=sys.stderr)

        
        survivors = self.members[:individuals_to_keep]
        
        new_generation = []
        while len(new_generation) < self.size - individuals_to_keep:
            random_parent_a = survivors[int(random.random() * len(survivors))]
            random_parent_b = survivors[int(random.random() * len(survivors))]
            new_individual = GAIndividual(GADEPTH)
            new_individual.spawn_from([random_parent_a, random_parent_b])
            new_individual.mutate()
            new_generation.append(new_individual)
        
        self.members = survivors + new_generation
        





class Point():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def distance_to(self, b):
        a = self
        da = a.x-b.x
        db = a.y-b.y
        d = math.sqrt(da**2 + db**2)
        return d
        
    def direction_to(self, b):
        opposite = b.y-self.y
        adjacent = b.x-self.x
        return math.atan2(opposite, adjacent)

    def point_distance_towards(self, units, target):
        angle = self.direction_to(target)
        return self.point_distance_in(units, angle)

    def point_distance_in(self, units, angle):
        y = self.y + math.sin(angle)*units
        x = self.x + math.cos(angle)*units
        return (Point(x, y))
        

    def __eq__(a, b):
        return (a.x == b.x) and (a.y == b.y)

    


class Unit():
    def __init__(self, game_id, position, speed):
        self.position = position
        self.speed = speed
        self.game_id = game_id

    def move_toward(self, target):
        if self.position.distance_to(target) <= self.speed:
            self.position = target
        else:
            self.position = self.position.point_distance_towards(self.speed, target)


class Enemy(Unit):
    def __init__(self, game_id, position, health):
        super().__init__(game_id, position, 500)
        self.health = health
        self.target_data_point = None

    def set_target_data_point(self, data_points):
        def distance_to_data_point(data_point):
            return self.position.distance_to(data_point.position)
        self.target_data_point = min(data_points, key = distance_to_data_point)

    def copy(self):
        return Enemy(self.game_id, self.position, self.health)
        


class Wolff(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 1000)

    def shot_damage(self, enemy):
        return round(125000 / self.position.distance_to(enemy.position)**1.2)
        


class Data_Point(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 0)

    def copy(self):
        return Data_Point(self.game_id, self.position)



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

    def copy(self):
        return Game(Wolff(self.wolff.game_id, Point(self.wolff.position.x, self.wolff.position.y)),
                    [enemy.copy() for enemy in self.enemies],
                    [data_point.copy() for data_point in self.data_points])

    def score(self):
        if self.lost:
            return 0
        DP = len(self.data_points)
        base = 100 * DP + 10 * (self.starting_enemy_count - len(self.enemies))
        bonus = DP * max(0, self.L - 3*self.S) * 3
        return base + bonus

    def do_move(self, move):
        #enemies move towards their targets
        for enemy in self.enemies:
            if enemy.target_data_point == None:
                enemy.set_target_data_point(self.data_points)
            enemy.move_toward(enemy.target_data_point.position)
            
        #if a move command was given, Wolff moves towards his target            
        if (move.move_type == MOVE):
            self.wolff.move_toward(move.target)

        #game over if an enemy is close enough to Wolff
        for enemy in self.enemies:
            if self.wolff.position.distance_to(enemy.position) <= 2000:
                self.lost = True
                return

        #if a shoot command was given, Wolff shoots an enemy
        if (move.move_type == SHOOT):
            damage = self.wolff.shot_damage(move.target)
            move.target.health -= damage
            self.S += 1

            #enemies with zero life points are removed from play
            if (move.target.health <= 0):
                self.enemies.remove(move.target)

        #enemies collect data points they share coordinates with
        collected_data_points = set()
        for enemy in self.enemies:
            if enemy.position == enemy.target_data_point.position:
                collected_data_points.add(enemy.target_data_point)
        for collected_data_point in collected_data_points:
            self.data_points.remove(collected_data_point)
            for enemy in self.enemies:
                if (enemy.target_data_point == collected_data_point):
                    enemy.target_data_point = None

        #If all data points are collected by the enemies, the game ends.
        if len(self.data_points) == 0:
            self.won = True
            return

        #if there are no more enemies left, we win yay
        if len(self.enemies) == 0:
            self.won = True
                
    def simulate(self, strategy):
        while (not self.won and not self.lost):
            next_move = strategy(self)
            self.do_move(next_move)
            
            


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









first_loop = True
my_GA = None
# game loop
while True:


#    while (True):
#        print(input(), file=sys.stderr)

    
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



    game = Game(wolff, enemies, data_points)
    


    if (first_loop):
        gen = GAGeneration(100)
        gen.randomize()
        print("start revolving " + str(time.time()), file=sys.stderr)
        for i in range(7):
            gen.revolve(game)
        print("stop revolving " + str(time.time()), file=sys.stderr)
        my_GA = gen.members[0]
        my_GA.reset_reading()
        first_loop = False

    


    # MOVE x y or SHOOT id
    print(my_GA.my_strategy(game).get_string())




