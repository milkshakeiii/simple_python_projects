def answer(x, y, n):
    return tabular_bidirectional_totals(n)[x][y]
    
#returns a two dimensional array of total number of permutations
#for n rabbits with x visible from one side and y from the other
def tabular_bidirectional_totals(n):

    #start with base cases
    tabled_ns = [ [[0, 1]], [[0, 0], [0, 1]] ]

    #for n and x, the list of permutations by y (as index) is:
    #sum(tabled_ns[n-1]), shift by 2-x
    #multiply permutations by (y/1 ... y/x-1)
    
    for tabled_n in range(2, n+1):
        totals_by_x_y = [ [0 for i in range(tabled_n+1)] ]
        
        previous_totals = tabled_ns[tabled_n-1]
        sum_of_previous = [0 for i in range(len(previous_totals[0]))]
        for by_y in previous_totals:
            for i in range(len(by_y)):
                sum_of_previous[i] += by_y[i]

        #shift by 2-x by adding 2, then shifting back 1 for each x
        previous_totals_by_y = [0, 0] + sum_of_previous
        
        for x in range(1, tabled_n+1):

            totals_by_y = [0 for i in range(tabled_n+1)]
                
            for y in range(tabled_n+1):

                divisor = x - 1
                multiplier = y
                if divisor == 0:
                    divisor = 1
                    multiplier = 1
                      
                totals_by_y[y] = int(previous_totals_by_y[y+1] * multiplier / divisor)
                
            previous_totals_by_y = totals_by_y + [0]
            totals_by_x_y.append(totals_by_y)

        tabled_ns.append(totals_by_x_y)

    return tabled_ns[n]


