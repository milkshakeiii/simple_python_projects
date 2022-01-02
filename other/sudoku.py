import pandas
import numpy as np

def series_satisfied(series):
    return sorted(series) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
            
def is_solved(sudoku):
    sudoku_satisfied = True
    
    for row in sudoku.iterrows():
        sudoku_satisfied = series_satisfied(row[1]) and sudoku_satisfied

    for column in sudoku.iteritems():
        sudoku_satisfied = series_satisfied(column[1]) and sudoku_satisfied

    boxes = []
    boxes.append(sudoku[0:3][[0, 1, 2]])
    boxes.append(sudoku[0:3][[3, 4, 5]])
    boxes.append(sudoku[0:3][[6, 7, 8]])
    boxes.append(sudoku[3:6][[0, 1, 2]])
    boxes.append(sudoku[3:6][[3, 4, 5]])
    boxes.append(sudoku[3:6][[6, 7, 8]])
    boxes.append(sudoku[6:9][[0, 1, 2]])
    boxes.append(sudoku[6:9][[3, 4, 5]])
    boxes.append(sudoku[6:9][[6, 7, 8]])
    flat_boxes = [pandas.Series([item for row in box.values for item in row]) for box in boxes]
    for flat_box in flat_boxes:
        sudoku_satisfied = series_satisfied(flat_box) and sudoku_satisfied
    
    return sudoku_satisfied

def exhaustive_solve(sudoku):
    if (is_solved(sudoku)):
        return sudoku
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for k in range(1, 10):
                    sudoku[i][j] = k
                    result = solve(sudoku)
                    if (result != None):
                            return result
                    sudoku[i][j] = 0
    return None

def full_sudoku():
    s = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
         [6, 7, 2, 1, 9, 5, 3, 4, 8],
         [1, 9, 8, 3, 4, 2, 5, 6, 7],
         [8, 5, 9, 7, 6, 1, 4, 2, 3],
         [4, 2, 6, 8, 5, 3, 7, 9, 1],
         [7, 1, 3, 9, 2, 4, 8, 5, 6],
         [9, 6, 1, 5, 3, 7, 2, 8, 4],
         [2, 8, 7, 4, 1, 9, 6, 3, 5],
         [3, 4, 5, 2, 8, 6, 1, 7, 9]]
    sudoku = Sudoku()
    sudoku.rows = s
    return sudoku

def unsolved_sudoku():
    s = [[0, 9, 0, 0, 0, 6, 0, 4, 0],
         [0, 0, 5, 3, 0, 0, 0, 0, 8],
         [0, 0, 0, 0, 7, 0, 2, 0, 0],
         [0, 0, 1, 0, 5, 0, 0, 0, 3],
         [0, 6, 0, 0, 0, 9, 0, 7, 0],
         [2, 0, 0, 0, 8, 4, 1, 0, 0],
         [0, 0, 3, 0, 1, 0, 0, 0, 0],
         [8, 0, 0, 0, 0, 2, 5, 0, 0],
         [0, 5, 0, 4, 0, 0, 0, 8, 0]]
    sudoku = Sudoku()
    sudoku.rows = s
    return sudoku
    
class Sudoku():
    def __init__(self):
        self.rows = [[0]*9 for i in range(9)]

    def __str__(self):
        s = ""
        for row in self.rows:
            s = s + str(row) + '\n'
        return s

    def unassigned_coord(self):
        for i in range(9):
            for j in range(9):
                if self.rows[j][i] == 0:
                    return (i, j)
        return None

    def possible_values(self, x, y):
        row = self.rows[y]
        column = [each_row[x] for each_row in self.rows]
        box_x_start = (x//3)*3
        box_y_start = (y//3)*3
        box_rows = self.rows[box_y_start:box_y_start+3]
        box = []
        for each_row in box_rows:
            box.append(each_row[box_x_start])
            box.append(each_row[box_x_start+1])
            box.append(each_row[box_x_start+2])
        possible_values = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for value in row+column+box:
            if value in possible_values:
                possible_values.remove(value)
        return possible_values

def smart_solve(sudoku):
    if sudoku.unassigned_coord() == None:
        return sudoku
    x, y = sudoku.unassigned_coord()
    for value in sudoku.possible_values(x, y):
        sudoku.rows[y][x] = value
        result = smart_solve(sudoku)
        if result != None:
            return result
        sudoku.rows[y][x] = 0
    return None
