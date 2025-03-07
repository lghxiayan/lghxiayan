import sys
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtWidgets import QPushButton, QTextEdit
import subprocess
import os
import io
import threading
import chardet
from pygments import highlight
# from pygments.lexers import get_lexer_by_name, LexerContext
from pygments.lexer import RegexLexer
from pygments.token import Text
from pygments.formatters import HtmlFormatter
import logging
from pynput import keyboard


class WoWJumpController:
    def __init__(self, ui):
        self.ui = ui
        self.setup_connections()
        self.process = None
        self.file_name = "wow_jump_02_单人_kook加速器_v3.py"

    def setup_connections(self):
        self.ui.pushButton_wowjump_run.clicked.connect(self.on_pushbutton_clicked)
        self.ui.pushButton_wowjump_stop.clicked.connect(self.on_stop_button_clicked)

    def on_pushbutton_clicked(self):
        print("wowjump 页面里面的 pushButton[run] 被点击了！")
        plain_textedit_wowjump_1 = self.ui.plainTextEdit_wowjump_1
        plain_textedit_wowjump_1.appendPlainText("Widgets里面的 pushButton[run] 被点击了！")

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, self.file_name)
        # print(file_path)
        # subprocess.run(['python', file_path])

        thread = threading.Thread(target=self.run_script, args=(file_path,))
        thread.start()

    def run_script(self, file_path):
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
                print(output.strip())
                # self.ui.plainTextEdit_wowjump_1.appendPlainText(output.strip())
        rc = self.process.poll()
        print(f'子进程退出码：{rc}')

    def on_stop_button_clicked(self):
        print("wowjump 页面里面的 pushButton[stop] 被点击了！")
        if self.process and self.process.poll() is None:
            self.process.terminate()
            print("子进程已终止")
