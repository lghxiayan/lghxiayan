from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个 QStackedWidget
        self.stackedWidget = QStackedWidget()

        # 创建一个布局
        layout1 = QVBoxLayout()
        # 在这里添加你的控件到 layout1

        # 创建一个 QWidget 并设置其布局
        widget1 = QWidget()
        widget1.setLayout(layout1)

        # 将 QWidget 添加到 QStackedWidget
        self.stackedWidget.addWidget(widget1)

        # 设置 QStackedWidget 为主窗口的中心部件
        self.setCentralWidget(self.stackedWidget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
