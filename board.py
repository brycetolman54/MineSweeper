# this class holds the board and all its associated parts for the game to work, including:
    # the squares.
    # the number of mines left to place,
    # the time

# import necessary parts
import random
import time
from square import Square

class Board():
    
    def __init__(self, rows, cols, mines):
        
        # make the variables accesible
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.left = rows * cols - mines
        self.start = None
        self.end = None

        # set the board
        self.board = list(range(rows))
        for i in range(rows):
            self.board[i] = list(range(cols))

        # set all the places in the board to be empty boxes
        for i in range(rows):
            for j in range(cols):
                self.board[i][j] = Square()
     
        # set the mines
        for i in range(mines):

            while True:

                # choose a random row and col
                theRow = random.randint(0, rows - 1)
                theCol = random.randint(0, cols - 1)
                theSquare = self.board[theRow][theCol]

                # make sure that isn't already a bomb
                if not theSquare.bomb:
                    break

            # set it to be a bomb
            theSquare.bomb = True

            # add a count to all surrounding squares (i-1 to i+1, etc)
            for j in range(theRow - 1, theRow + 2):
                for k in range(theCol - 1, theCol + 2):
                    if k < cols and j < rows and k >= 0 and j >= 0:
                        self.board[j][k].val += 1

    # to start the time
    def Start(self):
        self.start = time.time()        

    # to show all tiles next to the one chosen
    def Expand(self, row, col, ML=True):

        blownUp = False

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < self.rows and i >= 0 and j < self.cols and j >= 0 and not self.board[i][j].revealed and not self.board[i][j].flagged:
                    if self.Reveal(i, j, ML):
                        blownUp = True

        return blownUp

    # to flag a square as a mine
    def Flag(self, row, col):
        if not self.board[row][col].revealed:
            if self.board[row][col].flagged:
                self.board[row][col].flagged = False
                self.mines += 1
            else:
                self.board[row][col].flagged = True
                self.mines -= 1

    # to uncover a square
    def Reveal(self, row, col, ML=True):
        if not (self.board[row][col].revealed or self.board[row][col].flagged):
            self.left -= 1
            self.board[row][col].revealed = True
        if not ML and self.board[row][col].val == 0:
            self.Expand(row, col, ML)
        return self.board[row][col].bomb

    # to print the board for easy viewing
    def Print(self):

        # start the return
        ret = ""
        
        for i in range(self.rows + 1):
            ret += "\t"
            for j in range(self.cols + 1):
                
                # see if it is one of the edges
                if i == 0 and j == 0:
                    ret += "   "
                elif i == 0:
                    ret += " {} ".format(j % 10)
                elif j == 0:
                    ret += " {} ".format(i % 10)
                else:
                    # grab the square's value
                    ret += self.board[i - 1][j - 1].Print()
            
            ret += "\n\n"

        # add the time and the number of mines
        ret += "\n\n\t    Mines: {}\n\t    Time: {}".format(self.mines, int(time.time() - self.start) if self.start != None else "-")

        return ret

    def Won(self):
        if self.left == 0 and self.mines == 0:
            self.end = time.time() - self.start
            return True
        else:
            return False

        
