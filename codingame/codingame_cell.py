import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
bombs_remaining = 2

distance_table = [[0 for i in range(factory_count)] for i in range(factory_count)]
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distance_table[factory_1][factory_2] = distance
    distance_table[factory_2][factory_1] = distance

# game loop
while True:
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    factories = []
    troops = []
    bombs = []
    
    ###################################################
    ########################COLLECT STATE##############
    ###################################################
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        
        #id, owner, cyborgs, production, future_owner
        if entity_type == "FACTORY":
            factories.append((entity_id, arg_1, arg_2, arg_3, arg_1))
            
        #id, owner, source, target, cyborgs, countdown
        if entity_type == "TROOP":
            troops.append((entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
            
        #id, owner, source, target, countdown
        if entity_type == "BOMB":
            bombs.append((entity_id, arg_1, arg_2, arg_3, arg_4))
            
            
    ###################################################
    ########################PREDICT STUFF##############
    ###################################################
    for factory in factories:
        new_cyborgs = factory[2] + 0 if factory[1] == 0 else factory[3] * 10
        factories[factory[0]] = (factory[0],
                                 factory[1],
                                 factory[2],
                                 factory[3],
                                 factory[4],
                                 new_cyborgs)
    
    for troop in troops:
        target = factories[troop[3]]
        if troop[1] != target[1]:
            new_cyborgs = target[2] - troop[4]
        else:
            new_cyborgs = target[2] + troop[4]
        new_owner = target[1]
        if new_cyborgs < 0:
            new_cyborgs = -new_cyborgs
            new_owner = -new_owner
            
        factories[troop[3]] = (factories[troop[3]][0],
                               factories[troop[3]][1],
                               factories[troop[3]][2],
                               factories[troop[3]][3],
                               new_owner,
                               new_cyborgs)
                               
    for bomb in bombs:
        if (bomb[1] == 1):
            target = factories[bomb[3]]
            factories[bomb[3]] = (factories[bomb[3]][0],
                                  factories[bomb[3]][1],
                                  factories[bomb[3]][2],
                                  factories[bomb[3]][3],
                                  factories[bomb[3]][4],
                                  factories[bomb[3]][5] - min((factories[bomb[3]][2]//2, 10)))
            
            
            
    ###################################################
    ###################CAPTURE WHAT WE CAN#############
    ###################################################            

    source_factories = [factory for factory in factories if factory[1] == 1]
    if (len(source_factories) != 0):    
        targets = [factory for factory in factories if factory[1] != 1 and factory[3] != 0]
        def distance_to_nearest(target):
            distances = distance_table[target[0]]
            distances_to_friendly = []
            for factory in source_factories:
                distances_to_friendly.append(distances[factory[0]])
            return min(distances_to_friendly)
        targets = sorted(targets, key = distance_to_nearest)
        source_index = 0
        requested_cyborgs = 0        
        dispatches = [] #(source, target, number to send)
    
        
        for factory in targets:
            requested_cyborgs = factory[5] + 1;
                
            if (requested_cyborgs < source_factories[source_index][2]):
                dispatches.append((source_factories[source_index][0], factory[0], requested_cyborgs))
                source_factories[source_index] = (source_factories[source_index][0],
                                                    source_factories[source_index][1],
                                                    source_factories[source_index][2] - requested_cyborgs,
                                                    source_factories[source_index][3],
                                                    source_factories[source_index][4],
                                                    source_factories[source_index][5])
            else:
                source_index = source_index + 1
                
            if source_index >= len (source_factories):
                break
    
    
    
    
    
    
    ###################################################
    #######################BOMB AND ORDERS#############
    ###################################################
    orders = ""
    
    #bomb
    if (bombs_remaining > 0):
        for factory in factories:
            if (factory[4] == -1 and factory[2] > 25):
                print(factories, file = sys.stderr)
                source = [factory for factory in factories if factory[1] == 1][0][0]
                orders = orders + "BOMB " + str(source) + " " + str(factory[0]) + ";"
                bombs_remaining = bombs_remaining - 1
                break
    
            
    
    if (len(dispatches) == 0):
        print ("WAIT")
    else:
        for dispatch in dispatches:
            orders = orders + "MOVE " + str(dispatch[0]) + " " + str(dispatch[1]) + " " + str(dispatch[2]) + ";"
        print(orders[:-1])
    
            
        

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
