import math

def answer(N, K):
    return str(recursive_answer(N, K))


memoized_binomials = {}
def n_choose_m(n, m):
    if (n, m) in memoized_binomials:
        return memoized_binomials[n, m]
    
    if (m > n):
        return 0

    binomial = int(math.factorial(n)) / int((math.factorial(n-m)*math.factorial(m)))
    memoized_binomials[n, m] = binomial
    return binomial
