# This is a REPL that I can use to test out my minesweeper game

# get the imports that are necessary
from board import Board
import sys
import signal

# See if we have the proper args
if __name__ == '__main__':

    # allow us to CTRL+C the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # get the length of the args
    nArgs = len(sys.argv)

    # initialize the rows, cols, and mines variables
    rows = 0
    cols = 0
    mines = 0

    # get the args
    if not (nArgs == 2 or nArgs == 4):
        print("usage: python game.py <b|i|e>\n\tor\npython game.py <rows> <cols> <mines>")
        sys.exit(1)

    # see if we are doing a preassigned difficulty or creating one of our own
    if nArgs == 2:

        # get the difficulty
        diff = sys.argv[1]
        
        # set the vars for the difficult chosen
        if diff == 'b':
            rows = 9
            cols = 9
            mines = 10
        elif diff == 'i':
            rows = 16
            cols = 16
            mines = 40
        elif diff == 'e':
            rows = 16
            cols = 30
            mines = 99
        else:
            print("that is not a valid difficulty\n\tthe options are (b)eginner, (i)ntermediate, or (e)xpert")


    elif nArgs == 4:
        
        # grab the variables
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
        mines = int(sys.argv[3])

        # check that the number of mines is not too big
        if mines >= rows * cols - 1:
            print("the number of mines is too great for the board")


    # initialize the board
    b = Board(rows, cols, mines)

    b.Start()
    print(b.Print())

