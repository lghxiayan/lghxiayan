import sys
import ansiconv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

ansi = "\033[42m\033[31mHello World! --sidiot.\033[0m\033[0m"
ansi_2 = """
[32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:94 | 按下了按键：Key.ctrl_l[0m
[32m2025-03-06 17:38:19 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:126 | 未找到窗口：魔兽世界，尝试第 1 次重试...[0m
[32m2025-03-06 17:38:20 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:126 | 未找到窗口：魔兽世界，尝试第 2 次重试...[0m
[32m2025-03-06 17:38:21 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:126 | 未找到窗口：魔兽世界，尝试第 3 次重试...[0m
[31m2025-03-06 17:38:22 | root         | ERROR    | wow_jump_02_单人_kook加速器_v3.py:134 | 经过 3 次尝试后仍未找到窗口：魔兽世界[0m
[32m2025-03-06 17:38:36 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:94 | 按下了按键：Key.ctrl_l[0m
[32m2025-03-06 17:38:37 | root         | INFO     | wow_jump_02_单人_kook加速器_v3.py:94 | 按下了按键：Key.ctrl_l[0m
"""

# 将 ANSI 转换为 HTML
plain = ansiconv.to_plain(ansi_2)
html = ansiconv.to_html(ansi_2)

# 添加 CSS 样式规则
css_styles = """
<style>
    .ansi30 { color: black; }
    .ansi31 { color: red; }
    .ansi32 { color: green; }
    .ansi33 { color: yellow; }
    .ansi34 { color: blue; }
    .ansi35 { color: magenta; }
    .ansi36 { color: cyan; }
    .ansi37 { color: white; }
    .ansi40 { background-color: black; }
    .ansi41 { background-color: red; }
    .ansi42 { background-color: green; }
    .ansi43 { background-color: yellow; }
    .ansi44 { background-color: blue; }
    .ansi45 { background-color: magenta; }
    .ansi46 { background-color: cyan; }
    .ansi47 { background-color: white; }
</style>
"""

# 替换换行符为 <br>
html_with_br = html.replace('\n', '<br>')

# 合并 HTML 和 CSS 样式
full_html = f"<html><head>{css_styles}</head><body>{html_with_br}</body></html>"
print(f"Convert Plain: {plain}")
print(f"Convert HTML: {full_html}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANSI to QTextEdit")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml(full_html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
