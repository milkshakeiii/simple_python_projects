T = int(input())

def rational_by_number(n):
    binary = bin(n)[2:]
    result = [1, 1]
    for place in binary[1:]:
        if place == "0":
            result = [result[0], sum(result)]
        else:
            result = [sum(result), result[1]]
    return result

def number_by_rational(p, q):
    buildabinary = ""
    while (p, q) != (1, 1):
        if p < q:
            buildabinary += "0"
            q -= p
        else:
            buildabinary += "1"
            p -= q
    buildabinary = "1" + ''.join(reversed(buildabinary))
    return [int(buildabinary, base=2)]

for i in range(T):
    problem = list(map(int,input().split()))
    problem_id = problem[0]
    answer = []
    if problem_id == 1:
        n = problem[1]
        answer += rational_by_number(n)
    else:
        p, q = problem[1:]
        answer += number_by_rational(p, q)
    
    print("Case #" + str(i+1) + ": " + ' '.join(map(str,answer)))
