T = int(input())
for i in range(T):
    N, C = map(int,input().split())
    ups = {}
    downs = {}
    for j in range(N):
        L, R = map(int,input().split())
        ups[L+1] = ups.get(L+1, 0) + 1
        downs[R] = downs.get(R, 0) + 1
    active_intervals = {}

    change_points = set(list(ups.keys()) + list(downs.keys()))
    change_points = list(sorted(change_points))
    last_integer = 1
    current_active_intervals = 0
    for integer in change_points:
        active_intervals[current_active_intervals] = active_intervals.get(current_active_intervals, 0) + (integer-last_integer)
        current_active_intervals += ups.get(integer, 0)
        current_active_intervals -= downs.get(integer, 0)
        last_integer = integer
        
    active_intervals = list(active_intervals.items())
    active_intervals = list(sorted(active_intervals))
    additional_intervals = 0
    while C > 0 and len(active_intervals) > 0:
        biggest_amount, biggest_count = active_intervals.pop()
        cuts_made = min(C, biggest_count)
        C -= cuts_made
        additional_intervals += biggest_amount*cuts_made
    result = N + additional_intervals
    print("Case #" + str(i+1) + ": " + str(result))
    
