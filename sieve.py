def primes_less_than(n):
    sieve_me = [i for i in range(0, n)]
    prime = 2
    while True:
        if prime*prime > n:
            break
        for i in range(prime*prime, n, prime):
            sieve_me[i] = -1
        prime += 1
        while (sieve_me[prime] == -1):
            prime += 1
        prime = sieve_me[prime]
    return [sieved for sieved in sieve_me if sieved not in [-1, 0, 1]]
