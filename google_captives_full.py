import itertools, math

def tabular_answer(x, y, n):
    return tabular_bidirectional_totals(n)[x][y]

def brute_answer(x, y, n):
    if (x == y == 1):
        return 0
    if (x + y - 1 > n):
        return 0
    
    line = []
    for i in range(x):
        line.insert(0, n-i)

    for i in range(y-1):
        line.append(line[0]-i-1)

    for i in range(1, n-x-y+2):
        line.insert(1, i)

    return len(equivalences(line, visibility))


def visibility(line):
    return left_visibility(line), left_visibility(reversed(line))

def left_visibility(line):
    visibility = 0
    highest_so_far = -1
    for height in line:
        if height > highest_so_far:
            visibility += 1
            highest_so_far = height

    return visibility

def equivalences(line, equivalency):
    equivalent_lines = []
    original_visibility = equivalency(line)
    for permutation in itertools.permutations(line):
        if equivalency(permutation) == original_visibility:
            equivalent_lines.append(permutation)
    return equivalent_lines

def brute_totals(n):

    line = [i for i in range(1, n+1)]
    
    totals = [0 for i in range(len(line) + 1)]
    for permutation in itertools.permutations(line):
        totals[left_visibility(permutation)] += 1
    return totals

def brute_bidirectional_totals(n):

    line = [i for i in range(1, n+1)]

    totals = {}
    for i in range(1, n+1):
        for j in range(1, n+1):
            totals[(i, j)] = 0

    for permutation in itertools.permutations(line):
        totals[visibility(permutation)] += 1

    return totals
    
def tabular_bidirectional_totals(n):

    #start with base cases
    tabled_ns = [ [[0, 1]], [[0, 0], [0, 1]] ]

    #for n and x, the list of permutations by y (as index) is:
    #sum(tabled_ns[n-1]), shift by 2-x
    #multiply permutations by (y/1 ... y/x-1)
    
    for i in range(2, n+1):
        visibilities_by_x = [ [0 for j in range(i+1)] ]
        
        previous = tabled_ns[i-1]
        sum_of_previous = [0 for j in range(len(previous[0]))]
        for by_x in previous:
            for j in range(len(by_x)):
                sum_of_previous[j] += by_x[j]

        

        previous_visibility_by_x = [0, 0] + sum_of_previous
        
        for j in range(1, i+1):

            visibility_by_x = [0 for k in range(i+1)]
                
            for k in range(i+1):

                divisor = j - 1
                multiplier = k
                if divisor == 0:
                    divisor = 1
                    multiplier = 1
                      
                visibility_by_x[k] = int(previous_visibility_by_x[k+1] * multiplier / divisor)
                
            previous_visibility_by_x = visibility_by_x + [0]
            visibilities_by_x.append(visibility_by_x)

        tabled_ns.append(visibilities_by_x)

    return tabled_ns[n]
        
    
def visibilities_by_lower(n):
    line = [i for i in range(1, n+1)]
    visibilities = []
    for permutation in itertools.permutations(line):
        visibilities.append(visibility(permutation))
                           
    arranged_visibilities = []
    arranged_visibilities = [(min(tuple), max(tuple)) for tuple in visibilities]

    tuples_by_lower = [[0 for i in range(n+1)] for i in range(n+1)]
    for tuple in arranged_visibilities:
        tuples_by_lower[tuple[0]][tuple[1]] += 1

    return tuples_by_lower

def visibilities_by_first(n):
    line = [i for i in range(1, n+1)]
    visibilities = []
    for permutation in itertools.permutations(line):
        visibilities.append(visibility(permutation))

    tuples_by_first = [[0 for i in range(n+1)] for i in range(n+1)]
    for tuple in visibilities:
        tuples_by_first[tuple[0]][tuple[1]] += 1

    return tuples_by_first

def totals(visibilities):
    n = max(visibilities)
    totals = [0 for i in range(n+1)]
    for i in range(n+1):
        totals[i] = visibilities.count(i)

    return totals

def recursive_totals(n):

    totals = [0 for i in range(n+1)]
    
    for i in range(1, n):
        fixed_start_totals = heights_starting_from(i, n)
        for j in range(len(totals)):
            totals[j] += fixed_start_totals[j]

    totals[1] = (math.factorial(n-1))

    return totals

def tabular_totals(n):

    #the tabular method.  store the results of total possible heights here as we
    #find them.  start with a list of 1 representing undefined n = 0 and [0, 1]
    #representing the permutations of n = 1 (no permutations with 0 visible rabbits,
    #and 1 permutation with 1 visible rabbit)
    
    totals_by_n = [[1], [0, 1]]
    
    for tabled_n in range(2, n+1):
        totals_by_n.append([0 for i in range(tabled_n+1)])
        
        for start in range(1, tabled_n+1):
            analagous_totals = totals_by_n[tabled_n-start]

            #for each possible fixed starting number, the total possible heights 
            #starting with that number is that total possible heights produced by an
            #analagous lower n, times the number of extra permutations produced by
            #irrelevent lower numbers. also the heights are increased by one
            #by the fixed number

            #get the analagous heights and add 1 (count for each height is
            #stored at the index of the height) (ex. 2 heights and index 2
            #means 2 ways to make 2 visible rabbits)
            fixed_start_totals = [0 for i in range(tabled_n+1)]
            for i in range(len(analagous_totals)):
                fixed_start_totals[i+1] = analagous_totals[i]

            #account for extra permutations
            multiplier = 1
            for i in range(tabled_n-start+1, tabled_n):
                multiplier *= i
            fixed_start_totals = multiplied_list(fixed_start_totals, multiplier)

            #add the permutations for this fixed start in with the others
            for i in range(tabled_n+1):
                totals_by_n[tabled_n][i] += fixed_start_totals[i]

    return totals_by_n[n]

def simple_tabular_totals(n):

    #the tabular method.  according to a simplified recursion,
    #each n is the results of the previous n * n-1
    #plus the results of the previous n + 1
    
    totals_by_n = [[1], [0, 1]]
    
    for tabled_n in range(2, n+1):
        totals_by_n.append([0 for i in range(tabled_n+1)])
        n_minus_one = totals_by_n[tabled_n-1]
        for i in range(len(n_minus_one)):
            totals_by_n[tabled_n][i] += n_minus_one[i] * (tabled_n - 1)
            totals_by_n[tabled_n][i+1] += n_minus_one[i]

    return totals_by_n[n]


def heights_starting_from(start, n):
    if (start > n):
        raise Exception("Start out of range")
    
    if (n == 1):
        return [0, 1]
    
    if (start == n):
        return [0, math.factorial(n-1)]

    analagous_totals = recursive_totals(n-start)
    fixed_start_totals = [0 for i in range(n+1)]
    for i in range(len(analagous_totals)):
        fixed_start_totals[i+1] = analagous_totals[i]

    multiplier = 1

    for i in range(n-start+1, n):
        multiplier *= i

    fixed_start_totals = multiplied_list(fixed_start_totals, multiplier)

    return fixed_start_totals

def multiplied_list(original_list, multiplier):
    return [item*multiplier for item in original_list]
    
