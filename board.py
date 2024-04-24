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

        # set the board
        self.board = list(range(rows))
        for i in range(rows):
            self.board[i] = list(range(cols))

        # set all the places in the board to be empty boxes
       
       # set the mines
       for i in range(mines):

           # choose a random row and col
           
           # make sure that isn't already a bomb

           # set it to be a bomb

           # add a count to all surrounding squares (i-1 to i+1, etc)


    # to start the time
    def Start(self):
        self.time = time.time()        

    # to show all tiles next to the one chosen
    def Reveal(self, row, col):
        pass

    # to flag a square as a mine
    def Flag(self, row, col):
        pass

    # to uncover a square
    def Show(self, row, col):
        pass

    # to print the board for easy viewing
    def Print(self):

        # start the return
        ret = ""
        
        for i in range(self.rows + 1):
            for j in range(self.cols + 1):
                
                # see if it is one of the edges
                if i == 0:
                    ret += " {} ".format(j % 10)
                elif j == 0:
                    ret += " {} ".format(i % 10)
                else:
                    # grab the square's value
                    ret += self.board[i - 1][j - 1].Print()
            
            ret += "\n"

        # add the time and the number of mines
        ret += "\n\nMines: {}\nTime: {}".format(self.mines, time.time() - self.time)

        return ret

        
