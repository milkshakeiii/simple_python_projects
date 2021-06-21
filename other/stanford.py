def brute_inversions(array):
    inversions = 0
    for i in range(len(array)):
        at_i = array[i]
        for at_j in array[i:]:
            if at_i > at_j:
                inversions += 1
    return inversions


def merge_inversions(array):
    if len(array) == 2 and array[1] < array[0]:
        return sorted(array), 1
    if len(array) == 1:
        return array, 0
    if len(array) < 1:
        raise "Why nothing"

    new_inversions = 0

    half_point = len(array)//2
    
    left_half = array[:half_point]
    left_size = len(left_half)
    
    right_half = array[half_point:]
    right_size = len(right_half)

    left_half, left_inversions = merge_inversions(left_half)
    right_half, right_inversions = merge_inversions(right_half)
    
    left_marker = left_half.pop(0)
    right_marker = right_half.pop(0)

    sorted_array = []

    
    while(True):
        if left_marker > right_marker:
            new_inversions += len(left_half) + 1
            sorted_array.append(right_marker)
            if len(right_half) > 0:
                right_marker = right_half.pop(0)
            else:
                sorted_array = sorted_array + [left_marker] + left_half
                break
        else:
            sorted_array.append(left_marker)
            if len(left_half) > 0:
                left_marker = left_half.pop(0)
            else:
                sorted_array = sorted_array + [right_marker] + right_half
                break

    return sorted_array, left_inversions + right_inversions + new_inversions

    




            
with open("hwk 1.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x.strip()) for x in content] 

print(merge_inversions(content)[1])
