"""
全部使用PySide6的库，不要和PyQt6的库混用。它是是有区别的。例如PySide6中，信号用的是Signal，而PyQt6则是pyqtSignal。

todo 1.按钮的效果。按下运行的时候，要有按下去的效果，以便知道当前的状态。而停止按钮，只有在程序运行的时候才变成可按的效果，平时应该是灰色的，不可点击的状态。
todo 2.关于日志。子程序因为可以独立运行，所以日志是单独的，这个不用修改。但整个程序应该只有一个程序日志，它应该包括wowjump模块、ptvicomo模块、以及其它的模块，它们应该是共用一个日志的。
todo 3.日志。wowjump模块和独立子程序v3.py文件，共用一个日志，这里会有冲突，要解决。错误提示：【PermissionError: [WinError 32] 另一个程序正在使用此文件】

"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor
import subprocess
import os
import threading
import ansiconv
import logging
import logging.config

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


class OutputSignal(QObject):
    output_writer = Signal(str)


class PtvicomoController:
    def __init__(self, ui):
        self.ui = ui
        self.setup_connections()
        self.process = None
        self.file_name = "selenium_ptvicomo_cookie_04.py"

        # 配置日志记录器
        config_file_path = os.path.join(os.path.dirname(__file__), 'logging_ptvicomo.conf')
        logging.config.fileConfig(config_file_path, encoding='utf-8')
        self.logger = logging.getLogger('ptvicomo_log')
        self.logger.setLevel(logging.INFO)

        self.output_signal = OutputSignal()
        self.output_signal.output_writer.connect(self.append_output_to_textedit)

    def setup_connections(self):
        self.ui.pushButton_ptvicomo_run.clicked.connect(self.on_run_button_clicked)
        self.ui.pushButton_ptvicomo_stop.clicked.connect(self.on_stop_button_clicked)
        self.ui.pushButton_ptvicomo_setting.clicked.connect(self.on_setting_button_clicked)

    def on_run_button_clicked(self):
        print("ptvicomo 页面里面的 pushButton[run] 被点击了！")
        textedit_ptvicomo_1 = self.ui.textEdit_ptvicomo_1
        textedit_ptvicomo_1.insertPlainText("ptvicomo 页面里面的 pushButton[run] 被点击了！\n")
        self.scroll_to_end(textedit_ptvicomo_1)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, self.file_name)

        thread = threading.Thread(target=self.run_script, args=(file_path,))
        thread.start()

    def run_script(self, file_path):
        try:
            # 添加 CSS 样式规则
            global css_styles

            self.logger.info(f"运行脚本：{file_path}")
            self.process = subprocess.Popen(
                ['python', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    # 在终端打印日志信息
                    print(output.strip())
                    # 将ANSI日志结果转换成html格式
                    html = ansiconv.to_html(output)
                    # 替换换行符为 <br>
                    html_with_br = html.replace('\n', '<br>')
                    # 合并 HTML 和 CSS 样式
                    full_html = f"<html><head>{css_styles}</head><body>{html_with_br}</body></html>"
                    # print(f"Convert HTML: {html_with_br}")
                    self.output_signal.output_writer.emit(full_html.strip())
            rc = self.process.poll()
            print(f'子进程退出码：{rc}')
        except Exception as e:
            print(f"发生异常：{e}")

    def on_stop_button_clicked(self):
        print("ptvicomo 页面里面的 pushButton[stop] 被点击了！")
        textedit_ptvicomo_1 = self.ui.textEdit_ptvicomo_1
        textedit_ptvicomo_1.insertPlainText("ptvicomo 页面里面的 pushButton[stop] 被点击了！\n")
        self.scroll_to_end(textedit_ptvicomo_1)

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.logger.info("子进程已终止")

    def on_setting_button_clicked(self):
        print("ptvicomo 页面里面的 pushButton[setting] 被点击了！")
        textedit_ptvicomo_1 = self.ui.textEdit_ptvicomo_1
        textedit_ptvicomo_1.insertPlainText("ptvicomo 页面里面的 pushButton[setting] 被点击了！\n")
        self.scroll_to_end(textedit_ptvicomo_1)

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            print("setting按钮被点击")

    @staticmethod
    def scroll_to_end(text_edit):
        cursor = text_edit.textCursor()
        # 使用枚举值而不是直接传递字符串或常量
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

    def append_output_to_textedit(self, output):
        try:
            cursor = self.ui.textEdit_ptvicomo_1.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.ui.textEdit_ptvicomo_1.setTextCursor(cursor)
            self.ui.textEdit_ptvicomo_1.insertHtml(output)
            self.ui.textEdit_ptvicomo_1.ensureCursorVisible()  # 确保光标可见，即滚动到底部
        except Exception as e:
            print(f"发生异常：{e}")
            self.logger.error(f"发生异常：{e}")
