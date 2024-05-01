# get the imports
import sys
import signal
from PyQt6.QtCore import (
    Qt, 
    QEvent,
    pyqtSignal
)
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QLabel
)
from board import Board

# The Vision:
#   _____________________________________
#   |  _______    _____   ___   ______  |
#   | |_Mines_|  |_Lvl_| |_R_| |_Time_| |
#   | ________________________________  |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   | |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_| |
#   |___________________________________|

# the square to hold the info about each box in the board -{
class Square(QLabel):

    # set the signals
    reveal = pyqtSignal(int, int) # if we left click
    flag = pyqtSignal(int, int) # if we right click
    # if we hover and press the space bar, I want to be able to handle that too

    # set up the widget
    def __init__(self, row, col, val):
        super().__init__()

        # set the vars
        self.row = row
        self.col = col
        self.val = val

        self.initUI()

    # set up the widget de verdad
    def initUI(self):

        # set the size
        self.setFixedHeight(25)
        self.setFixedWidth(25)

        # set the style
        self.setStyleSheet("background-color: gray; border: 3px solid; border-color: white black black white")

# }-

# the board to hold all of the squares and update them as needed -{
class Squares(QWidget):

    # start the sweeper
    def __init__(self, rows, cols, mines):
        super().__init__()
        
        # set the vars
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.colors = ["blue", "green", "red", "purple", "orange", "teal", "yellow", "black"]
        self.squares = list(range(rows))
        for i in range(rows):
            self.squares[i] = list(range(cols))

        self.initUI()

    def initUI(self):

        # set the size
        self.setFixedHeight(self.rows * 31)
        self.setFixedWidth(self.cols * 31)

        # get the board
        self.board = Board(self.rows, self.cols, self.mines)
        
        # set up the layout
        layout = QGridLayout()
        layout.setSpacing(0)

        # add the squares
        for row in range(self.rows):
            for col in range(self.cols):
                square = Square(row, col, self.board.board[row][col].val)
                layout.addWidget(square, row, col)
                self.squares[row][col] = square
        self.setLayout(layout)


# }-
        
# the header to hold all of the info that isn't in the board -{
class Header(QWidget):

    def __init__(self, mines):
        super().__init__()
        self.mines = mines
        self.initUI()

    def initUI(self):

        # set the size
        self.setFixedHeight(100)
        self.setFixedWidth(600)

        # start the mine counter
        self.mineCount = MineCount(self.mines)

        # start the difficulty level holder
        self.difficulty = Difficulty()

        # start the reset button
        self.reset = Reset()

        # start the timer
        self.timer = Timer()

        # set the style
        self.setStyleSheet("font-family: Impact")

        # set the layout
        layout = QHBoxLayout()
        layout.addWidget(self.mineCount)
        layout.setAlignment(self.mineCount, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.difficulty)
        layout.setAlignment(self.difficulty, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.reset)
        layout.setAlignment(self.reset, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.timer)
        layout.setAlignment(self.timer, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)
# }-

# the timer to keep track of time since the game started -{
class Timer(QLabel):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set the height
        self.setFixedHeight(60)
        self.setFixedWidth(140)
        
        # flag to know if we have started
        self.started = False

        # var to keep the time
        self.time = 0

        # center the text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # display the time
        self.setStyleSheet("border-radius: 10px; font-size: 60px; font-weight: bold; color: red; background-color: rgb(211, 211, 211); border: 2px solid black")
        self.setText("000")
# }-

# the item to hold the infro about the difficulty (the list and the options for cutsom boards) -{
class Difficulty(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set the size
        self.setFixedWidth(180)

        # set the list of options
        self.list = DifficultyList()
        
        # set the style
        self.setStyleSheet("border-radius: 5px")

        # set the holder in place
        self.holder = DifficultyHolder()
        
        # set the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)

    def ChooseCustom(self):
        # catch the emit from the difficulty list and change this to show the widget, I don't know if you need to redo the setup of the layout or no, I guess you'll find out
        pass
# }-

# the list of the difficulties to play with that are preset or custom -{
class DifficultyList(QComboBox):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.addItem("Beginner (9, 9, 10)")
        self.addItem("Intermediate (16, 16, 40)")
        self.addItem("Expert (16, 30, 99)")
        self.addItem("Custom Board")
        self.setCurrentText("--Level-- (rows, cols, mines)")
# }-

# the holder of the options for custom difficulty -{
class DifficultyHolder(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set the rows
        self.rows = Rows()

        # set the cols
        self.cols = Cols()

        # set the mines
        self.mines = Mines()

        # set the layout
        layout = QHBoxLayout()
        layout.addWidget(self.rows)
        layout.addWidget(self.cols)
        layout.addWidget(self.mines)
        self.setLayout(layout)
# }-

# the items to hold the custom options for difficulty -{
class Rows(QLineEdit):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setPlaceholderText("  rows")
        self.setFixedWidth(45)

class Cols(QLineEdit):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setPlaceholderText("  cols")
        self.setFixedWidth(40)

class Mines(QLineEdit):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setPlaceholderText("  mines")
        self.setFixedWidth(50)
# }-

# the button to reset the board and give a new one -{
class Reset(QPushButton):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set the size
        self.setFixedWidth(80)
        self.setFixedHeight(40)

        # set the text
        self.setText("Restart")

        # set the color
        self.setStyleSheet("border-radius: 10px; background-color: blue; font-weight: bold; color: white")
        # change this to New Game if we have chosen a new difficulty, and change th ebutton to blue
# }-

# the item to hold the count of how many mines you have left to place -{
class MineCount(QLabel):

    def __init__(self, mines):
        super().__init__()
        self.mines = mines
        self.initUI()

    def initUI(self):

        # set the size
        self.setFixedHeight(60)
        self.setFixedWidth(100)

        # center the text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # display the count
        self.setStyleSheet("border-radius: 10px; font-size: 60px; font-weight: bold; color: red; background-color: rgb(211, 211, 211); border: 2px solid black")
        self.setText(str(self.mines))
# }-

# the widget to hold all other widgets -{
class Window(QWidget):

    def __init__(self, rows = 16, cols = 30, mines = 99):
        super().__init__()

        # get set the size of the board from the command line
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # set everything else up
        self.initUI()

    def initUI(self):

        # start the header
        self.Header = Header(self.mines)

        # start the board
        self.Squares = Squares(self.rows, self.cols, self.mines)
        
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.Header, 0)
        layout.setAlignment(self.Header, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.Squares, 1)
        layout.setAlignment(self.Squares, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
# }-

# run the program -{
if __name__ == '__main__':

    # allow quitting from the command line
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # start the app
    app = QApplication(sys.argv)
    
    # initialize the rows and cols
    rows = 16
    cols = 30
    mines = 99

    # grab the difficulty
    size = len(sys.argv)
    if not (size == 1 or size == 2 or size == 4):
        print("\u001b[38;5;160musage:\n  python window.py\n  python window.py <b|i|e>\n\tor\n  python window.py <rows> <cols> <mines>\u001b[38;5;15m")
        sys.exit(1)
    elif size == 2:
        difficulty = sys.argv[1]
        if difficulty == 'b':
            rows = 9
            cols = 9
            mines = 10
        elif difficulty == 'i':
            rows = 16
            cols = 16
            mines = 40
        elif difficulty == 'e':
            rows = 16
            cols = 30
            mines == 99
        else:
            print("\u001b[38;5;160mthat is not a valid difficulty\n\tthe options are (b)eginner, (i)ntermediate, or (e)xpert\u001b[38;5;15m")
            sys.exit(1)
    elif size == 4:
        try:
            rows = int(sys.argv[1])
            cols = int(sys.argv[2])
            mines = int(sys.argv[3])
        except ValueError:
            print("\u001b[38;5;160myou have to provide ints for the arguments\u001b[38;5;15m")
            sys.exit(1)
        if mines >= rows * cols - 1:
            print("\u001b[38;5;160mthe number of mines is too great for the board\u001b[38;5;15m")
            sys.exit(1)

    window = Window(rows, cols, mines)
    window.show()
    sys.exit(app.exec())
# }-
