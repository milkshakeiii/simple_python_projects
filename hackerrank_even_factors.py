def even_factors(N):
    if N%2 != 0:
        print("0")
    else:
        divisors = [N]
        for i in range(2, int(N**0.5)+1):
            if N%i == 0 and i%2==0:
                divisors.append(i)
            if N/i%2==0 and N/i != i:
                divisors.append(N//i)
        return sorted(divisors)

def pfs(n):
    #from http://stackoverflow.com/questions/16996217/prime-factorization-list
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac

def prime_factors_method(N):
    prime_factors = pfs(N)
    unique_prime_factors = set(prime_factors)
    permutations = 2**(len(unique_prime_factors)-1)
    duplicate_prime_factors = prime_factors[:]
    for pf in unique_prime_factors:
        duplicate_prime_factors.remove(pf)
    duplicate_2s = duplicate_prime_factors.count(2)
    permutations *= duplicate_2s + 1
    duplicate_others = set(duplicate_prime_factors)
    if 2 in duplicate_others:
        duplicate_others.remove(2)
    for duplicate_other in duplicate_others:
        duplicate_other_count = duplicate_prime_factors.count(duplicate_other)
        permutations *= 1 + duplicate_other_count/2
    print (int(permutations))

def sieve_method(N):
    print(len(even_factors(N)))
    
T = int(input())

for i in range(T):
    N = int(input())
    if (N%2 != 0):
        print ("0")
    else:
        #prime_factors_method(N)
        sieve_method(N)
