def V(x):
    if x == 0:
        return 0
    degree = 0
    while x%P == 0:
        degree += 1
        x /= P
    return degree

T = int(input())
for i in range(T):
    results = []
    
    N, Q, P = map(int, input().split())
    A = [0] + list(map(int,input().split()))
    Av = [V(x) for x in A]
    Am = [x%P for x in A]
    for j in range(Q):
        query = list(map(int,input().split()))
        if query[0] == 1:
            pos, val = query[1:]
            Av[pos] = V(val)
            Am[pos] = val%P
        if query[0] == 2:
            S, L, R = query[1:]
            sigma = []
            for k in range(L, R+1):
                print(Av[k]*S, Am[k]**S)
                sigma.append(Av[k]*S - Am[k]**S )
            results.append(str(sum(sigma)))
    
    
    print("Case #" + str(i+1) + ": " + ' '.join(results))
