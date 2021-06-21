T = int(input())

for i in range(T):
    N = int(input())
    skaters = []
    cost = 0
    for j in range(N):
        skaters.append(input())
    max_skater = skaters[0]
    for j in range(1, N):
        if skaters[j] < max_skater:
            cost += 1
        else:
            max_skater = skaters[j]
    print("Case #" + str(i+1) + ": " + str(cost))
