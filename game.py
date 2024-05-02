# This is a REPL that I can use to test out my minesweeper game

# get the imports that are necessary
from board import Board
import sys
import signal
import time

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


    # initialize the board and the start flag
    b = Board(rows, cols, mines)
    start = False

    # initialize colors
    red = "\u001b[38;5;160m"
    white = "\u001b[38;5;15m"
    green = "\u001b[38;5;46m"
    clear = "\u001b[H\u001b[2J"

    # Clear the screen and print the welcome message
    print(clear)
    print("\t\tWelcome to {}MineSweeper{}!".format(red, white))

    # start the repl
    resp = ""
    while not b.Won():

        # get the response
        resp = input("    ## ")
        resp = resp.split()

        if len(resp) == 0:
            continue
        elif resp[0] == "q" or resp[0] == "quit":
            break
        elif resp[0] == "h" or resp[0] == "help":
            print("""
      \u001b[4m  Commands              Purpose                                                                         \u001b[24m
          [h]elp                print a list of valid commands
          [s]tart               start the timer on the game of minesweeper (must be done before you can play)
          [e]xpand              reveal all the squares around the indicated square that are not flagged
                                    e <row> <col>
          [f]lag                flag a square as a mine
                                    f <row> <col>
          [r]eveal              uncover the indicated square to see if it is a mine
                                    r <row> <col>
          [c]lear               clear the screen and reprint the game board
                """)
        elif resp[0] == "c" or resp[0] == "clear":
            print("{}\n{}".format(clear, b.Print() if start else ""))
        elif resp[0] == "s" or resp[0] == "start":
            if start:
                print("\t{}the game has already started{}".format(red, white))
            else:
                start = True
                b.Start()
                print("\n{}".format(b.Print()))
        elif not start and resp[0] in ("e", "expand", "f", "flag", "r", "reveal"):
            print("{}you must start the game before you can do any other actions{}".format(red, white))
        elif resp[0] in ("e", "expand", "f", "flag", "r", "reveal"):
            if not len(resp) == 3:
                print("\t{}you must give the indices of the box you wish to act on{}".format(red, white))
                continue
            try:
                int(resp[1])
                int(resp[2])
            except ValueError:
                print("\t{}the indices of the box must be numbers{}".format(red, white))
                continue
            squareRow = int(resp[1])
            squareCol = int(resp[2])
            if squareRow > rows or squareRow <= 0:
                print("\t{}that is not a valid row index{}".format(red, white))
            elif squareCol > cols or squareCol <= 0:
                print("\t{}that is not a valid column index{}".format(red, white))

            if resp[0] == "e" or resp[0] == "expand":
                if b.Expand(squareRow - 1, squareCol - 1, False):
                    break
                print("\n{}".format(b.Print()))
            elif resp[0] == "f" or resp[0] == "flag":
                if b.Flag(squareRow - 1, squareCol - 1):
                    break
                print("\n{}".format(b.Print()))
            elif resp[0] == "r" or resp[0] == "reveal":
                if b.Reveal(squareRow - 1, squareCol - 1, False):
                    break
                print("\n{}".format(b.Print()))
        else:
            print("\t{}that is not a valid command, type 'h' to see a list of valid commands{}".format(red, white))

    if b.Won():
        print("{}\n\t{}You won! It took you {} seconds. Congratulations!{}\n\n{}".format(clear, green, int(b.end), white, b.Print()))
    else: 
        print("{}\n\t{}You lost! Too bad. Better Luck next time!{}\n\n{}".format(clear, red, white, b.Print()))


    print("\n\t{}Thanks for playing!{}".format(green, white))
