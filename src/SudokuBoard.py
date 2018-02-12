import itertools
import random
import Constraint
import Variable

"""
    Represents a Sudoku Board. This is converted to a constraint network,
    so BTSolver can interface with it as a CSP.
"""

class SudokuBoard:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__( self, p = None, q = None, m = None, board = None, filepath = None ):
        self.p = p
        self.q = q
        try:
            self.N = self.p*self.q
        except:
            self.N = 9

        if board != None:
            self.board = board

        elif filepath != None:
            '''read from input file and generate gameboard'''
            with open(filepath) as f:
                lines = f.readlines()

                try:
                    self.p = int(float(lines[0].split()[0]))
                    self.q = int(float(lines[0].split()[1]))
                    self.N = self.p*self.q
                except:
                    self.p = 3
                    self.q = 3
                    self.N = 9

                self.board = []
                for i in range(1, len(lines)):
                    tempLine = []
                    for n in lines[i].split():
                        tempLine.append(self.odometerToInt(n))
                    self.board.append(tempLine)

        else:
            if m == None:
                m = 7
            if p == None:
                self.p = 3
            if q == None:
                self.q = 3
            self.N = p*q
            self.board = [[0 for j in range(self.N)] for i in range(self.N)]

            while True:
                if m <= 0:
                    break

                randomRow = random.randint(0, self.N-1)
                randomCol = random.randint(0, self.N-1)
                randomAssignment = random.randint(1, self.N)
                if self.board[randomRow][randomCol] == 0 and self.isValidValue( randomRow, randomCol, randomAssignment ):
                    self.board[randomRow][randomCol] = randomAssignment
                    m -= 1

    # ==================================================================
    # String representation
    # ==================================================================

    def __str__ ( self ):
        output = "p:" + str(self.p) + "\tq:" \
                                            + str(self.q) + "\n"
        for i in range(self.N):
            for j in range(self.N):
                try:
                    output += self.intToOdometer(self.board[i][j]) + " "
                except:
                    pass

                if (j+1) % self.q == 0 and j!=0 and j != (self.N - 1):
                    output += "| "

            output += "\n"
            if (i+1) % self.p == 0 and i!=0 and i != (self.N - 1):
                for k in range(self.N + self.p - 1):
                    output += "- "
                output += "\n"
        return output

    # ==================================================================
    # Private Helper Methods
    # ==================================================================

    def isValidValue ( self, row, col, value ):
        # check whether current value can be assigned to current variable
        return self.isValidColValue(col, value) and self.isValidRowValue(row, value) and self.isValidBlock(row, col, value)


    def isValidColValue ( self, col, value ):
        return value not in [self.board[v][col] for v in range(self.N)]


    def isValidRowValue ( self, row, value ):
        return value not in [self.board[row][v] for v in range(self.N)]


    def isValidBlock ( self, row, col, value ):
        rDiv = row // self.p;
        cDiv = col // self.q;
        for i in range(rDiv * self.p, (rDiv + 1) * self.p):
            for j in range(cDiv * self.q, (cDiv + 1) * self.q):
                if self.board[i][j] == value:
                    return False
        return True

    def intToOdometer ( self, n ):
        alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        toReturn = ''

        while n != 0:
            n, i = divmod(n, len(alphabet))
            toReturn = alphabet[i] + toReturn

        if toReturn == '':
            toReturn = '0'

        return toReturn

    def odometerToInt ( self, s ):
        try:
            return int( s, 36 )

        except:
            return 0
