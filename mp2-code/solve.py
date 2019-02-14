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
    
    board = copy.deepcopy(board)
    pents = copy.deepcopy(pents)

    #rotating the board ensures that the algorithm always fills in dominos along SHORT axis first.
    #because of the way pentominoes are shaped, many immediately create unfillable holes when
    #placed near walls.  filling in the short axis first ensures that we search the area around
    #a pentomino for unfillable squares soon after placing the pentomino.  this prevents early
    #undetected failure and drastically increases performance of the algorithm.
    rotated = False
    if (board.shape[0] < board.shape[1]):
        rotated = True
        board = np.rot90(board)

    width = len(board)
    height = len(board[0])
    
    unassigned_pent_idxs = set([i for i in range(len(pents))])
    solution = []
    rotated_versions(0, pents[0], reset_memos = True)
    square_pents_to_options, bin_to_pent_retrieval = build_options_dict(copy.deepcopy(board), pents)

    bin_board = board_to_binary(1 - board)
    result = backtrack(bin_board,
                       width,
                       height,
                       1,
                       unassigned_pent_idxs,
                       pents,
                       solution,
                       square_pents_to_options)
    result = [bin_to_pent_retrieval[placement] for placement in result]
    if rotated:
        result = [(np.flip(np.rot90(placement[0]), 0), (placement[1][1], placement[1][0])) for placement in result]
    return result


def backtrack(board,
              width,
              height,
              first_uncovered_square,
              unassigned_pent_idxs,
              pents,
              solution,
              square_pents_to_options):
    '''
    This algorithm has a lot of similarities to Donald Knuth's "Algorithm X."  The main difference
    is this algorithm does not delete subsets which cover members that have already been covered.
    Instead, it reduces the occurence of overlap by covering the farthest/lowest square at each
    step and only considering dominos which cover exclusively nearer/higher squares than the square
    being considered.
    '''
    
    if (len(unassigned_pent_idxs) == 0):
        return solution

    #find the first square with no collision starting from a corner and choosing the farthest/
    #bottemest square at each step.
    #because of this selection heuristic we always choose a square in a corner maximally
    #surrounded by filled squares.
    #this is a form of "least remaining values" heuristic since
    #thre are fewer ways to place dominoes around borders.
    while (first_uncovered_square&board):
        first_uncovered_square *= 2

    for assign_me_idx in unassigned_pent_idxs:
        assigned_pent_idxs = set([assign_me_idx])
        
        if (first_uncovered_square, assign_me_idx) not in square_pents_to_options:
            continue #this piece won't ever fit here
        
        for placement in square_pents_to_options[(first_uncovered_square, assign_me_idx)]:
            if placement&board: #there is an overlap
                continue

            #bitwise or | will do an intersection AKA place the piece
            result = backtrack(placement|board,
                               width,
                               height,
                               first_uncovered_square,
                               unassigned_pent_idxs - assigned_pent_idxs,
                               pents,
                               solution + [(placement, assign_me_idx)],
                               square_pents_to_options)
            if result:
                return result

    return False


def square_to_positional(x, y, width, height):
    return 2**(height*(width-x) - y - 1)


def order_possible_placements(assign_me_idx, board, pents, square):
    placements = []
    for rotation in rotated_versions(assign_me_idx, pents[assign_me_idx]):
        x = square[0] - rotation.shape[0] + 1
        last_row = rotation[-1]
        first_square = max([i for i in range(len(last_row)) if last_row[i] != 0])
        y = square[1] - first_square
        position = (x, y)
        if (add_pentomino(board, rotation, assign_me_idx, position)):
            board.fill(0)
            placements.append((rotation, position))
    
    return placements


def in_bounds(placement, board):
    pent = placement[0]
    x, y = placement[1]
    return not (x < 0 or
                y < 0 or
                x + pent.shape[0] - 1 >= board.shape[0] or
                y + pent.shape[1] - 1 >= board.shape[1])


def build_options_dict(board, pents):
    board.fill(0)
    square_pents_to_options = {}
    bin_to_pent_retrieval = {}
    width = board.shape[0]
    height = board.shape[1]

    for x in range(width):
        for y in range(height):
            for pent_idx in range(len(pents)):
                possible_placements = order_possible_placements(pent_idx, board, pents, (x, y))
                for placement in possible_placements:
                    if not (add_pentomino(board, placement[0], pent_idx, placement[1])):
                        raise Exception("invalid placement")
                    else:
                        positional = square_to_positional(x, y, width, height)
                        if (positional, pent_idx) not in square_pents_to_options:
                            square_pents_to_options[positional, pent_idx] = []
                        binary = board_to_binary(board)
                        square_pents_to_options[positional, pent_idx].append(binary)
                        bin_to_pent_retrieval[(binary, pent_idx)] = placement
                        board.fill(0)

    return square_pents_to_options, bin_to_pent_retrieval


def board_to_binary(board):
    binary = 0
    i = 0
    for row in reversed(range(len(board))):
        for column in reversed(range(len(board[row]))):
            if board[row][column] != 0:
                binary += 2**i
            i = i+1

    return binary
        
    
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
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap or zero-covering
                    for square in assigned_squares:
                        board[square[0]][square[1]] = 0
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
                    assigned_squares.append((coord[0]+row, coord[1]+col))
    return True


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


def bin_print(n, width):
    print("")
    s = bin(n)
    for i in range(1, len(s)-1):
        print(s[-i], end='')
        if (i)%width == 0:
            print("")
    print("")
