# -*- coding: utf-8 -*-
import numpy as np
import copy


def solve(board, pents):
    board = -board
    pents = copy.deepcopy(pents)
    unassigned_pent_idxs = set([get_pent_idx(pent) for pent in pents])
    solution = []

    result = smarter_backtrack(board, unassigned_pent_idxs, pents, solution)
    print(board)
    return result


def backtrack(board, unassigned_pent_idxs, pents, solution):
    if (len(solution)) <= 2:
        print (board)
    #print(unassigned_pent_idxs)
    
    if len(unassigned_pent_idxs) == 0:
        return solution if check_correctness(solution, board, pents) else False

    width = len(board)
    height = len(board[0])

    first_uncovered_square = None
    for x in range(width):
        for y in range(height):
            if board[x, y] == -1:
                first_uncovered_square = (x, y)
                break

    for assign_me_idx in unassigned_pent_idxs:
        assigned_pent_idxs = set([assign_me_idx])
        #print (assign_me_idx)
        #print (order_possible_placements(assign_me_idx, board, pents, first_uncovered_square))
        for placement in order_possible_placements(assign_me_idx, board, pents, first_uncovered_square):
            rotation = placement[0]
            position = placement[1]
            if not add_pentomino(board, rotation, position):
                raise Exception("Invalid placement")
            
            inference_success = smarter_inference(board, unassigned_pent_idxs - assigned_pent_idxs, assigned_pent_idxs, pents)
            if inference_success:
                result = smarter_backtrack(board, unassigned_pent_idxs - assigned_pent_idxs, pents, solution + [(rotation, position)])
                if result:
                    return result
                    
            for pent_idx in assigned_pent_idxs:
                remove_pentomino(board, pents[pent_idx])

    return False


def order_possible_placements(assign_me_idx, board, pents, first_uncovered_square):
    placements = []
    for rotation in rotated_versions(pents[assign_me_idx]):
        for x in range(len(rotation)):
            for y in range(len(rotation[0])):
                if rotation[x, y] == 0:
                    continue
                position = (first_uncovered_square[0] - x, first_uncovered_square[1] - y)
                if (add_pentomino(board, rotation, position)):
                    remove_pentomino(board, rotation)
                    placements.append((rotation, position))
    
    return placements


def select_unassigned_variable(board, unassigned_pent_idxs, pents, first_uncovered_square):
    for pent in [pents[i] for i in range(len(pents)) if i in unassigned_pent_idxs]:
        for rotation in rotated_versions(pent):
            for x in range(len(rotation)):
                for y in range(len(rotation[0])):
                    if rotation[x, y] == 0:
                        continue
                    position = (first_uncovered_square[0] - x, first_uncovered_square[1] - y)
                    #print(rotation, position)
                    if (add_pentomino(board, rotation, position)):
                        remove_pentomino(board, rotation)
                        return get_pent_idx(rotation)

    return -1


def smarter_inference(board, unassigned_pent_idxs, assigned_pent_idxs, pents):
    return True


def in_bounds(placement, board):
    for x in range(len(placement[0])):
        for y in range(len(placement[0][0])):
            try_x = placement[1][0] + x
            try_y = placement[1][1] + y
            if placement[0][x][y] != 0 and (try_x >= len(board) or try_y >= len(board[0]) or try_y < 0 or try_x < 0):
                return False
    return True    


def rotated_versions(pent):
    #returns a list of all rotated versions of the pentomino
    versions = []
    versions.append(pent)
    versions.append(np.rot90(pent))
    versions.append(np.rot90(np.rot90(pent)))
    versions.append(np.rot90(np.rot90(np.rot90(pent))))
    versions.append(np.flip(pent, 0))
    versions.append(np.flip(np.rot90(pent), 0))
    versions.append(np.flip(np.rot90(np.rot90(pent)), 0))
    versions.append(np.flip(np.rot90(np.rot90(np.rot90(pent))), 0))
    unique_versions = []
    for version in versions:
        unique = True
        for compare in unique_versions:
            if version.shape == compare.shape and(version == compare).all():
                unique = False
        if unique:
            unique_versions.append(version)
    return unique_versions

                        
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
