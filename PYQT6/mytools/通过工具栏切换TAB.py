import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QToolBar
from PyQt6.QtGui import QAction  # 从 PyQt6.QtGui 模块中导入 QAction
from PyQt6 import uic


def switch_tab(tab_widget, index):
    tab_widget.setCurrentIndex(index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 加载 UI 文件
        self.ui = uic.loadUi('./ui/slot.ui', self)

        # 获取 QTabWidget 实例
        self.tab_widget = self.ui.findChild(QTabWidget, 'tabWidget')  # 假设 tabWidget 的对象名为 'tabWidget'
        if self.tab_widget is None:
            raise ValueError("QTabWidget not found in the UI file")

        # 隐藏标签页
        self.tab_widget.tabBar().setVisible(False)

        # 创建工具栏
        toolbar = QToolBar("Tab Switcher")
        self.addToolBar(toolbar)

        # 创建工具栏按钮并连接槽函数
        button1 = QAction('Tab 1', self)
        button2 = QAction('Tab 2', self)
        button3 = QAction('Tab 3', self)

        button1.triggered.connect(lambda: switch_tab(self.tab_widget, 0))
        button2.triggered.connect(lambda: switch_tab(self.tab_widget, 1))
        button3.triggered.connect(lambda: switch_tab(self.tab_widget, 2))

        # 添加按钮到工具栏
        toolbar.addAction(button1)
        toolbar.addAction(button2)
        toolbar.addAction(button3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
