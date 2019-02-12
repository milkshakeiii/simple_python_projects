# -*- coding: utf-8 -*-
import numpy as np
import copy

def solve(board, pents):
    board = -board
    pents = copy.deepcopy(pents)
    unassigned_pent_idxs = set([get_pent_idx(pent) for pent in pents])
    solution = []
    rotated_versions(0, pents[0], reset_memos = True)

    result = backtrack(board, unassigned_pent_idxs, pents, solution)
    #print(board)
    return result


def backtrack(board, unassigned_pent_idxs, pents, solution):
    #if (len(solution)) <= 2:
    #    print (board)
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
            if not add_pentomino(board, rotation, assign_me_idx, position):
                raise Exception("Invalid placement")
            
            result = backtrack(board, unassigned_pent_idxs - assigned_pent_idxs, pents, solution + [(rotation, position)])
            if result:
                return result
                    
            for pent_idx in assigned_pent_idxs:
                remove_pentomino(board, pent_idx)

    return False


def order_possible_placements(assign_me_idx, board, pents, first_uncovered_square):
    placements = []
    for rotation in rotated_versions(assign_me_idx, pents[assign_me_idx]):
        x = first_uncovered_square[0] - rotation.shape[0] + 1
        last_row = rotation[-1]
        first_square = min([i for i in range(len(last_row)) if last_row[i] != 0])
        y = first_uncovered_square[1] - first_square
        position = (x, y)
        if (add_pentomino(board, rotation, assign_me_idx, position)):
            remove_pentomino(board, assign_me_idx)
            placements.append((rotation, position))
    
    return placements


def in_bounds(placement, board):
    pent = placement[0]
    x, y = placement[1]
    return not (x < 0 or y < 0 or x + pent.shape[0] - 1 >= board.shape[0] or y + pent.shape[1] - 1 >= board.shape[1])


memos = {}
def rotated_versions(pent_idx, pent, reset_memos = False):
    if reset_memos:
        keys = list(memos.keys())
        for key in keys:
            del memos[key]
    if pent_idx in memos:
        return memos[pent_idx]
    
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

    memos[pent_idx] = unique_versions
    return unique_versions

                        
def add_pentomino(board, pent, pent_idx, coord):
    if not in_bounds((pent, coord), board):
        return False

    assigned_squares = []
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap or zero-covering
                    for square in assigned_squares:
                        board[square[0]][square[1]] = -1
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
                    assigned_squares.append((coord[0]+row, coord[1]+col))
    return True


def remove_pentomino(board, pent_idx):
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
