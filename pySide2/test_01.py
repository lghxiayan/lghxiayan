import sys
import random
from PySide2 import QtGui, QtWidgets, QtCore


class MainWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle('Hello World')
        self.hello = ['hallo Welt', '你好世界']
        self.button = QtWidgets.QPushButton('Click me')
        self.text = QtWidgets.QLabel('hello world')
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())
