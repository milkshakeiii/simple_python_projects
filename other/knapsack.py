w = int(input())
volumes = map(int, input().split())
weights = map(int, input().split())
n = len(volumes)
pairs = [weights[i], volumes[i] for i in range(n)]

solution_omitting_i = []
first_solution = [[] for i in range(n)]
for i in range(n):
    for j in range(n):
        candidates = []
        if pairs[i][1] == 1 and i != j:
            candidates.append(pairs[i])
    first_solution[j] = [max(candidates)]
solution_omitting_i.append(first_solution)

for j in range(1, w):
    for i in range(n):
        
