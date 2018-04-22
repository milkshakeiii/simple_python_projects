import sys
import math
import random

WIDTH = 1920
HEIGHT = 1000

KNIGHT_COST = 80
ARCHER_COST = 100
GIANT_COST = 140

UNITS_TO_SPEEDS = {-1: 60, 0: 100, 1: 75, 2: 50}

SITE_WEIGHT = float('inf')
QUEEN_WEIGHT = 100
GIANT_WEIGHT = 20
ARCHER_WEIGHT = 9
KNIGHT_WEIGHT = 4

QUEEN_RADIUS = 30

##########################################
#SITES: (site_id, x, y, radius)
#
#STRUCTURES: (site_id, gold, maxMineSize, structure_type, owner, param_1, param_2)
#-1: No structure
#0: Goldmine
#1: Tower
#2: Barracks
#
#
#UNITS: (x, y, owner, unit_type, health)
#unitType: The unit type: -1 for Queen, 0 for KNIGHT, 1 for ARCHER, 2 for GIANT
##########################################




def QueenAction(gold, touched_site, sites, structures, units):
    my_mines = MyStructuresOfType(structures, 0)
    my_barracks = MyStructuresOfType(structures, 2)
    my_towers = MyStructuresOfType(structures, 1)
    queen = GetQueen(units)
    
    unclaimed_sites = UnclaimedSites(structures, sites)
    nearest_unclaimed_site = NearestSite(queen, unclaimed_sites)
    unclaimed_sites_and_towers = {**unclaimed_sites, **SitesOfStructures(sites, my_towers)}
    nearest_unclaimed_site_or_tower = NearestSite(queen, unclaimed_sites_and_towers)
    random_unclaimed_site_or_tower = unclaimed_sites_and_towers[random.choice(list(unclaimed_sites_and_towers.keys()))]
    
    nearest_corner = NearestCornerToQueen(queen)
    
    return MoveAroundSites(queen, WIDTH, HEIGHT, sites)
#if nearest_unclaimed_site is None and len(my_towers) > 0:
#    return BuildAStructure("TOWER", touched_site, nearest_unclaimed_site_or_tower)
#elif nearest_unclaimed_site is None:
#    return Move(nearest_cornet[0], nearest_corner[1])
#elif (len(my_barracks) < 1):
#    return BuildAStructure("BARRACKS-KNIGHT", touched_site, nearest_unclaimed_site)
#elif (len(my_mines) < 3):
#    return BuildAStructure("MINE", touched_site, nearest_unclaimed_site)
#elif (len(my_towers) < 2):
#    return BuildAStructure("TOWER", touched_site, nearest_unclaimed_site)
#else:
#    return BuildAStructure("TOWER", touched_site, random_unclaimed_site_or_tower)



def TrainingInstructions(gold, touched_site, sites, structures, units):
    my_structures = MyStructuresOfType(structures, 2)
    budgetable_knights = gold//KNIGHT_COST
    return "TRAIN" + StringifyStructures(my_structures[:budgetable_knights])






#####################-------------------------------------------------------------------------------------------#####################



def SimulateTurn(action, queen, sites, structures, units):
    
    queen, units = DoMovement(action, queen, units)
    #queen, units = ResolveCollisions(queen, sites, units)
    
    
    
    
    
    
    
    
    
    
    
    
    return action, queen, gold, touched_site, sites, structures, units


#def ResolveCollisions(queen, sites, units):
#    weighted_entities


def DoMovement(action, queen, units):
    
    action_components = action.split(' ')
    queen_target = queen[0], queen[1]
    if action_components[0] == "MOVE":
        queen_target = action_components[1], action_components[2]
    
    enemy_queen = GetEnemyQueen(units)

for i in rage(len(units)):
    unit = units[i]
    target = 0, 0
        if unit[3] == -1: #queen
            target = queen_target
    if unit[3] == 0 and unit[2] == 0: #friendly knight
        target = (enemy_queen[0], enemy_queen[1])
        if unit[3] == 0 and unit[2] == 1: #enemy knight
            target = (queen[0], queen[1])

unit = MoveUnitToward(unit, target)
units[i] = unit
    
    return GetQueen(units), units



def MoveUnitToward(unit, target):
    
    x = unit[0]
    y = unit[1]
    target_x = target[0]
    target_y = target[1]
    
    speed = UNITS_TO_SPEEDS[unit[3]]
    distance = math.sqrt(SquaredDistance(x, y, target_x, target_y))
    if speed > distance:
        speed = distance
    
    movement_angle = DirectionToward(x, y, target_x, target_Y)
    movement_x = speed * math.cos(movement_angle)
    movement_y = speed * math.sin(movement_angle)

unit[0] = unit[0] + movement_x
unit[1] = unit[1] + movement_y

return unit





#####################-------------------------------------------------------------------------------------------#####################

def MoveAroundSites(queen, target_x, target_y, sites):
    start_x = queen[0]
    start_y = queen[1]
    direction_to_target = DirectionToward(start_x, start_y, target_x, target_y)
    
    site_list = list(sites.values())
    site_list.sort(key = lambda site: SquaredDistance(site[1], site[2], start_x, start_y))
    
    for site in site_list:
        DistanceFromLineToPoint(start_x, start_y, target_x, target_y, site[1], site[2])
    
    return Move(site_list[0][1], site_list[0][2])




def OptimizePath(queen, target_x, target_y, units, sites):
    
    start_x = queen[0]
    start_y = queen[1]
    iterations = 500
    turns_to_optimize = 20
    
    direction_to_target = DirectionToward(start_x, start_y, target_x, target_y)
    current_moves = [direction_to_target for i in range(turns_to_optimize)]
    
    def Neighbor(moves):
        return [move+random.random()-0.5 for move in moves]
    
    def Temperature(k, kmax):
        return k/kmax
    
    def Energy(queen, target_x, taget_y, units, sites):
        return 1
    
    def Probability(current_energy, new_energy, T):
        return 1 if new_energy < current_energy else 0
    
    for i in range(iterations):
        T = Temperature(i, iterations)
        
        new_moves = Neighbor(moves)





















#####################-------------------------------------------------------------------------------------------#####################

def DebugPrint(message):
    print(message, file=sys.stderr)

def DirectionToward(x, y, target_x, target_y):
    return math.atan2(target_x-x, target_y-y)

def HugATower(tower, sites):
    tower_site = sites[tower[0]]
    return Move(tower_site[1], tower_site[2])

def Move(x, y):
    return "MOVE " + str(x) + " " + str(y)

def RunAway(queen, sites, units):
    pass

def NearestSite(queen, sites):
    if len(sites) == 0:
        return None
    return min(sites.values(), key=lambda site: SquaredDistance(site[1], site[2], queen[0], queen[1]))


def BuildAStructure(type_name, touched_site, target_site):
    if (touched_site == target_site[0]):
        return "BUILD " + str(touched_site) + " " + type_name
    else:
        return Move(target_site[1], target_site[2])

def NearestCornerToQueen(queen):
    corners = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]
    return min(corners, key=lambda corner: SquaredDistance(corner[0], corner[1], queen[0], queen[1]))


def GetQueen(units):
    for unit in units:
        if unit[2] == 0 and unit[3] == -1:
            return unit

def GetEnemyQueen(units):
    for unit in units:
        if unit[2] == 1 and unit[3] == -1:
            return unit

def UnclaimedSites(structures, sites):
    unclaimed_sites = {}
    for unclaimed_structure in UnclaimedStructures(structures):
        site_id = unclaimed_structure[0]
        unclaimed_sites[site_id] = sites[site_id]
    return unclaimed_sites

def UnclaimedStructures(structures):
    return [structure for structure in structures if structure[4] == -1]

def MyStructures(structures):
    return [structure for structure in structures if structure[4] == 0]

def MyStructuresOfType(structures, type_number):
    return [structure for structure in structures if structure[4] == 0 and structure[3] == type_number]

def ArbitraryValue(dictionary):
    return next(iter(dictionary.values()))

def StringifyStructures(structures):
    structures_string = ""
    for structure in structures:
        structures_string = structures_string + " " + str(structure[0])
    return structures_string

def SitesOfStructures(sites, structures):
    structure_sites = {}
    for structure in structures:
        structure_sites[structure[0]] = sites[structure[0]]
    return structure_sites

def SquaredDistance(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2












#####################-------------------------------------------------------------------------------------------#####################
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
#
#
num_sites = int(input())
sites = {}
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = (site_id, x, y, radius)

# game loop
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    structures = []
    for i in range(num_sites):
        # ignore_1: used in future leagues
        # ignore_2: used in future leagues
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        structures.append((site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2))
    
    num_units = int(input())
    units = []
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        units.append((x, y, owner, unit_type, health))
    
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    # First line: A valid queen action
    # Second line: A set of training instructions
    print (QueenAction(gold, touched_site, sites, structures, units))
    print (TrainingInstructions(gold, touched_site, sites, structures, units))
#
#
#####################-------------------------------------------------------------------------------------------#####################











#    if (touched_site != -1):
#        print("BUILD " + str(touched_site) + " BARRACKS-KNIGHT")
#        print("TRAIN " + str(touched_site))
#    else:
#        print("MOVE " + str(sites[0][1]) + " " + str(sites[0][2]))
#        print("TRAIN")
