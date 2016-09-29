def answer(food, grid):
    if len(grid) == 0 or len(grid[0]) == 0:
        raise Exception("Invalid grid.  Don't do this to me, man.")
    if (food > 200):
        raise Exception("That's too much food.  200 max")
    
    best_path = best_path_from(0, 0, food, grid)

    if best_path == 201:
        return -1
    else:
        return best_path
        

def best_path_from(x, y, food, grid):
    #print ("exploring room " + str(x) + ", " + str(y))
    
    this_square_cost = grid[y][x]
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    
    if this_square_cost > food:
        print ("ran out of food in square " + str(x) + ", " + str(y))
        return 201
        
    food = food - this_square_cost
    
    next_rooms = []
    if x != max_x:
        next_rooms.append((x+1, y))
        #print ("exploring right")
    if y != max_y:
        next_rooms.append((x, y+1))
        #print ("exploring down")
    if len(next_rooms) == 0:
        #print ("found a way out with " + str(food) + " food remaining")
        return food
    
    return min([best_path_from(room[0], room[1], food, grid) for room in next_rooms])
