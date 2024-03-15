from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QTextBrowser, QTextEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon


class Http:
    def __init__(self):
        # 从文件中加载UI定义
        my_qfile = QFile('http_port_test.ui')
        my_qfile.open(QFile.ReadOnly)
        my_qfile.close()
        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(my_qfile)

        self.ui.display_Button.clicked.connect(self.display)
        self.ui.clear_Button.clicked.connect(self.clear)

    def display(self):
        everyDayUp = pow(1.001, 365)
        self.ui.response_Browser.setPlainText(f'每天进步千分之一,365天之后：{everyDayUp:.3f}')

    def clear(self):
        self.ui.response_Browser.clear()


app = QApplication([])
app.setWindowIcon(QIcon('drive_fs.ico'))
http_Window = Http()

http_Window.ui.show()
app.exec_()
