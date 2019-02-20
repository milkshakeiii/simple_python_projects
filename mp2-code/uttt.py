from time import sleep
from math import inf
from random import randint
import copy

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
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

    def evaluateDesigned(self, isMax, currBoardIdx):
        return self.checkWinner()

    def evaluateDesignedMC(self, isMax, currBoardIdx):
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
            while (self.checkMovesLeft() and self.checkWinner() == 0):
                localBoard = self.board[currBoardIdx]
                empty_spots = [i for i in range(len(localBoard)) if localBoard[i] == '_']
                if len(empty_spots) == 0:
                    open_boards = [i for i in range(len(self.board)) if self.board[i].count('_') > 0]
                    currBoardIdx = open_boards[randint(0, len(open_boards)-1)]
                    localBoard = self.board[currBoardIdx]
                    empty_spots = [i for i in range(len(localBoard)) if localBoard[i] == '_']
                
                rand_idx = randint(0, len(empty_spots)-1)
                empty_spot = empty_spots[rand_idx]
                localBoard[empty_spot] = self.maxPlayer if simulated_player else self.minPlayer
                currBoardIdx = empty_spots[rand_idx]
                simulated_player = not simulated_player
                
            score += self.checkWinner()

        self.board = original_board
        return score

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
        
        
        if depth == 0 or not self.checkMovesLeft or self.checkWinner() != 0:
            if isMax:
                return self.evaluatePredifined(True)
            elif not minIsDesigned:
                return self.evaluatePredifined(False)
            else:
                return self.evaluateDesigned(False, currBoardIdx)

        self.expandedNodes += 1

        if self.currPlayer:
            value = float('-inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.maxPlayer
                    self.currPlayer = False
                    new_value = self.general_alphabeta(depth-1, i, alpha, beta, isMax, minIsDesigned)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    self.board[currBoardIdx][i] = '_'
                    if (alpha >= beta):
                        break
            return value
        else:
            value = float('inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.minPlayer
                    self.currPlayer = True
                    new_value = self.general_alphabeta(depth-1, i, alpha, beta, isMax, minIsDesigned)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    self.board[currBoardIdx][i] = '_'
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
        
        if depth == 0 or not self.checkMovesLeft() or self.checkWinner() != 0:
            return self.evaluatePredifined(isMax)

        if self.currPlayer:
            value = float('-inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.maxPlayer
                    self.currPlayer = False
                    new_value = self.minimax(depth-1, i, isMax)
                    value = max(value, new_value)
                    self.board[currBoardIdx][i] = '_'
            return value
        else:
            value = float('inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.minPlayer
                    self.currPlayer = True
                    new_value = self.minimax(depth-1, i, isMax)
                    value = min(value, new_value)
                    self.board[currBoardIdx][i] = '_'
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
        while (self.checkWinner() == 0 and self.checkMovesLeft()):
            if not quiet:
                print("---")
                printGameBoard(self.board)
            
            self.expandedNodes = 0
            move_evaluations = []
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.maxPlayer if currIsMax else self.minPlayer
                    self.currPlayer = not currIsMax
                    if (currIsMax and isMinimaxMax) or (not currIsMax and isMinimaxMin):
                        evaluation = self.minimax(3, i, currIsMax)
                    else:
                        evaluation = self.general_alphabeta(3, i, float('-inf'), float('inf'), currIsMax, minIsDesigned)
                    move_evaluations.append((evaluation, i))
                    
                    self.board[currBoardIdx][i] = '_'

            if currIsMax:
                best_move = max(move_evaluations, key=lambda eval: (eval[0], -eval[1]))
            else:
                best_move = min(move_evaluations)

            if not quiet:
                print("Move evaluations:")
                print(move_evaluations)

            bestMoves.append((currBoardIdx, best_move[1]))
            gameBoards.append(copy.deepcopy(self.board))
            expandedNodesList.append(self.expandedNodes)
            bestValues.append(best_move[0])

            self.board[currBoardIdx][best_move[1]] = (self.maxPlayer if currIsMax else self.minPlayer)
            currIsMax = not currIsMax
            currBoardIdx = best_move[1]

            #printGameBoard(self.board)
            #print("- - -")

        winner = self.checkWinner()
        gameBoards.append(copy.deepcopy(self.board))
        
        return gameBoards, bestMoves, expandedNodesList, bestValues, winner

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
        while (self.checkWinner() == 0 and self.checkMovesLeft()):
            print("---" + ("Player" if currIsPlayer else "Designed") + "---")
            print("local board: " + str(currBoardIdx))
            printGameBoard(self.board)
            
            self.expandedNodes = 0
            move_evaluations = []

            if not currIsPlayer:
                for i in range(len(self.board[currBoardIdx])):
                    marker = self.board[currBoardIdx][i]
                    if marker == '_':
                        self.board[currBoardIdx][i] = self.minPlayer
                        self.currPlayer = not currIsPlayer
                        evaluation = self.general_alphabeta(3, i, float('-inf'), float('inf'), False, True)
                        move_evaluations.append((evaluation, i))
                        
                        self.board[currBoardIdx][i] = '_'

                best_move = min(move_evaluations)
            else:
                square = int(input())
                best_move = (0, square)

            bestMoves.append((currBoardIdx, best_move[1]))
            gameBoards.append(copy.deepcopy(self.board))
            expandedNodesList.append(self.expandedNodes)
            bestValues.append(best_move[0])

            self.board[currBoardIdx][best_move[1]] = (self.maxPlayer if currIsPlayer else self.minPlayer)
            currIsPlayer = not currIsPlayer
            currBoardIdx = best_move[1]

            #printGameBoard(self.board)
            #print("- - -")

        winner = self.checkWinner()
        gameBoards.append(copy.deepcopy(self.board))
        
        return gameBoards, bestMoves, winner

        
    def count_corners(self, player_marker):
        count = 0
        for local_board in self.board:
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
        for local_board in self.board:
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
        for local_board in self.board:
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
        for local_board in self.board:
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
        printGameBoard(self.board)

def printGameBoard(board):
        """
        This function prints the current game board.
        """
        for k in [0, 3, 6]:
            for l in [0, 3, 6]:
                for i in range(3):
                    for j in range(3):
                        print(board[k+i][l+j], end='')
                    print(" ", end='')
                print("")
            print("")


if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, winner=uttt.playGameHuman()
    print("Human vs. designed.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    
    '''
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    print("Max (minimax) vs Min (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
    
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,True)
    print("Min (minimax) vs Max (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
    
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,True)
    print("Max (alphabeta) vs Min (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
    
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,False)
    print("Max (minimax) vs Min (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    print("Max (alphabeta) vs Min (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,False)
    print("Min (alphabeta) vs Max (minimax).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,False,True)
    print("Min (minimax) vs Min (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,False,False)
    print("Min (alphabeta) vs Max (alphabeta).  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")

    for i in range(20):
        uttt=ultimateTicTacToe()
        gameBoards, bestMove, winner=uttt.playGameYourAgent()
        print("MyHeuristic vs. Offensive.  Winner: " + str(winner) + " in " + str(len(bestMove)) + " turns.")
        printGameBoard(gameBoards[-1])
    '''
