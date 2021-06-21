#!/bin/python3

import sys

def solution(n, A):
    indexes_by_integer = {}

    for i in range(0, n):
        indexes_by_integer[A[i]] = indexes_by_integer.get(A[i], []) + [i]

    minimum_gap = float("inf")
    for value_group in indexes_by_integer.values():
        previous = value_group[0]
        if len(value_group) == 1:
            continue
        for index in value_group[1:]:
            if abs(index-previous) < minimum_gap:
                minimum_gap = abs(index-previous)
            previous = index

    return minimum_gap if minimum_gap != float("inf") else -1
        
n = int(input().strip())
A = [int(A_temp) for A_temp in input().strip().split(' ')]
print(solution(n, A))
