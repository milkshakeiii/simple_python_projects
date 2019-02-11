# -*- coding: utf-8 -*-
import numpy as np
import copy


def solve(board, pents):
    board = -board
    pents = copy.deepcopy(pents)
    unassigned_pent_idxs = set([get_pent_idx(pent) for pent in pents])
    solution = []

    return smarter_backtrack(board, unassigned_pent_idxs, pents, solution)


def smarter_backtrack(board, unassigned_pent_idxs, pents, solution):
    print(board)
    
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

    assign_me_idx = select_unassigned_variable(board, unassigned_pent_idxs, pents, first_uncovered_square)
    print (assign_me_idx)
    if assign_me_idx == -1:
        return False
    
    assigned_pent_idxs = set([assign_me_idx])

    for placement in order_possible_placements(assign_me_idx, board, pents, first_uncovered_square):
        print (placement)
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
                print(rotation, position)
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
                    print(rotation, position)
                    if (add_pentomino(board, rotation, position)):
                        remove_pentomino(board, rotation)
                        return get_pent_idx(rotation)

    return -1


def smarter_inference(board, unassigned_pent_idxs, assigned_pent_idxs, pents):
    return True

    


def bad_solve(board, pents):
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

    print(len(domains[1]))
    
    result = backtrack(board, set([get_pent_idx(pent) for pent in pents]), copy.deepcopy(pents), domains, [])
    return result


def backtrack(board, unassigned_pent_idxs, all_pents, domains, solution):
    if len(unassigned_pent_idxs) == 0:
        return solution if check_correctness(solution, board, all_pents) else False
    
    width = len(board)
    height = len(board[0])

    assigned_pent_idxs = set()
    assign_me = list(unassigned_pent_idxs)[0]
    placement_options = domains[assign_me]
    assigned_pent_idxs.add(assign_me)

    for option in placement_options:
        if add_pentomino(board, option[0], option[1]):
            #print (board)
            new_domains = copy.deepcopy(domains)
            inference_success = AC3(board, unassigned_pent_idxs - assigned_pent_idxs, assigned_pent_idxs, new_domains, all_pents)
            if inference_success:
                result = backtrack(board, unassigned_pent_idxs - assigned_pent_idxs, all_pents, new_domains, solution + [option])
                if result:
                    return result
                
        for pent_idx in assigned_pent_idxs:
            remove_pentomino(board, all_pents[pent_idx])

    return False


def AC3(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents):
    #returns true iff the board seems arc consistent
    queue = []
    for pent1 in unassigned_pent_idxs:
        for pent2 in unassigned_pent_idxs:
            if pent1 != pent2:
                queue.append((pent1, pent2))

    width = len(board)
    height = len(board[0])
    for key in domains.keys():
        domains[key] = []
    for pent in [all_pents[idx] for idx in unassigned_pent_idxs]:
        for x in range(width):
            for y in range(height):
                pent_rotations = rotated_versions(pent)
                for rotation in pent_rotations:
                    if add_pentomino(board, rotation, (x, y)):
                        option = (rotation, (x, y))
                        domains[get_pent_idx(pent)].append(option)
                        remove_pentomino(board, rotation)

    print(board)
    while len(queue) > 0:
        pent1_idx, pent2_idx = queue.pop()
        #print (len(queue))
        pent1, pent2 = all_pents[pent1_idx], all_pents[pent2_idx]
        if revise(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents, pent1_idx, pent2_idx):
            if len(domains[pent1_idx]) == 0:
                return False
            for pent3 in unassigned_pent_idxs - set([pent2]):
                queue.add((pent3, pent1))
    #print(board)
            
    return True


def revise(board, unassigned_pent_idxs, assigned_pent_idxs, domains, all_pents, pent1_idx, pent2_idx):
    #revise the domain of pent1 to be consistent with pent2.  return True iff revisions are made.
    revised = False
    new_domain = []

    for option_x in domains[pent1_idx]:
        some_y_exists = False
        
        for option_y in domains[pent2_idx]:
            if not add_pentomino(board, option_y[0], option_y[1]):
                raise Exception("Invalid option in domain")
            if add_pentomino(board, option_x[0], option_x[1]):
                some_y_exists = True
                if get_pent_idx(option_x[0]) == 0:
                    raise Exception("ack")
                if get_pent_idx(option_y[0]) == 0:
                    raise Exception("ack")
                remove_pentomino(board, option_x[0])
                remove_pentomino(board, option_y[0])
                break
            remove_pentomino(board, option_y[0])
        if some_y_exists:
            new_domain.append(option_x)

    domains[pent1_idx] = new_domain

    return revised


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
