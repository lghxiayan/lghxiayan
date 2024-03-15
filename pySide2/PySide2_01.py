from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile('ui/first.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        info = self.ui.textEdit.toPlainText()
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            parts = [i for i in parts if i]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'
        QMessageBox.about(self.ui,
                          '统计结果',
                          f'''工资超过20K的有\n{salary_above_20k}
                          \n工资低于20K的有\n{salary_below_20k}'''
                          )


# 创建应用程序对象
app = QApplication([])
stats = Stats()

# 显示主窗口
stats.ui.show()

# 程序执行
app.exec_()
