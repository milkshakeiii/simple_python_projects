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

    width = len(board)
    height = len(board[0])
    domains = {}
    for pent in pents:
        for x in range(width):
            for y in range(height):
                pent_rotations = rotated_versions(pent)
                for rotation in pent_rotations:
                    if add_pentomino(board, rotation, (x, y)):
                        option = (rotation, (x, y))
                        if get_pent_idx(pent) not in domains:
                            domains[get_pent_idx(pent)] = [option]
                        domains[get_pent_idx(pent)].append(option)
                        remove_pentomino(board, rotation)
    
    result = backtrack(board, set([get_pent_idx(pent) for pent in pents]), copy.deepcopy(pents), domains, [])
    return result


def backtrack(board, unassigned_pent_idxs, all_pents, domains, solution):
    if len(unassigned_pent_idxs) == 0:
        return solution if check_correctness(solution, board, all_pents) else False
    
    width = len(board)
    height = len(board[0])

    placement_options = domains[list(unassigned_pent_idxs)[0]]

    for option in placement_options:
        assigned_pent_idxs = set()
        if add_pentomino(board, option[0], option[1]):
            assigned_pent_idxs.add(get_pent_idx(option[0]))
            inference_success = AC-3(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents)
            if inference_success:
                result = backtrack(board, unassigned_pent_idxs - assigned_pent_idxs, all_pents, domains, solution + [option])
                if result:
                    return result
                
        for pent_idx in assigned_pent_idxs:
            remove_pentomino(board, all_pents[pent_idx])

    return False


def AC-3(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents):
    queue = []
    for pent1 in unassigned_pent_idxs:
        for pent2 in unassigned_pent_idxs:
            queue.add((pent1, pent2))

    while len(queue) > 0:
        pent1_idx, pent2_idx = queue.pop()
        pent1, pent2 = all_pents[pent1_idx], all_pents[pent2_idx]
        if revise(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents, pent1, pent2):
            if len(domains[pent1_idx]) == 0:
                return False
            for pent3 in unassigned_pent_idxs - set([pent2]):
                queue.add((pent3, pent1))
            
    return True


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
                    remove_pentomino(board, pent)
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True


def remove_pentomino(board, pent):
    pent_idx = get_pent_idx(pent)
    board[board==pent_idx+1] = -1


def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1

        
def check_correctness(sol_list, board, pents):
    # All tiles used
    if len(sol_list) != len(pents):
        return False

    if -1 in board:
        return False
    
    return True
