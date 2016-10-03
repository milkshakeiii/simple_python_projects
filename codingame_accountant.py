import sys
import math


MOVE = 0
SHOOT = 1



class Point():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def distance_to(self, b):
        a = self
        da = a.x-b.y
        db = a.x-b.y
        d = math.sqrt(da**2 + db**2)
        return d
        
    def direction_to(self, b):
        opposite = b.y-self.y
        adjacent = b.x-self.x
        return math.atan2(opposite, adjacent)

    def point_distance_towards(self, units, target):
        angle = self.direction_to(target)
        y = self.y + math.sin(angle)*units
        x = self.x + math.cos(angle)*units
        return (Point(x, y))

    


class Unit():
    def __init__(self, game_id, position, speed):
        self.position = position
        self.speed = speed
        self.game_id = game_id

    def move_toward(self, target):
        self.position = self.position.point_distance_towards(self.speed, target)


class Enemy(Unit):
    def __init__(self, game_id, position, health):
        super().__init__(game_id, position, 500)
        self.health = health
        self.target_data_point = None

    def set_target_data_point(self, data_points):
        def distance_to_data_point(data_point):
            return self.position.distance_to(data_point.position)
        target_data_point = min(data_points, key = distance_to_data_point)


class Wolff(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 1000)


class Data_Point(Unit):
    def __init__(self, game_id, position):
        super().__init__(game_id, position, 0)



class Game():
    def __init__(self, wolff, enemies, data_points):
        self.wolff = wolff
        self.enemies = enemies
        self.data_points = data_points
        self.L = sum([enemy.health for enemy in enemies])
        self.S = 0
        self.starting_enemy_count = len(self.enemies)
        self.lost = False

    def score(self):
        if lost:
            return -1
        DP = len(self.data_points)
        base = 100 * DP + 10 * (self.starting_enemy_count - len(self.enemies))
        bonus = DP * max(0, self.L - 3*self.S) * 3
        return base + bonus

    def do_move(self, move):
        #enemies move towards their targets
        for enemy in self.enemies:
            if enemy.target_data_point == None:
                enemy.set_target_data_point()
            enemy.move_toward(enemy.target_data_point())

        #if a move command was givne, WOlff moves towards his target            
        if (move.move_type == MOVE):
            self.wolff.move_toward(move.target)

        #game over if an enemy is close enough to wolff
        for enemy in self.enemies:
            if self.wolff.position.distance_to(enemy.position) <= 2000:
                self.lost = True
                return

        #if a shoot command was given, Wolff shoots an enemy
        if (move.move_type == SHOOT):
            self.wolff.shoot(move.target)
            
            


def dumb_strategy(game):



    return Move(MOVE, Point(8000, 4500))




def stand_and_deliver(game):
    
    return Move(SHOOT, game.enemies[0])




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


# game loop
while True:
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


    # MOVE x y or SHOOT id
    print(stand_and_deliver(game).get_string())
