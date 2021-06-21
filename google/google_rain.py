def answer(heights):
    if len(heights) <= 1:
        return 0
    
    divide = max(heights)
    divide_index = heights.index(divide)
    
    left = heights[:divide_index]
    right = heights[divide_index+1:]

    right.reverse()
    return held_water(left) + held_water(right)
    
def held_water(heights):
    #consider a hut group with a wall on the right side
    #the water it holds is equal to the water from the max height hut
    #to the huts below it, from the max height hut to the wall on the right

    #that max height hut then becomes a wall to the right for the huts
    #to the left of it, and we use the same process on those huts to the left
    
    if len(heights) <= 1:
        return 0
    
    divide = max(heights)
    divide_index = heights.index(divide)
    
    left = heights[:divide_index]
    right = heights[divide_index:]
    
    held_water_total = 0
    for height in right:
        held_water_total = held_water_total + (divide - height)
    
    return held_water_total + held_water(left)
