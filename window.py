# get the imports -{
import sys
import signal
from PyQt6.QtCore import (
    Qt, 
    QEvent,
    pyqtSignal,
    QTime,
    QTimer
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
# }-

# The Vision: -{
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
# }-

# the square to hold the info about each box in the board -{
class Square(QLabel):

    # set the signals
    reveal = pyqtSignal(int, int)
    flag = pyqtSignal(int, int, bool)
    expand = pyqtSignal(int, int)

    # set up the widget
    def __init__(self, row, col):
        super().__init__()

        # set the vars
        self.row = row
        self.col = col
        self.val = ""
        self.start = False
        self.done = False

        self.initUI()

    # set up the widget de verdad
    def initUI(self):

        # set flags
        self.revealed = False
        self.flagged = False
        
        # set the size
        self.setFixedHeight(25)
        self.setFixedWidth(25)

        # set the style
        self.hidden = "background-color: gray; border: 3px solid; border-color: white black black white"
        self.setStyleSheet(self.hidden)

    # to flag the square
    def Flag(self):
        if not self.revealed and self.start:
            if not self.flagged:
                self.flagged = True
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setStyleSheet(f"{self.hidden}; background-color: rgb(204, 68, 153); color: black; font-weight: bold; font-size: 14px")
                self.setText("F")
                self.flag.emit(self.row, self.col, True)
            else: 
                self.flagged = False
                self.setStyleSheet(self.hidden)
                self.setText("")
                self.flag.emit(self.row, self.col, False)

# to reveal the square
    def Reveal(self, val, color):
        if not self.revealed:
            self.revealed = True
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setText(str(val))
            self.setStyleSheet(f"font-size: 17px; font-weight: bold; background-color: {'rgb(204, 204, 204)' if not val == 'B' else 'red'}; color: {color}; border: 1px solid black")

    # check when we are hovering over the square
    def enterEvent(self, event):
        if self.done:
            return
        self.setFocus()

    # check if we hit space
    def keyPressEvent(self, event):
        if self.done: 
            return
        if event.key() == Qt.Key.Key_Space:
            self.Flag() if not self.revealed else self.expand.emit(self.row, self.col)

    # check if we used the mouse
    def mousePressEvent(self, event):
        if self.done:
            return
        if event.button() == Qt.MouseButton.LeftButton and not self.flagged:
            self.reveal.emit(self.row, self.col) if not self.revealed else self.expand.emit(self.row, self.col)
        elif event.button() == Qt.MouseButton.RightButton:
            self.Flag()

# }-

# the board to hold all of the squares and update them as needed -{
class Squares(QWidget):

    # set up signals
    won = pyqtSignal()
    lost = pyqtSignal()
    flagSet = pyqtSignal(bool)
    start = pyqtSignal()

    # start the sweeper
    def __init__(self, rows, cols, mines):
        super().__init__()

        # set the vars
        self.done = False
        self.started = False
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.colors = ["rgb(204, 204, 204)", "blue", "green", "red", "purple", "orange", "teal", "yellow", "black"]
        self.squares = list(range(rows))
        for i in range(rows):
            self.squares[i] = list(range(cols))

        self.initUI()

    def initUI(self):

        # start the board
        self.board = None
        
        # set up the layout
        layout = QGridLayout()
        layout.setSpacing(0)

        # add the squares and connect their signals
        for row in range(self.rows):
            for col in range(self.cols):
                
                # get the square
                square = Square(row, col)
                
                # connect the signals
                square.reveal.connect(self.Reveal)
                square.flag.connect(self.Flag)
                square.expand.connect(self.Expand)
                
                # add the square to the layout and the array
                layout.addWidget(square, row, col)
                self.squares[row][col] = square

        self.setLayout(layout)
    # to flag a square
    def Flag(self, row, col, down):

        # send the signal
        self.flagSet.emit(down)

        # update the board
        self.board.Flag(row, col)

        # see if we have won
        if self.board.Won():
            self.won.emit()
            self.done = True

    # to reveal a square
    def Reveal(self, row, col):

        if not self.started:
            self.board = Board(self.rows, self.cols, self.mines, True, row, col)
            self.board.Start()
            self.started = True
            for rowA in range(self.rows):
                for colA in range(self.cols):
                    self.squares[rowA][colA].start = True
            self.start.emit()

        # update the board
        if self.board.Reveal(row, col, False):
            self.done = True
            self.updateSquares()
            self.lost.emit()
            return
            
        self.updateSquares()

        # see if we have won
        if self.board.Won():
            self.won.emit()
            self.done = True

    # to expand a square
    def Expand(self, row, col):

        # update the board
        if self.board.Expand(row, col, False):
            self.done = True
            self.updateSquares()
            self.lost.emit()
            return

        # update the squars
        self.updateSquares()

        # see if we have won
        if self.board.Won():
            self.won.emit()
            self.done = True


    # helper function to update the board after an expand or reveal
    def updateSquares(self):

        # loop the array and update all boxes that are no longer revealed
        for row in range(self.rows):
            for col in range(self.cols):
                if self.done:
                    self.squares[row][col].done = True
                if self.board.board[row][col].revealed:
                    val = self.board.board[row][col].val if not self.board.board[row][col].bomb else 'B'
                    self.squares[row][col].Reveal(val, self.colors[int(val)] if not val == 'B' else "black")

# }-
        
# the header to hold all of the info that isn't in the board -{
class Header(QWidget):

    # set the signals
    resetButton = pyqtSignal()

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
        self.resetGuy = Reset()

        # start the timer
        self.timer = Timer()

        # set the connections
        self.resetGuy.clicked.connect(self.Reset)

        # set the layout
        layout = QHBoxLayout()
        layout.addWidget(self.mineCount)
        layout.setAlignment(self.mineCount, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.difficulty)
        layout.setAlignment(self.difficulty, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.resetGuy)
        layout.setAlignment(self.resetGuy, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.timer)
        layout.setAlignment(self.timer, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    # send the reset signal up
    def Reset(self):
        self.resetButton.emit()

    # deal with things from the main window
    def DownMine(self, down):
        self.mineCount.CountDown(down)
    def Start(self):
        self.timer.StartTimer()
    def End(self):
        return self.timer.EndTimer()

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

        # set the time
        self.time = 0
        self.setText("000")

        # set a flag to see if we have started
        self.started = False

        # center the text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # display the time
        self.setStyleSheet("border-radius: 10px; font-size: 60px; font-weight: bold; color: red; background-color: rgb(211, 211, 211); border: 2px solid black")

    def StartTimer(self):
        # start the clock
        self.start = QTime.currentTime()
        
        # start the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1000)

    def EndTimer(self):
        self.timer.stop()
        return self.time

    def UpdateTime(self):
        self.time = self.start.secsTo(QTime.currentTime())
        if self.time > 999:
            self.time = 999
        more = ""
        if self.time < 10:
            more = "00"
        elif self.time < 100:
            more = "0"
        self.setText(f"{more}{self.time}")
# }-

# the item to hold the info about the difficulty (the list and the options for cutsom boards) -{
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
        self.setStyleSheet("border-radius: 5px; border: 1px solid black")

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
        self.addItem("--Select Level--")
        self.addItem("Beginner (9, 9, 10)")
        self.addItem("Intermediate (16, 16, 40)")
        self.addItem("Expert (16, 30, 99)")
        self.addItem("Custom (rows, cols, mines)")
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
        self.active = "font-size: 18px; border-radius: 10px; background-color: blue; font-weight: bold; color: white; border: 2px solid; border-color: grey black black grey"
        self.setStyleSheet(self.active)

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

    # to handle lowering the mine count
    def CountDown(self, down):
        if down:
            self.mines -= 1
        else:
            self.mines += 1
        self.setText(str(self.mines))
# }-

# the class to hold your score report -{
class Score(QLabel):

    def __init__(self, text, color):
        super().__init__()
        self.initUI(text, color)

    def initUI(self, text, color):
        self.setText(text)
        self.setFixedHeight(20)
        self.setStyleSheet(f"font-size: 16px; color: {color}")
# }-

# the widget to hold all other widgets -{
class Window(QWidget):

    def __init__(self, rows = 16, cols = 30, mines = 99):
        super().__init__()

        # get set the size of the board from the command line
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.layout = QVBoxLayout()

        # set the style
        self.setStyleSheet("font-family: Impact")

        # set everything else up
        self.Set()

        # set the layout in place
        self.setLayout(self.layout)

    # set up the game
    def Set(self):
        self.Initialize()
        self.Connections()
        self.Layout()

    # make the components
    def Initialize(self):
        self.Header = Header(self.mines)
        self.Squares = Squares(self.rows, self.cols, self.mines)
        self.Score = None

    # set the connections
    def Connections(self):
        self.Squares.won.connect(self.Won)
        self.Squares.lost.connect(self.Lost)
        self.Squares.flagSet.connect(self.Flag)
        self.Squares.start.connect(self.Start)
        self.Header.resetButton.connect(self.ResetGame)

    # define the layout
    def Layout(self):
        self.layout.addWidget(self.Header)
        self.layout.setAlignment(self.Header, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.Squares)
        self.layout.setAlignment(self.Squares, Qt.AlignmentFlag.AlignCenter)

    # to handle the squares emissions
    def Won(self):
        secs = self.Header.End()
        self.Score = Score(f"You Won! It took you {secs} seconds. Congratulations! Feel free to play again!", "green")
        self.layout.insertWidget(1, self.Score)
        self.layout.setAlignment(self.Score, Qt.AlignmentFlag.AlignCenter)
    def Lost(self):
        self.Score = Score("You Lost! That's too bad! Feel free to play again!", "red")
        self.layout.insertWidget(1, self.Score)
        self.layout.setAlignment(self.Score, Qt.AlignmentFlag.AlignCenter)
        self.Header.End()
    def Flag(self, down):
        self.Header.DownMine(down)
    def Start(self):
        self.Header.Start()

    # to handle the header emissions
    def ResetGame(self):
        
        # remove the widgets
        if not self.Score == None:
            self.layout.removeWidget(self.Score)
        self.layout.removeWidget(self.Header)
        self.layout.removeWidget(self.Squares)

        # set the game up again
        self.Set()
    
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
