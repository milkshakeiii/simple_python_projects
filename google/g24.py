def one_dimensional_meet_and_party(positions, weight_changes):
    running_sums = 0
    last_position = position_weight_changes[0][0]
    weight = 0
    for position, change in zip(positions, weight_changes):
        running_sums.append(running_sums[-1] + (position - last_position) * weight)
        weight += change
        last_position = position

    end_sum = running_sums[-1]
    low_index = binary_search(running_sums, end_sum/2)
    start_sum = running_sums[low_index]
    max_inclusions = running_sums[low_index+1]
    left = positions[low_index]
    right = position[low_index+1]
    while left <= right:
        center = (right+left)//2
        this_sum = start_sum+weight*(center-positions[low_index]+1)
        if this_sum == end_sum/2:
            return center
        elif this_sum > end_sum/2:
            right = center-1
        elif this_sum < end_sum/2:
            left = center+1
    low_position = (right+left)//2
    low_distance = start_sum+weight*(low_position-positions[low_index]+1)
    best_position = low_position
    if abs(low_distance + weight - end_sum/2) < abs(low_distance-end_sum/2):
        best_position += 1

    
    

def binary_search(a, value):
    left = 0
    right = len(a)-1
    while left <= right:
        center = (right+left)//2
        if a[center] == value:
            return center
        elif a[center] > value:
            right = center-1
        elif a[center] < value:
            left = center+1
    return (right+left)//2

T = int(input())
for i in range(T):
    B = int(input())
    
    cornerweights = []
    weight_sum = 0
    for j in range(B):
        x1, y1, x2, y2 = map(int,input().split())
        topleft = (x1, y1)
        bottomright = (x2, y2)
        y_step = (x2-x1+1)
        x_step = (y2-y1+1)
        weight = x_step*y_step
        weight_sum += weight
        cornerweights.append((topleft, bottomright, x_step, y_step, weight))

#######
    answer_d = 0
    answer_x = None
    answer_y = None
        

        
            
          
    print("Case #" + str(i+1) + ": " + ' '.join(map(str,[answer_x, answer_y, int(answer_d)])))
