from time import sleep
from math import inf
from random import randint

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

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def evaluatePredefined(self, isMax):
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

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
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
        #YOUR CODE HERE
        bestValue=0.0
        return bestValue

    #based off pseudocode from wikipedia
    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
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
            return self.evaluatePredefined(isMax)

        if isMax:
            value = float('-inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.maxPlayer
                    value = max(value, self.minimax(depth-1, i, False))
                    self.board[currBoardIdx][i] = '_'
            return value
        else:
            value = float('inf')
            for i in range(len(self.board[currBoardIdx])):
                marker = self.board[currBoardIdx][i]
                if marker == '_':
                    self.board[currBoardIdx][i] = self.minPlayer
                    value = min(value, self.minimax(depth-1, i, True))
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
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes=0
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

        
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

        return count

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
