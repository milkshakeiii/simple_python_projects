# -*- coding: utf-8 -*-
import numpy as np
import copy


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """

    board = -board #avoid conflicts between place-marker 1s and 1st pentominos


    
    result = backtrack(board, copy.deepcopy(pents), copy.deepcopy(pents), [])
    return result


def backtrack(board, unassigned_pents, all_pents, solution):
    if len(unassigned_pents) == 0:
        return solution if check_correctness(solution, board, all_pents) else False
    
    width = len(board)
    height = len(board[0])

    pent = unassigned_pents.pop(0) #place me
    placement_options = []
    for x in range(width):
        for y in range(height):
            pent_rotations = rotated_versions(pent)
            for rotation in pent_rotations:
                placement_options.append((rotation, (x, y)))

    for option in placement_options:
        if add_pentomino(board, option[0], option[1]):
            solution.append(option)
            result = backtrack(board, unassigned_pents, all_pents, solution)
            if result:
                return result

    return False


def in_bounds(placement, board):
    for x in range(len(placement[0])):
        for y in range(len(placement[0][0])):
            if placement[0][x][y] != 0 and (placement[1][0] + x >= len(board) or placement[1][1] + y >= len(board[0])):
                return False
    return True    


def rotated_versions(pent):
    #returns a list of all rotated versions of the pentomino
    versions = []
    versions.append(pent)
    versions.append(np.rot90(pent))
    versions.append(np.rot90(np.rot90(pent)))
    versions.append(np.rot90(np.rot90(np.rot90(pent))))
    versions.append(np.flip(pent))
    versions.append(np.flip(np.rot90(pent)))
    versions.append(np.flip(np.rot90(np.rot90(pent))))
    versions.append(np.flip(np.rot90(np.rot90(np.rot90(pent)))))
    return versions

                        
def add_pentomino(board, pent, coord):
    if not in_bounds((pent, coord), board):
        return False
    
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap or zero-covering
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True

        
def check_correctness(sol_list, board, pents):
    # All tiles used
    if len(sol_list) != len(pents):
        return False

    if -1 in board:
        return False
    
    return True
