#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'queensAttack' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER k
#  3. INTEGER r_q
#  4. INTEGER c_q
#  5. 2D_INTEGER_ARRAY obstacles
#

def down_diagonal(r, c):
    return r+c-1

def up_diagonal(r, c, n):
    if r>=c:
        return r-c+1
    else:
        return n+c-r

def queensAttack(n, k, r_q, c_q, obstacles):
    row_start = 1
    row_end = n
    column_start = 1
    column_end = n
    down_diagonal_start = max(1, down_diagonal(r_q, c_q)-n+1) #column
    down_diagonal_end = down_diagonal(r_q, c_q) if down_diagonal(r_q, c_q) <= n else n
    up_diagonal_start = up_diagonal(r_q, c_q, n) if up_diagonal(r_q, c_q, n) <= n else 1
    up_diagonal_end = min(n, 2*n-up_diagonal(r_q, c_q, n)) #row
    #print(down_diagonal_start)
    #print(down_diagonal_end)
    #print(up_diagonal_start)
    #print(up_diagonal_end)
    
    for obstacle in obstacles:
        r_o, c_o = obstacle
        if r_o == r_q:
            if c_o > c_q:
                row_end = min(row_end, c_o-1)
            else:
                row_start = max(row_start, c_o+1)
        if c_o == c_q:
            if r_o > r_q:
                column_end = min(column_end, r_o-1)
            else:
                column_start = max(column_start, r_o+1)
        if down_diagonal(r_o, c_o) == down_diagonal(r_q, c_q):
            if c_o > c_q:
                row_end = min(row_end, c_o-1)
            else:
                row_start = max(row_start, c_o+1)
        if up_diagonal(r_o, c_o, n) == up_diagonal(r_q, c_q, n):
            if r_o > r_q:
                column_end = min(column_end, r_o-1)
            else:
                column_start = max(column_start, r_o+1)
    
    print(row_end)
    print(row_start)
    print(column_end)
    print(column_start)
    print(up_diagonal_end)
    print(up_diagonal_start)
    print(down_diagonal_end)
    print(down_diagonal_start)

    rows = [["." if (i+j)%2==0 else " " for i in range(n)] for j in range(n)]
    for obstacle in obstacles:
        rows[obstacle[1]][obstacle[0]] = "X"
    rows[r_q][c_q] = "Q"
    for row in rows:
        print(''.join(row))
    
    return row_end - row_start + column_end - column_start + up_diagonal_end - up_diagonal_start + down_diagonal_end - down_diagonal_start
        

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    second_multiple_input = input().rstrip().split()

    r_q = int(second_multiple_input[0])

    c_q = int(second_multiple_input[1])

    obstacles = []

    for _ in range(k):
        obstacles.append(list(map(int, input().rstrip().split())))

    result = queensAttack(n, k, r_q, c_q, obstacles)

    #fptr.write(str(result) + '\n')

    #fptr.close()
