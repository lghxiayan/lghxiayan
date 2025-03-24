# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
import os
import sys

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *

"""
日志配置文件为logging_app.conf，日志存放目录为根目录下的logs
"""
# 引入我需要的库
from controllers.widgets.widgets_controller import WidgetsController
from controllers.wowjump.wowjump_controller import WoWJumpController
from controllers.ptvicomo.ptvicomo_controller import PtvicomoController

import time
import logging.config

# 确保 Python 解释器和终端使用的默认编码为 UTF-8，因为windows默认使用是GBK
os.environ['PYTHONIOENCODING'] = 'utf-8'


class LoggingApp:
    @staticmethod
    def setup_logging():
        try:
            # 获取当前模块的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # print(current_dir)
            # 定义日志文件名
            log_file_name = f"app_log_{time.strftime('%Y%m%d')}.log"
            # 构造保存日志文件目录的路径
            logs_dir = os.path.join(current_dir, 'logs')
            # 确保 logs 目录存在
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
            # 构造日志文件的绝对路径
            log_file_path = os.path.join(logs_dir, log_file_name).replace('\\', '\\\\')
            # print(log_file_path)
            # 使用绝对路径来加载日志配置文件
            config_file_path = os.path.join(current_dir, 'logging_app.conf').replace('\\', '\\\\')
            # print(f"加载日志配置文件路径: {config_file_path}")
            logging.config.fileConfig(
                config_file_path,
                encoding='utf-8',
                defaults={'logfilename': log_file_path},
                disable_existing_loggers=False
            )
            my_logger = logging.getLogger('app_log')
            my_logger.setLevel(logging.INFO)
            # print(f"app_log handlers: {my_logger.handlers}")
            # print(f"app_log propagate: {my_logger.propagate}")
            return my_logger
        except Exception as e:
            print(f"加载日志配置文件时出错: {e}")
            exit(1)


os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self, logger):
        QMainWindow.__init__(self)
        self.logger = logger

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # 我添加的页面控制代码
        self.widgets_controller = WidgetsController(self.ui)
        self.wowjump_controller = WoWJumpController(self.ui, self.logger)
        self.ptvicomo_controller = PtvicomoController(self.ui, self.logger)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # 我添加的按钮
        widgets.btn_wowjump.clicked.connect(self.buttonClick)
        widgets.btn_ptvicomo.clicked.connect(self.buttonClick)

        # widgets.pushButton.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        # SHOW WOWJUMP PAGE
        if btnName == "btn_wowjump":
            widgets.stackedWidget.setCurrentWidget(widgets.wowjump_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET OTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        # SHOW PTVICOMO PAGE
        if btnName == "btn_ptvicomo":
            widgets.stackedWidget.setCurrentWidget(widgets.ptvicomo_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET OTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

        # if btnName == "pushButton":
        #     print("Widgets 里面的 pushButton 被点击了!")

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


if __name__ == "__main__":
    new_logger = LoggingApp().setup_logging()
    new_logger.info("main.py加载正常")

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow(new_logger)
    sys.exit(app.exec())
