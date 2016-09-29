import math

def answer(N, K):
    return str(recursive_answer(N, K))

#memoized recursive method will perform similarly to tabular method
memoized_calls = {}
def recursive_answer(N, K):
    if (N, K) in memoized_calls:
        return memoized_calls[N, K]
    
    if K == N-1:
        memoized_calls[N, K] = int(math.pow(N, N-2))
        return int(math.pow(N, N-2))

    #there are n(n-1)/2 possible tunnels
    #there are n(n-1)/2 choose k choices of tunnel possible
    #subtract the number of choices that exclude warrens to find answer
    
    possible_choices = n_choose_m(N*(N-1)//2, K)
    
    for i in range(N-1):
        unconnected_choices = 0
        
        #we can shave off unnecessary solutions
        #i referenced Marko Riedel's math stackexchange post
        #(http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges/690422#690422)
        for j in range(max ( [( K - int ((float(1)/2) * (i+1) * i) ), 0] ), K-i+1):
            unconnected_choices += n_choose_m( (N-1-i)*(N-2-i)/2, j ) * recursive_answer(i + 1, K - j)

        possible_choices -= n_choose_m(N-1, i)*unconnected_choices
    

    memoized_calls[N, K] = possible_choices
    return possible_choices

memoized_binomials = {}
def n_choose_m(n, m):
    if (n, m) in memoized_binomials:
        return memoized_binomials[n, m]
    
    if (m > n):
        return 0

    binomial = int(math.factorial(n)) / int((math.factorial(n-m)*math.factorial(m)))
    memoized_binomials[n, m] = binomial
    return binomial
