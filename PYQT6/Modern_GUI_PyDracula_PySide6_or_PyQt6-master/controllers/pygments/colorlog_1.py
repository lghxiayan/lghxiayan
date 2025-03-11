import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

# 正则表达式，用于解析 ANSI 颜色代码
ansi_color_pattern = re.compile(r'\x1b\[([0-9;]+)m')

# 颜色名称到 QColor 对象的映射
color_map = {
    'black': QColor(0, 0, 0),
    'red': QColor(255, 0, 0),
    'green': QColor(0, 255, 0),
    'yellow': QColor(255, 255, 0),
    'blue': QColor(0, 0, 255),
    'magenta': QColor(255, 0, 255),
    'cyan': QColor(0, 255, 255),
    'white': QColor(255, 255, 255),
}


# ANSITextEdit 类，可以处理 ANSI 颜色代码
class ANSITextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 保存正常格式的引用
        self.normal_format = self.currentCharFormat()

    def appendPlainText(self, text):
        # 根据 ANSI 颜色代码分割文本
        parts = ansi_color_pattern.split(text)
        cursor = self.textCursor()

        # 遍历部分文本并应用相应的颜色
        for i, part in enumerate(parts):
            if i % 2 == 1:  # 颜色代码
                # 解析颜色代码
                code = part
                color = self.normal_format.foreground().color()
                if code == "0":  # 重置为默认颜色
                    color = self.normal_format.foreground().color()
                elif code == "1":  # 加粗
                    continue  # 暂时忽略加粗
                elif code in ["30", "40"]:  # 黑色
                    color = color_map['black']
                elif code in ["31", "41"]:  # 红色
                    color = color_map['red']
                elif code in ["32", "42"]:  # 绿色
                    color = color_map['green']
                elif code in ["33", "43"]:  # 黄色
                    color = color_map['yellow']
                elif code in ["34", "44"]:  # 蓝色
                    color = color_map['blue']
                elif code in ["35", "45"]:  # 品红色
                    color = color_map['magenta']
                elif code in ["36", "46"]:  # 青色
                    color = color_map['cyan']
                elif code in ["37", "47"]:  # 白色
                    color = color_map['white']

                # 设置颜色格式
                format = QTextCharFormat()
                format.setForeground(color)
                cursor.setCharFormat(format)
            else:  # 文本
                if part:
                    cursor.insertText(part)

        # 确保文本实际被追加
        self.setTextCursor(cursor)


ansi_2 = """
[32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
[32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 1 次重试...[0m
[32m2025-03-06 17:38:20 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 2 次重试...[0m
[32m2025-03-06 17:38:21 | root         | INFO     | wow_jump_kook_v3.py.py:126 | 未找到窗口：魔兽世界，尝试第 3 次重试...[0m
[31m2025-03-06 17:38:22 | root         | ERROR    | wow_jump_kook_v3.py.py:134 | 经过 3 次尝试后仍未找到窗口：魔兽世界[0m
[32m2025-03-06 17:38:36 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
[32m2025-03-06 17:38:37 | root         | INFO     | wow_jump_kook_v3.py.py:94 | 按下了按键：Key.ctrl_l[0m
"""

# 示例用法
app = QApplication([])
window = QMainWindow()
editor = ANSITextEdit(window)
window.setCentralWidget(editor)
editor.appendPlainText("\x1b[31m这是红色文本\x1b[0m，这是正常文本。")
editor.appendPlainText(ansi_2)
window.show()
app.exec()
