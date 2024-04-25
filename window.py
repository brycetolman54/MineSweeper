
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Hello, PyQt!", self)
        self.label.setGeometry(150, 80, 200, 30)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
