import re
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QColor, QTextCharFormat, QFont


class ANSIMessageHandler:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.document = text_edit.document()
        self.cursor = QTextCursor(self.document)
        self.normal_format = QTextCharFormat()
        self.current_format = QTextCharFormat()

    def write(self, message):
        # ANSI 转义序列的正则表达式
        ansi_escape = re.compile(r'\x1B\[([0-9;]+)m')
        parts = ansi_escape.split(message)
        for i, part in enumerate(parts):
            if i % 2 == 1:  # 颜色代码
                self._parse_ansi_code(part)
            else:  # 文本
                if part:
                    self.cursor.insertText(part, self.current_format)

    def _parse_ansi_code(self, code):
        # 解析 ANSI 颜色代码
        codes = code.split(';')
        for c in codes:
            if c == "0":
                self.current_format = QTextCharFormat()
            elif c == "1":
                self.current_format.setFontWeight(QFont.Weight.Bold)
            elif c == "22":
                self.current_format.setFontWeight(QFont.Weight.Normal)
            elif c.startswith('3') and len(c) == 2:  # 前景色
                color_codes = {
                    '30': QColor("black"),
                    '31': QColor("red"),
                    '32': QColor("green"),
                    '33': QColor("yellow"),
                    '34': QColor("blue"),
                    '35': QColor("magenta"),
                    '36': QColor("cyan"),
                    '37': QColor("white")
                }
                self.current_format.setForeground(color_codes.get(c, QColor("black")))
            elif c.startswith('4') and len(c) == 2:  # 背景色
                color_codes = {
                    '40': QColor("black"),
                    '41': QColor("red"),
                    '42': QColor("green"),
                    '43': QColor("yellow"),
                    '44': QColor("blue"),
                    '45': QColor("magenta"),
                    '46': QColor("cyan"),
                    '47': QColor("white")
                }
                self.current_format.setBackground(color_codes.get(c, QColor("black")))

    def flush(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANSI to QTextEdit")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.ansi_handler = ANSIMessageHandler(self.text_edit)

        # 重定向 stdout 和 stderr 到 QTextEdit
        sys.stdout = self.ansi_handler
        sys.stderr = self.ansi_handler

        # 示例输出
        print("\033[31m这是红色文本\033[0m，这是正常文本。")
        print(ansi_2)


if __name__ == "__main__":
    ansi_2 = """
    [32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
    [32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 1 次重试...[0m
    [32m2025-03-06 17:38:20 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 2 次重试...[0m
    [32m2025-03-06 17:38:21 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 3 次重试...[0m
    [31m2025-03-06 17:38:22 | root         | ERROR    | wow_jump_kook_v3.py.py:134 | 经过 3 次尝试后仍未找到窗口：魔兽世界[0m
    [32m2025-03-06 17:38:36 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
    [32m2025-03-06 17:38:37 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
    """

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
