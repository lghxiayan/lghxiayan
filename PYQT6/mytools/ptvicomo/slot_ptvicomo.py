import time

from PyQt6 import uic
from PyQt6.QtWidgets import QProgressBar, QLineEdit, QCheckBox, QStatusBar, QButtonGroup, QDialog
from PyQt6.QtCore import pyqtSlot, QTimer

import config_ptvicomo_04 as config


def update_config(lineEdit_sale_number: QLineEdit, lineEdit_buy_number: QLineEdit, lineEdit_profit_margin: QLineEdit,
                  lineEdit_save_page: QCheckBox):
    print("Updating configuration...")  # 调试输出
    new_config = {
        'SALE_NUMBER': int(lineEdit_sale_number.text()),
        'BUY_NUMBER': int(lineEdit_buy_number.text()),
        'PROFIT_MARGIN': int(lineEdit_profit_margin.text()),
        'SAVE_PAGE': lineEdit_save_page.isChecked()
    }

    config_file_path = 'config_ptvicomo_04.py'
    with open(config_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(config_file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            for key, value in new_config.items():
                if f"{key} =" in line:
                    if isinstance(value, str):
                        file.write(f'{key} = "{value}"\n')
                    else:
                        file.write(f"{key} = {value}\n")
                    break
            else:
                file.write(line)

    print("Configuration updated successfully!")  # 调试输出


def run_now():
    for i in range(5):
        print(f"Running now! {i}")
        time.sleep(1)
    # selenium_ptvicomo_cookie_05.main()


def run_now_process_bar(status_bar: QStatusBar):
    progress_bar = QProgressBar()
    status_bar.addWidget(progress_bar)
    progress_bar.setMaximum(100)

    def update_progress():
        nonlocal current_value
        if current_value < 100:
            current_value += 1
            progress_bar.setValue(current_value)
            timer.start(100)
        else:
            timer.stop()
            status_bar.removeWidget(progress_bar)

    current_value = 0
    timer = QTimer()
    timer.timeout.connect(update_progress)
    timer.start(100)


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        ui_setting_ptvicomo = uic.loadUi("./ui/pop_dialog.ui", self)
        self.setWindowTitle("象岛设置")

        ui_setting_ptvicomo.lineEdit_chrome_driver_path.setText(config.CHROME_DRIVER_PATH)
        ui_setting_ptvicomo.lineEdit_db_host.setText(config.DB_CONFIG['host'])
        ui_setting_ptvicomo.lineEdit_db_port.setText(str(config.DB_CONFIG['port']))
        ui_setting_ptvicomo.lineEdit_db_user.setText(config.DB_CONFIG['user'])
        ui_setting_ptvicomo.lineEdit_db_password.setText(config.DB_CONFIG['password'])
        ui_setting_ptvicomo.lineEdit_db_database.setText(config.DB_CONFIG['database'])
        ui_setting_ptvicomo.lineEdit_table_name.setText(config.TABLE_NAME)
        ui_setting_ptvicomo.lineEdit_website_url.setText(config.WEBSITE_URL)
        ui_setting_ptvicomo.lineEdit_login_username.setText(config.LOGIN_USERNAME)
        ui_setting_ptvicomo.lineEdit_login_password.setText(config.LOGIN_PASSWORD)

        ui_setting_ptvicomo.spinBox_wait_timeout.setValue(config.WAIT_TIMEOUT)
        ui_setting_ptvicomo.spinBox_sale_number.setRange(0, 9999)
        ui_setting_ptvicomo.spinBox_sale_number.setValue(config.SALE_NUMBER)
        ui_setting_ptvicomo.spinBox_buy_number.setRange(1, 9999)
        ui_setting_ptvicomo.spinBox_buy_number.setValue(config.BUY_NUMBER)
        ui_setting_ptvicomo.doubleSpinBox_profit_margin.setValue(config.PROFIT_MARGIN)

        ui_setting_ptvicomo.checkBox_save_page.setChecked(config.SAVE_PAGE)

        time_button_group = QButtonGroup()
        radio1 = ui_setting_ptvicomo.radioButton_day
        radio2 = ui_setting_ptvicomo.radioButton_hour
        radio3 = ui_setting_ptvicomo.radioButton_minutes
        print(radio1.text(), radio2.text(), radio3.text())
        time_button_group.addButton(radio1)
        time_button_group.addButton(radio2)
        time_button_group.addButton(radio3)

        # ui_setting_ptvicomo.save_button.clicked.connect(self.save_settings)
        self.save_button.clicked.connect(self.save_settings)

    @pyqtSlot()
    def save_settings(self):
        print("保存设置")
        self.close()
        # update_config()


def open_settings_dialog():
    settings_dialog = SettingsDialog()
    settings_dialog.show()
    settings_dialog.exec()


def bind_ptvicomo_slots(ui):
    pass
    # 象岛保存按钮
    # ui.button_update_config.clicked.connect(
    #     lambda: update_config(ui.lineEdit_sale_number, ui.lineEdit_buy_number, ui.lineEdit_profit_margin,
    #                           ui.checkBox_save_page))
