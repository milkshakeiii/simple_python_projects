T = int(input())
for i in range(T):
    rows = []
    for j in range(3):
        rows.append(list(map(int,input().split())))
    sums = []
    sums.append(rows[1][0] + rows[1][1])
    sums.append(rows[0][1] + rows[2][1])
    sums.append(rows[0][0] + rows[2][2])
    sums.append(rows[0][2] + rows[2][0])
    averages = {}
    for asum in sums:
        if asum%2 == 0:
            averages[asum//2] = averages.get(asum//2, 0) + 1
    progressions = max(list(averages.values()) + [0])
    if rows[0][1] == (rows[0][0] + rows[0][2]) / 2:
        progressions += 1
    if rows[2][1] == (rows[2][0] + rows[2][2]) / 2:
        progressions += 1
    if rows[1][0] == (rows[0][0] + rows[2][0]) / 2:
        progressions += 1
    if rows[1][1] == (rows[0][2] + rows[2][2]) / 2:
        progressions += 1
    print("Case #" + str(i+1) + ": " + str(progressions))
