"""
全部使用PySide6的库，不要和PyQt6的库混用。它是是有区别的。例如PySide6中，信号用的是Signal，而PyQt6则是pyqtSignal。

todo 1.按钮的效果。按下运行的时候，要有按下去的效果，以便知道当前的状态。而停止按钮，只有在程序运行的时候才变成可按的效果，平时应该是灰色的，不可点击的状态。

"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox, QHBoxLayout, QLineEdit
import configparser
import configupdater
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor
import subprocess
import os
import threading
import ansiconv

os.environ['PYTHONIOENCODING'] = 'utf-8'

# 打印当前工作目录
print(f"当前工作目录   : {os.getcwd()}")

# 调整工作目录为配置文件所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
os.chdir(script_dir)
print(f"调整后的工作目录: {os.getcwd()}")

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


class SettingsWindow(QDialog):
    def __init__(self, ui_main_window):
        # 获取真正的 QWidget 实例
        parent = ui_main_window.centralWidget() if hasattr(ui_main_window, 'centralWidget') else None
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.layout = QVBoxLayout(self)

        # 使用 QHBoxLayout 将 QLabel 和 QCheckBox 放在同一行
        self.headless_layout = QHBoxLayout()
        self.headless_label = QLabel('无头模式:')
        self.headless_checkbox = QCheckBox()
        self.headless_layout.addWidget(self.headless_label)
        self.headless_layout.addWidget(self.headless_checkbox)

        # 利润率 PROFIT_MARGIN = 10
        self.profit_margin_layout = QHBoxLayout()
        self.profit_margin_label = QLabel('利润率:')
        self.profit_margin_line_edit = QLineEdit()
        self.profit_margin_layout.addWidget(self.profit_margin_label)
        self.profit_margin_layout.addWidget(self.profit_margin_line_edit)

        # 将 QHBoxLayout 添加到主布局中
        self.layout.addLayout(self.headless_layout)
        self.layout.addLayout(self.profit_margin_layout)

        self.save_button = QPushButton('保存')
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.load_settings()

    def load_settings(self):
        config = configparser.ConfigParser(interpolation=None)
        config_file_path = 'config_ptvicomo_04.ini'

        # 检查配置文件是否存在
        if not os.path.exists(config_file_path):
            QMessageBox.critical(self, "错误", f"配置文件不存在: {config_file_path}")
            return
        try:
            config.read(config_file_path, encoding='utf-8')

            # 读取 HEAD_LESS 参数
            headless = config.getboolean('DEFAULT', 'HEAD_LESS')
            self.headless_checkbox.setChecked(headless)
            # print(f'读取配置文件成功! HEAD_LESS={headless}')
            # 读取 PROFIT_MARGIN 参数
            profit_margin = config.get('TRADE', 'PROFIT_MARGIN')
            self.profit_margin_line_edit.setText(profit_margin)
            print(f'读取配置文件成功! PROFIT_MARGIN = {profit_margin}')
        except configparser.NoSectionError:
            QMessageBox.warning(self, "警告", "配置文件中缺少 [DEFAULT] 部分。")
        except configparser.NoOptionError:
            QMessageBox.warning(self, "警告", "配置文件中缺少 HEAD_LESS 参数。")
        except configparser.Error as e:
            QMessageBox.critical(self, "错误", f"读取配置文件时发生错误: {e}")

    def save_settings(self):
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_ptvicomo_04.ini')
        try:
            # 创建 ConfigUpdater 对象
            updater = configupdater.ConfigUpdater()
            # 读取现有的配置文件
            if os.path.exists(config_file_path):
                updater.read(config_file_path, encoding='utf-8')
            else:
                QMessageBox.critical(self, "错误", f"配置文件不存在: {config_file_path}")
                return
            # 更新 HEAD_LESS 参数
            if 'DEFAULT' not in updater:
                updater.add_section('DEFAULT')
            # 获取 QCheckBox 的当前状态（布尔值）
            headless_checkbox_value = self.headless_checkbox.isChecked()
            # 将布尔值转换为字符串并更新配置文件
            updater['DEFAULT']['HEAD_LESS'] = str(headless_checkbox_value)
            print(f"更新 HEAD_LESS 参数: {headless_checkbox_value}")

            # 获取 QLineEdit 的当前状态（布尔值）
            profit_margin_line_edit_value = self.profit_margin_line_edit.text()
            updater['TRADE']['PROFIT_MARGIN'] = profit_margin_line_edit_value
            print(f"更新 PROFIT_MARGIN 参数: {profit_margin_line_edit_value}")

            # 写入更新后的配置文件
            with open(config_file_path, 'w', encoding='utf-8') as configfile:
                updater.write(configfile)
            print("成功", "设置已保存")

        except Exception as e:
            print("错误", f"保存配置文件时发生异常: {e}")

        QMessageBox.information(self, "成功", "设置已保存")
        self.accept()


class PtvicomoController:
    def __init__(self, ui, logger):
        self.ui = ui
        self.logger = logger
        self.logger.info("PtvicomoController加载成功")
        self.setup_connections()
        self.process = None
        # self.file_name = "selenium_ptvicomo_cookie_04_test.py"
        self.file_name = "selenium_ptvicomo_cookie_04_sqlalchemy.py"

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

            script_dir = os.path.dirname(os.path.abspath(file_path))
            # print('script_dir:', script_dir)
            print(f"运行脚本：{file_path}")
            self.logger.info(f"运行脚本：{file_path}")
            self.process = subprocess.Popen(
                ['python', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                cwd=script_dir,  # 设置子进程的工作目录
            )
            while True:
                output = self.process.stdout.readline()
                # print(f"94line:{output}")  # 结果前面有,后面输出空值。为什么
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

            # 捕获并打印错误输出
            errors = self.process.stderr.read()
            if errors:
                print(f"子进程错误输出：{errors}")

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
            print("子进程已终止")

    def on_setting_button_clicked(self):
        print("ptvicomo 页面里面的 pushButton[setting] 被点击了！")
        textedit_ptvicomo_1 = self.ui.textEdit_ptvicomo_1
        textedit_ptvicomo_1.insertPlainText("ptvicomo 页面里面的 pushButton[setting] 被点击了！\n")
        self.scroll_to_end(textedit_ptvicomo_1)

        settings_window = SettingsWindow(self.ui.parent() if hasattr(self.ui, 'parent') else None)
        settings_window.exec()

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
