from time import sleep
from math import inf
from random import randint
from collections import Counter
import copy, cProfile

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.winnerMyUtility=-10000
        self.twoInARowMyUtility=-500
        self.cornerMyUtility=-30
        self.preventThreeInARowMyUtility=-100
	
        self.expandedNodes=0
        self.currPlayer=True


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        if isMax:
            if self.count_3_in_a_row(self.maxPlayer) > 0:
                return self.winnerMaxUtility
            elif self.count_2_in_a_row(self.maxPlayer) > 0 or self.count_preventions(self.maxPlayer, self.minPlayer) > 0:
                return self.twoInARowMaxUtility*self.count_2_in_a_row(self.maxPlayer) + self.preventThreeInARowMaxUtility*self.count_preventions(self.maxPlayer, self.minPlayer)
            else:
                return self.cornerMaxUtility*self.count_corners(self.maxPlayer)
        else:
            if self.count_3_in_a_row(self.minPlayer) > 0:
                return self.winnerMinUtility
            elif self.count_2_in_a_row(self.minPlayer) > 0 or self.count_preventions(self.minPlayer, self.maxPlayer) > 0:
                return self.twoInARowMinUtility*self.count_2_in_a_row(self.minPlayer) + self.preventThreeInARowMinUtility*self.count_preventions(self.minPlayer, self.maxPlayer)
            else:
                return self.cornerMinUtility*self.count_corners(self.minPlayer)

    def evaluateDesignedSimple(self, isMax, currBoardIdx):
        return self.checkWinner()

    def evaluateDesigned(self, isMax, currBoardIdx):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                                 True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # possible 3-in-row locations
        winList = {(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)}
        score = 0
        for bId in self.globalIdx:
                num3InRow = 0
                num2InRow = 0
                numPrevent = 0
                numCorner = 0
                for w in winList:
                        outcomes = [self.board[bId[0]+(w[i]//3)][bId[1]+(w[i]%3)] for i in range(3)]
                        nums = Counter(outcomes)
                        if nums['O'] == 3 or nums['X'] == 3:
                                num3InRow += 1
                                if nums['O'] == 3:
                                        score += self.winnerMyUtility
                                else:
                                        score += -self.winnerMyUtility
                                break
                        elif nums['O'] == 2 and nums['_'] == 1:
                                num2InRow += 1
                        elif nums['X'] == 2 and nums['O'] == 1:
                                numPrevent += 1

                if not num3InRow:
                        if num2InRow or numPrevent:
                                score += num2InRow*self.twoInARowMyUtility + numPrevent*self.preventThreeInARowMyUtility

                        else:
                                if self.board[bId[0]][bId[1]] == 'O':
                                        numCorner += 1
                                if self.board[bId[0]][bId[1]+2] == 'O':
                                        numCorner += 1
                                if self.board[bId[0]+2][bId[1]] == 'O':
                                        numCorner += 1
                                if self.board[bId[0]+2][bId[1]+2] == 'O':
                                        numCorner += 1

                                score += numCorner*self.cornerMyUtility
        return score
        

    def evaluateDesignedMCTS(self, isMax, currBoardIdx):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        original_board = copy.deepcopy(self.board)
        score=0
        for i in range(20): #play out this many random games
            self.board =  copy.deepcopy(original_board)
            simulated_player = not self.currPlayer
            while (self.checkMovesLeft() and self.checkWinner() == 0 and self.checkLocalMoveLeft(currBoardIdx)):
                offsets = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
                idx = self.globalIdx[currBoardIdx]
                squares = [(idx[0] + offset[0], idx[1] + offset[1]) for offset in offsets]
                empty_spots = [spot for spot in squares if self.board[spot[0]][spot[1]] == '_']
                if len(empty_spots) == 0:
                    raise Exception("empty board despite check")
                
                rand_idx = randint(0, len(empty_spots)-1)
                empty_spot = empty_spots[rand_idx]
                self.board[empty_spot[0]][empty_spot[1]] = self.maxPlayer if simulated_player else self.minPlayer
                currBoardIdx = squares.index(empty_spot)
                simulated_player = not simulated_player
                
            score += self.checkWinner()

        self.board = original_board
        return score

    def evaluateExtraCredit(self, isMax):
        check = self.checkExtraCreditWinner()
        if check != 0:
            return float('inf') * check
        
        if isMax:
            value = 0
            value += self.count_3_in_a_row(self.maxPlayer) * 5000
            value += self.count_2_in_a_row(self.maxPlayer) * 100
            value -= self.count_3_in_a_row(self.minPlayer) * 2500
            value -= self.count_2_in_a_row(self.minPlayer) * 50
            return value
        else:
            value = 0
            value += self.count_3_in_a_row(self.maxPlayer) * 5000
            value += self.count_2_in_a_row(self.maxPlayer) * 100
            value -= self.count_3_in_a_row(self.minPlayer) * 2500
            value -= self.count_2_in_a_row(self.minPlayer) * 50
            return value
        
    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for row in self.board:
            for entry in row:
                if entry == '_':
                    return True
        return False

    def checkLocalMoveLeft(self, localBoardIdx):
        idx = self.globalIdx[localBoardIdx]
        
        local_board = [self.board[idx[0]+0][idx[1]],
                       self.board[idx[0]+0][idx[1]+1],
                       self.board[idx[0]+0][idx[1]+2],
                       self.board[idx[0]+1][idx[1]],
                       self.board[idx[0]+1][idx[1]+1],
                       self.board[idx[0]+1][idx[1]+2],
                       self.board[idx[0]+2][idx[1]],
                       self.board[idx[0]+2][idx[1]+1],
                       self.board[idx[0]+2][idx[1]+2]]

        return local_board.count('_') > 0

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        if self.count_3_in_a_row(self.maxPlayer) > 0:
            return 1
        if self.count_3_in_a_row(self.minPlayer) > 0:
            return -1
        return 0

    def checkExtraCreditWinner(self):
        original_board = copy.deepcopy(self.board)
        mini_board = []
        offsets = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        
        for i in range(9):
            local_winner = self.checkLocalWinner(i)
            if local_winner == 1:
                mini_board.append('X')
            elif local_winner == -1:
                mini_board.append('O')
            else:
                mini_board.append('_')

        self.board = [['_'] * 9 for i in range(9)]
        for i in range(9):
            offset = offsets[i]
            self.board[offset[0]][offset[1]] = mini_board[i]

        result = None
        if self.count_3_in_a_row(self.maxPlayer) > 0:
            result = 1
        elif self.count_3_in_a_row(self.minPlayer) > 0:
            result = -1
        else:
            result = 0

        self.board = original_board
        return result

    def checkLocalWinner(self, i):
        originalBoard = copy.deepcopy(self.board)
        offsets = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        idx = self.globalIdx[i]
        self.board = [['_'] * 9 for i in range(9)]
        for offset in offsets:
            self.board[idx[0]+offset[0]][idx[1]+offset[1]] = originalBoard[idx[0]+offset[0]][idx[1]+offset[1]]
        winner = 0
        if self.count_3_in_a_row(self.maxPlayer):
            winner = 1
        elif self.count_3_in_a_row(self.minPlayer):
            winner = -1
        self.board = originalBoard
        return winner

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        return self.general_alphabeta(depth, currBoardIdx, alpha, beta, isMax, False)

    def general_alphabeta(self,depth,currBoardIdx,alpha,beta,isMax,minIsDesigned):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        self.expandedNodes += 1

        if depth >= 3 or not self.checkMovesLeft() or self.checkWinner() != 0 or not self.checkLocalMoveLeft(currBoardIdx):
            if isMax:
                return self.evaluatePredifined(True)
            elif not minIsDesigned:
                return self.evaluatePredifined(False)
            else:
                return self.evaluateDesigned(False, currBoardIdx)

        if self.currPlayer:
            value = float('-inf')
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                marker = self.board[idx[0] + offset[0]][idx[1] + offset[1]]
                if marker == '_':
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = self.maxPlayer
                    self.currPlayer = False
                    new_value = self.general_alphabeta(depth+1, i, alpha, beta, isMax, minIsDesigned)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = '_'
                    if (alpha >= beta):
                        break
            return value
        else:
            value = float('inf')
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                marker = self.board[idx[0] + offset[0]][idx[1] + offset[1]]
                if marker == '_':
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = self.minPlayer
                    self.currPlayer = True
                    new_value = self.general_alphabeta(depth+1, i, alpha, beta, isMax, minIsDesigned)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = '_'
                    if (alpha >= beta):
                        break
            return value

        return bestValue

    def extracredit_alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):

        self.expandedNodes += 1

        if depth >= 3 or not self.checkMovesLeft() or self.checkExtraCreditWinner() != 0:
            if isMax:
                return self.evaluateExtraCredit(True)
            else:
                return self.evaluateExtraCredit(False)

        if self.currPlayer:
            value = float('-inf')
            for move in self.getECLegalMoves(currBoardIdx):
                self.board[move[0]][move[1]] = self.maxPlayer
                self.currPlayer = False
                new_value = self.extracredit_alphabeta(depth+1, move[2], alpha, beta, isMax)
                value = max(value, new_value)
                alpha = max(alpha, value)
                self.board[move[0]][move[1]] = '_'
                if (alpha >= beta):
                    break
            return value
        else:
            value = float('inf')
            for move in self.getECLegalMoves(currBoardIdx):
                self.board[move[0]][move[1]] = self.minPlayer
                self.currPlayer = True
                new_value = self.extracredit_alphabeta(depth+1, move[2], alpha, beta, isMax)
                value = min(value, new_value)
                beta = min(beta, value)
                self.board[move[0]][move[1]] = '_'
                if (alpha >= beta):
                    break
            return value

        return bestValue

    #based off pseudocode from wikipedia
    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        
        output:
        bestValue(float):the bestValue that current player may have
        """
        self.expandedNodes += 1
        
        if depth >= 3 or not self.checkMovesLeft() or self.checkWinner() != 0 or not self.checkLocalMoveLeft(currBoardIdx):
            return self.evaluatePredifined(isMax)

        if self.currPlayer:
            value = float('-inf')
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                marker = self.board[idx[0] + offset[0]][idx[1] + offset[1]]
                if marker == '_':
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = self.maxPlayer
                    self.currPlayer = False
                    new_value = self.minimax(depth+1, i, isMax)
                    value = max(value, new_value)
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = '_'
            return value
        else:
            value = float('inf')
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                marker = self.board[idx[0] + offset[0]][idx[1] + offset[1]]
                if marker == '_':
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = self.minPlayer
                    self.currPlayer = True
                    new_value = self.minimax(depth+1, i, isMax)
                    value = min(value, new_value)
                    self.board[idx[0] + offset[0]][idx[1] + offset[1]] = '_'
            return value

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        return self.generalPlayGame(maxFirst, 4, isMinimaxOffensive, isMinimaxDefensive, False)

    def generalPlayGame(self, maxFirst, startingBoard, isMinimaxMax, isMinimaxMin, minIsDesigned, quiet=True):
        bestMoves=[]
        bestValues=[]
        gameBoards=[]
        expandedNodesList=[]
        winner=0

        currIsMax = maxFirst
        currBoardIdx = startingBoard
        while (self.checkWinner() == 0 and self.checkMovesLeft() and self.checkLocalMoveLeft(currBoardIdx)):
            if not quiet:
                print("---")
                printGameBoard(self.my_board)
            
            self.expandedNodes = 0
            move_evaluations = []
            
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                move_coord = (idx[0] + offset[0], idx[1] + offset[1])
                marker = self.board[move_coord[0]][move_coord[1]]
                if marker == '_':
                    self.board[move_coord[0]][move_coord[1]] = self.maxPlayer if currIsMax else self.minPlayer
                    self.currPlayer = not currIsMax
                    if (currIsMax and isMinimaxMax) or (not currIsMax and isMinimaxMin):
                        evaluation = self.minimax(1, i, currIsMax)
                    else:
                        evaluation = self.general_alphabeta(1, i, float('-inf'), float('inf'), currIsMax, minIsDesigned)
                    move_evaluations.append((evaluation, i, move_coord))
                    
                    self.board[move_coord[0]][move_coord[1]] = '_'

            if currIsMax:
                best_move = max(move_evaluations, key=lambda eval: (eval[0], -eval[1]))
            else:
                best_move = min(move_evaluations)

            if not quiet:
                print("Move evaluations:")
                print(move_evaluations)

            bestMoves.append((currBoardIdx, best_move[2]))
            expandedNodesList.append(self.expandedNodes)
            bestValues.append(best_move[0])

            self.board[best_move[2][0]][best_move[2][1]] = (self.maxPlayer if currIsMax else self.minPlayer)
            gameBoards.append(copy.deepcopy(self.board))
            currIsMax = not currIsMax
            currBoardIdx = best_move[1]

            #printGameBoard(self.my_board)
            #print("- - -")

        winner = self.checkWinner()
        
        return gameBoards, bestMoves, expandedNodesList, bestValues, winner


    def playExtraCreditGame(self, maxFirst, startingBoard):
        bestMoves=[]
        bestValues=[]
        gameBoards=[]
        expandedNodesList=[]
        winner=0

        currIsMax = maxFirst
        currBoardIdx = startingBoard
        while (self.checkExtraCreditWinner() == 0 and self.checkMovesLeft()):
            
            self.expandedNodes = 0
            move_evaluations = []

            move_evaluations = []
            legal_moves = self.getECLegalMoves(currBoardIdx)

            if len(legal_moves) == 0:
                break
            
            for move_coord in legal_moves:
                self.currPlayer = not currIsMax
                self.board[move_coord[0]][move_coord[1]] = self.maxPlayer if currIsMax else self.minPlayer
                evaluation = self.extracredit_alphabeta(1, move_coord[2], float('-inf'), float('inf'), currIsMax)
                move_evaluations.append((evaluation, move_coord[2], move_coord))
                self.board[move_coord[0]][move_coord[1]] = '_'

            if currIsMax:
                best_move = max(move_evaluations, key=lambda eval: (eval[0], -eval[1]))
            else:
                best_move = min(move_evaluations)

            bestMoves.append((currBoardIdx, best_move[2]))
            gameBoards.append(copy.deepcopy(self.board))
            expandedNodesList.append(self.expandedNodes)
            bestValues.append(best_move[0])

            self.board[best_move[2][0]][best_move[2][1]] = (self.maxPlayer if currIsMax else self.minPlayer)
            currIsMax = not currIsMax
            currBoardIdx = best_move[1]

            #printGameBoard(self.my_board)
            #print("- - -")

        winner = self.checkExtraCreditWinner()
        gameBoards.append(copy.deepcopy(self.board))
        
        return gameBoards, bestMoves, expandedNodesList, bestValues, winner

    def getECLegalMoves(self, currBoardIdx):
        legal_moves = []
                                         
        if self.checkLocalWinner(currBoardIdx) == 0:
            for i in range(9):
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                move_coord = (idx[0] + offset[0], idx[1] + offset[1])
                marker = self.board[move_coord[0]][move_coord[1]]
                if marker == '_':
                    legal_moves.append((move_coord[0], move_coord[1], i))
        if len(legal_moves) == 0:
            for boardno in range(9):
                if self.checkLocalWinner(boardno) != 0:
                        continue
                for i in range(9):
                    offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                    idx = self.globalIdx[boardno]
                    move_coord = (idx[0] + offset[0], idx[1] + offset[1])
                    marker = self.board[move_coord[0]][move_coord[1]]
                    if marker == '_':
                        legal_moves.append((move_coord[0], move_coord[1], i))

        return legal_moves

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        maxFirst = randint(0, 1)
        startingBoard = randint(0, 8)
        if maxFirst:
            print ("Offensive agent starts")
        else:
            print ("My agent starts")
        print ("starting board: " + str(startingBoard))
        
        gameBoards, bestMoves, self.expandedNodes, bestValues, winner = self.generalPlayGame(maxFirst, startingBoard, False, False, True)
        
        return gameBoards, bestMoves, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        bestMoves=[]
        bestValues=[]
        gameBoards=[]
        expandedNodesList=[]
        winner=0

        currIsPlayer = randint(0, 1)
        currBoardIdx = randint(0, 8)
        while (self.checkWinner() == 0 and self.checkMovesLeft() and self.checkLocalMoveLeft(currBoardIdx)):
            print("---" + ("Player" if currIsPlayer else "Designed") + "---")
            print("local board: " + str(currBoardIdx))
            printGameBoard(self.board)
            
            self.expandedNodes = 0
            move_evaluations = []

            if not currIsPlayer:
                for i in range(9):
                    offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                    idx = self.globalIdx[currBoardIdx]
                    move_coord = (idx[0] + offset[0], idx[1] + offset[1])
                    marker = self.board[move_coord[0]][move_coord[1]]
                    if marker == '_':
                        self.board[move_coord[0]][move_coord[1]] = self.minPlayer
                        self.currPlayer = not currIsPlayer
                        evaluation = self.general_alphabeta(1, i, float('-inf'), float('inf'), False, True)
                        move_evaluations.append((evaluation, i, move_coord))
                        
                        self.board[move_coord[0]][move_coord[1]] = '_'

                best_move = min(move_evaluations)
            else:
                i = int(input())
                offset = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][i]
                idx = self.globalIdx[currBoardIdx]
                move_coord = (idx[0] + offset[0], idx[1] + offset[1])
                best_move = (0, i, move_coord)

            bestMoves.append((currBoardIdx, best_move[2]))
            gameBoards.append(copy.deepcopy(self.board))
            expandedNodesList.append(self.expandedNodes)
            bestValues.append(best_move[0])

            self.board[best_move[2][0]][best_move[2][1]] = (self.maxPlayer if currIsPlayer else self.minPlayer)
            currIsPlayer = not currIsPlayer
            currBoardIdx = best_move[1]
            gameBoards.append(copy.deepcopy(self.board))

            #printGameBoard(self.my_board)
            #print("- - -")

        winner = self.checkWinner()
        
        return gameBoards, bestMoves, winner

        
    def count_corners(self, player_marker):
        count = 0
        for idx in self.globalIdx:
            local_board = [self.board[idx[0]+0][idx[1]],
                           self.board[idx[0]+0][idx[1]+1],
                           self.board[idx[0]+0][idx[1]+2],
                           self.board[idx[0]+1][idx[1]],
                           self.board[idx[0]+1][idx[1]+1],
                           self.board[idx[0]+1][idx[1]+2],
                           self.board[idx[0]+2][idx[1]],
                           self.board[idx[0]+2][idx[1]+1],
                           self.board[idx[0]+2][idx[1]+2]]
            
            if (local_board[0] == player_marker):
                count += 1
            if (local_board[2] == player_marker):
                count += 1
            if (local_board[6] == player_marker):
                count += 1
            if (local_board[8] == player_marker):
                count += 1
        return count


    def count_preventions(self, player_marker, enemy_marker):
        preventions = set()
        for idx in self.globalIdx:
            local_board = [self.board[idx[0]+0][idx[1]],
                           self.board[idx[0]+0][idx[1]+1],
                           self.board[idx[0]+0][idx[1]+2],
                           self.board[idx[0]+1][idx[1]],
                           self.board[idx[0]+1][idx[1]+1],
                           self.board[idx[0]+1][idx[1]+2],
                           self.board[idx[0]+2][idx[1]],
                           self.board[idx[0]+2][idx[1]+1],
                           self.board[idx[0]+2][idx[1]+2]]
            
            #  XX_
            if (local_board[0] == local_board[1] == enemy_marker) and (local_board[2] == player_marker):
                preventions.add(2)
            if (local_board[3] == local_board[4] == enemy_marker) and (local_board[5] == player_marker):
                preventions.add(5)
            if (local_board[6] == local_board[7] == enemy_marker) and (local_board[8] == player_marker):
                preventions.add(8)

            #  _XX
            if (local_board[1] == local_board[2] == enemy_marker) and (local_board[0] == player_marker):
                preventions.add(0)
            if (local_board[4] == local_board[5] == enemy_marker) and (local_board[3] == player_marker):
                preventions.add(3)
            if (local_board[7] == local_board[8] == enemy_marker) and (local_board[6] == player_marker):
                preventions.add(6)

            #  X_X
            if (local_board[0] == local_board[2] == enemy_marker) and (local_board[1] == player_marker):
                preventions.add(1)
            if (local_board[3] == local_board[5] == enemy_marker) and (local_board[4] == player_marker):
                preventions.add(4)
            if (local_board[6] == local_board[8] == enemy_marker) and (local_board[7] == player_marker):
                preventions.add(7)

            #  X
            #  X
            #  _
            if (local_board[0] == local_board[3] == enemy_marker) and (local_board[6] == player_marker):
                preventions.add(6)
            if (local_board[1] == local_board[4] == enemy_marker) and (local_board[7] == player_marker):
                preventions.add(7)
            if (local_board[2] == local_board[5] == enemy_marker) and (local_board[8] == player_marker):
                preventions.add(8)

            #  _
            #  X
            #  X
            if (local_board[3] == local_board[6] == player_marker) and (local_board[0] == player_marker):
                preventions.add(0)
            if (local_board[4] == local_board[7] == player_marker) and (local_board[1] == player_marker):
                preventions.add(1)
            if (local_board[5] == local_board[8] == player_marker) and (local_board[2] == player_marker):
                preventions.add(2)

            #  X
            #  _
            #  X
            if (local_board[0] == local_board[6] == enemy_marker) and (local_board[3] == player_marker):
                preventions.add(3)
            if (local_board[1] == local_board[7] == enemy_marker) and (local_board[4] == player_marker):
                preventions.add(4)
            if (local_board[2] == local_board[8] == enemy_marker) and (local_board[5] == player_marker):
                preventions.add(5)

            #  X__
            #  ___
            #  __X
            if (local_board[0] == local_board[8] == enemy_marker) and (local_board[4] == player_marker):
                preventions.add(4)

            #  __X
            #  ___
            #  X__
            if (local_board[2] == local_board[6] == enemy_marker) and (local_board[4] == player_marker):
                preventions.add(4)

            #  X
            #  _X
            #  ___
            if (local_board[2] == local_board[4] == enemy_marker) and (local_board[6] == player_marker):
                preventions.add(6)
            if (local_board[6] == local_board[4] == enemy_marker) and (local_board[2] == player_marker):
                preventions.add(2)
            if (local_board[0] == local_board[4] == enemy_marker) and (local_board[8] == player_marker):
                preventions.add(8)
            if (local_board[8] == local_board[4] == enemy_marker) and (local_board[0] == player_marker):
                preventions.add(0)

        return len(preventions)
            


    def count_3_in_a_row(self, player_marker):
        count = 0
        for idx in self.globalIdx:
            local_board = [self.board[idx[0]+0][idx[1]],
                           self.board[idx[0]+0][idx[1]+1],
                           self.board[idx[0]+0][idx[1]+2],
                           self.board[idx[0]+1][idx[1]],
                           self.board[idx[0]+1][idx[1]+1],
                           self.board[idx[0]+1][idx[1]+2],
                           self.board[idx[0]+2][idx[1]],
                           self.board[idx[0]+2][idx[1]+1],
                           self.board[idx[0]+2][idx[1]+2]]
            
            #  XXX
            if (local_board[0] == local_board[1] == local_board[2] == player_marker):
                count += 1
            if (local_board[3] == local_board[4] == local_board[5] == player_marker):
                count += 1
            if (local_board[6] == local_board[7] == local_board[8] == player_marker):
                count += 1

            #  X
            #  X
            #  X
            if (local_board[0] == local_board[3] == local_board[6] == player_marker):
                count += 1
            if (local_board[1] == local_board[4] == local_board[7] == player_marker):
                count += 1
            if (local_board[2] == local_board[5] == local_board[8] == player_marker):
                count += 1

            #  X__       __X
            #  _X_  and  _X_
            #  __X       X__
            if (local_board[0] == local_board[4] == local_board[8] == player_marker):
                count += 1
            if (local_board[2] == local_board[4] == local_board[6] == player_marker):
                count += 1


        return count


    def count_2_in_a_row(self, player_marker):
        count = 0
        for idx in self.globalIdx:
            local_board = [self.board[idx[0]+0][idx[1]],
                           self.board[idx[0]+0][idx[1]+1],
                           self.board[idx[0]+0][idx[1]+2],
                           self.board[idx[0]+1][idx[1]],
                           self.board[idx[0]+1][idx[1]+1],
                           self.board[idx[0]+1][idx[1]+2],
                           self.board[idx[0]+2][idx[1]],
                           self.board[idx[0]+2][idx[1]+1],
                           self.board[idx[0]+2][idx[1]+2]]
            
            #  XX_
            if (local_board[0] == local_board[1] == player_marker) and (local_board[2] == '_'):
                count += 1
            if (local_board[3] == local_board[4] == player_marker) and (local_board[5] == '_'):
                count += 1
            if (local_board[6] == local_board[7] == player_marker) and (local_board[8] == '_'):
                count += 1

            #  _XX
            if (local_board[1] == local_board[2] == player_marker) and (local_board[0] == '_'):
                count += 1
            if (local_board[4] == local_board[5] == player_marker) and (local_board[3] == '_'):
                count += 1
            if (local_board[7] == local_board[8] == player_marker) and (local_board[6] == '_'):
                count += 1

            #  X_X
            if (local_board[0] == local_board[2] == player_marker) and (local_board[1] == '_'):
                count += 1
            if (local_board[3] == local_board[5] == player_marker) and (local_board[4] == '_'):
                count += 1
            if (local_board[6] == local_board[8] == player_marker) and (local_board[7] == '_'):
                count += 1

            #  X
            #  X
            #  _
            if (local_board[0] == local_board[3] == player_marker) and (local_board[6] == '_'):
                count += 1
            if (local_board[1] == local_board[4] == player_marker) and (local_board[7] == '_'):
                count += 1
            if (local_board[2] == local_board[5] == player_marker) and (local_board[8] == '_'):
                count += 1

            #  _
            #  X
            #  X
            if (local_board[3] == local_board[6] == player_marker) and (local_board[0] == '_'):
                count += 1
            if (local_board[4] == local_board[7] == player_marker) and (local_board[1] == '_'):
                count += 1
            if (local_board[5] == local_board[8] == player_marker) and (local_board[2] == '_'):
                count += 1

            #  X
            #  _
            #  X
            if (local_board[0] == local_board[6] == player_marker) and (local_board[3] == '_'):
                count += 1
            if (local_board[1] == local_board[7] == player_marker) and (local_board[4] == '_'):
                count += 1
            if (local_board[2] == local_board[8] == player_marker) and (local_board[5] == '_'):
                count += 1

            #  X__
            #  ___
            #  __X
            if (local_board[0] == local_board[8] == player_marker) and (local_board[4] == '_'):
                count += 1

            #  __X
            #  ___
            #  X__
            if (local_board[2] == local_board[6] == player_marker) and (local_board[4] == '_'):
                count += 1

            #  X
            #  _X
            #  ___
            if (local_board[2] == local_board[4] == player_marker) and (local_board[6] == '_'):
                count += 1
            if (local_board[6] == local_board[4] == player_marker) and (local_board[2] == '_'):
                count += 1
            if (local_board[0] == local_board[4] == player_marker) and (local_board[8] == '_'):
                count += 1
            if (local_board[8] == local_board[4] == player_marker) and (local_board[0] == '_'):
                count += 1

        return count

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

def printGameBoard(board):
    """
    This function prints the current game board.
    """
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in board[:3]])+'\n')
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in board[3:6]])+'\n')
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in board[6:9]])+'\n')


if __name__=="__main__":

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("Max (minimax) vs Min (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
    
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,True)
    print("Min (minimax) vs Max (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
    
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,True)
    print("Max (alphabeta) vs Min (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,False)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("Max (minimax) vs Min (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    print("Max (alphabeta) vs Min (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,False)
    print("Min (alphabeta) vs Max (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,False,True)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("Min (minimax) vs Max (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,False,False)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("Min (alphabeta) vs Max (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    for i in range(20):
        uttt=ultimateTicTacToe()
        gameBoards, bestMove, winner=uttt.playGameYourAgent()
        print("MyHeuristic vs. Offensive.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
        printGameBoard(gameBoards[-1])
'''
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, winner=uttt.playGameHuman()
    print("Human vs. designed.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(False, 5)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Min first, starting board 5.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(False, 8)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Min first, starting board 8.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(True, 5)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Max first, starting board 5.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(True, 8)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Max first, starting board 8.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")


    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(True, 4)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Max first, starting board 4.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playExtraCreditGame(False, 4)
    printGameBoard(gameBoards[-1])
    print(expandedNodes)
    print("EC: Min first, starting board 4.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
'''
