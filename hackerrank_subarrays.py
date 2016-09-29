t = int(input())
for i in range(t):
    n = int(input())
    arr = [int(item) for item in input().split()]
    
    #starting at an index, you can choose between only that index,
    #or that index, plus the best subarray starting at the next index
    best_sums = {n: float('-inf')}
    for i in range(1, n+1):
        start = n-i
        best_subarray_sum = max((arr[start], arr[start] + best_sums[start+1]))
        best_sums[start] = best_subarray_sum
    max_continuous = max(best_sums.values())
    
    #sum all positive items for max discontiguous
    #or if everything is negative take the highest one
    positive_items = [item for item in arr if item>0]
    if len(positive_items) == 0:
        max_discontiguous = max(arr)
    else:
        max_discontiguous = sum(positive_items)
    
    print(str(max_continuous) + " " + str(max_discontiguous))
