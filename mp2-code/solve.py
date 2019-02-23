# -*- coding: utf-8 -*-
import numpy as np

# def exactCover(X,Y,ans = []):
# 	if not X:
# 		return ans
# 	else:
# 		x1 = min(X, key = lambda x1: len(X[x1])) #choose the col with least num rows
# 		for y1 in X[x1]:
# 			ans.append(y1)

def exactCover(X, Y, solution=[]):
	if not X:
		yield list(solution)
	else:
		c = min(X, key=lambda c: len(X[c]))
		for r in X[c]:
			solution.append(r)
			cols = removeRows(X, Y, r)
			for s in exactCover(X, Y, solution):
				yield s
			addRowsBack(X, Y, r, cols)
			solution.pop()


def removeRows(X, Y, r):
	cols = []
	for j in Y[r]:
		for i in X[j]:
			for k in Y[i]:
				if k != j:
					X[k].remove(i)
		cols.append(X.pop(j))
	return cols

def addRowsBack(X, Y, r, cols):
	for j in reversed(Y[r]):
		X[j] = cols.pop()
		for i in X[j]:
			for k in Y[i]:
				if k != j:
					X[k].add(i)

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
	myPents = np.copy(pents)

	numPents = len(myPents)
	X = {i: set() for i in range(numPents)} #first 0-numPents-1 cols for myPents

	#storing board valid locations in cols
	validCells = np.transpose(np.nonzero(board))
	for i in validCells:
		X[board.shape[1]*i[0] + i[1] + numPents] = set()

	#initialize Y or rows as dict
	Y = {}
	countY = 0 #keeps count of num of rows, key of dict Y

	#dict to store rows in required return format
	formattedDict = {}

	for p in range(numPents):
		configSeen = []
		for flipNum in range(3):
			if flipNum == 0:
				currPent = np.copy(myPents[p])
			if flipNum > 0:
				currPent = np.flip(myPents[p],flipNum-1)
				seen = 0
				for cs in configSeen:
					if np.array_equal(cs,currPent):
						seen = 1
						break
				if seen:
					break
			for rotNum in range(4):
				# check pent validity and store X and Y for each cell on board
				for r in range(board.shape[0]):
					if r+currPent.shape[0] > board.shape[0]:
						break
					for c in range(board.shape[1]):
						if c+currPent.shape[1] > board.shape[1]:
							break

						validCurr = 1
						Y[countY] = []
						for pr in range(currPent.shape[0]):
							for pc in range(currPent.shape[1]):
								if currPent[pr][pc] != 0:
									if board[r+pr][c+pc] == 0:
										validCurr = 0
										break
									else:
										Y[countY].append((r+pr)*board.shape[1]+(c+pc)+numPents) #added col corr to cell
							else:
								continue
							break #if validCurr == 0,break out of both loops & choose next c

						if validCurr == 0:
							del Y[countY]
							continue

						else:
							#add it to X,Y
							Y[countY].append(p) #added col corr to pent
							for s in Y[countY]:
								X[s].add(countY)
							#add to formattedDict
							formattedDict[countY] = (np.copy(currPent),(r,c))
							#next row in table
							countY += 1

				configSeen.append(np.copy(currPent))
				currPent = np.rot90(currPent)
				seen = 0
				for cs in configSeen:
					if np.array_equal(cs,currPent):
						seen = 1
						break
				if seen:
					break

	returnList = []

	for solution in exactCover(X, Y, []):
		for r in solution:
			returnList.append(formattedDict[r])
			#if len(returnList) == numPents:
		return returnList
