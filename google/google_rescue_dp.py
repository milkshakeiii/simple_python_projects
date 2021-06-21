import math

def answer(food, grid):

    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1

    
    known_costs = { (0, 0) : [0] }
    #save known costs to squares here so that we don't repeat work

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if (x, y) == (0, 0):
                continue
            
            food_in_room = grid[y][x]
            paths_from_left = [cost + food_in_room for cost in possible_costs(x-1, y, known_costs)]
            paths_from_up = [cost + food_in_room for cost in possible_costs(x, y-1, known_costs)]

            #use a set, ignoring duplicates so that we don't get bogged down in multiples
            known_costs[(x, y)] = set(paths_from_left + paths_from_up)
            #print(known_costs[x, y])

    possible_costs_to_exit = known_costs[(y_max, x_max)]

    lowest_remaining = math.inf
    for possible_cost in possible_costs_to_exit:
        food_remaining = food - possible_cost
        if (food_remaining >= 0 and food_remaining < lowest_remaining):
            lowest_remaining = food_remaining

    if (lowest_remaining == math.inf):
        return -1
    else:
        return lowest_remaining



def possible_costs(x, y, known_costs):
    return known_costs.get((x, y), [])
