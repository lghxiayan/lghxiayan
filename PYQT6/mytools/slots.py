import os
import sys

import slots_calculator

# 添加 ptvicomo 目录到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/ptvicomo')
from ptvicomo.slot_ptvicomo import open_settings_dialog, run_now, run_now_process_bar, bind_ptvicomo_slots

# from ptvicomo.slot_ptvicomo_01 import SlotPtvicomo  # 导入子模块的类

"""
这个类似于urls.py文件一样。
"""


def bind_slots(ui):
    # my_ptvicomo = SlotPtvicomo()
    # ui.pushButton_run_now.clicked.connect(lambda: my_ptvicomo.run_now)
    # ui.pushButton_run_now.clicked.connect(lambda: my_ptvicomo.run_now_process_bar)

    bind_ptvicomo_slots(ui)
    # 象岛设置按钮
    ui.pushButton_read_settings.clicked.connect(lambda: open_settings_dialog())
    # 象岛“立即执行”按钮
    ui.pushButton_run_now.clicked.connect(lambda: run_now)
    # ui.pushButton_run_now.clicked.connect(lambda: run_now_process_bar)
    # 象岛运行状态栏
    ui.pushButton_run_now.clicked.connect(lambda: run_now_process_bar(ui.statusbar))

    # 加法计算按钮
    ui.pushButton_6.clicked.connect(
        lambda: slots_calculator.cal(int(ui.lineEdit_4.text()), int(ui.lineEdit_5.text()),
                                     ui.lineEdit_6) if slots_calculator.validate_input(
            ui.lineEdit_4, ui.lineEdit_5) else None)
    ui.pushButton_6.clicked.connect(lambda: slots_calculator.style(ui.lineEdit_6))

    # 每天一小步
    ui.pushButton_6.clicked.connect(lambda: slots_calculator.print_result(ui.plainTextEdit))
