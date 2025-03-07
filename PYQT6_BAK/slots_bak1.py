import sys
import time
import asyncio

from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMessageBox, QProgressBar, QLineEdit, QPlainTextEdit, QCheckBox, QStatusBar, QRadioButton, \
    QButtonGroup, QDialog, QPushButton
import day_up
import ptvicomo


def cal(a: int, b: int, line_edit_3: QLineEdit):
    line_edit_3.setText(str(a + b))


def print_result(plainTextEdit: QPlainTextEdit):
    plainTextEdit.setPlainText(day_up.main())


def validate_input(lineEdit_4: QLineEdit, lineEdit_5: QLineEdit):
    input_text_4 = lineEdit_4.text().strip()
    input_text_5 = lineEdit_5.text().strip()

    if not input_text_4 or not input_text_5:
        QMessageBox.warning(None, "警告", "请输入有效的整数！")
        return False

    try:
        int(input_text_4)
        int(input_text_5)
    except ValueError:
        QMessageBox.warning(None, "警告", "请输入有效的数字！")
        return False

    return True


def style(line_edit_6: QLineEdit):
    line_edit_6.setStyleSheet("background-color:red")


def update_config(lineEdit_sale_number: QLineEdit, lineEdit_buy_number: QLineEdit, lineEdit_profit_margin: QLineEdit,
                  lineEdit_save_page: QCheckBox):
    print("Updating configuration...")  # 调试输出
    new_config = {
        'SALE_NUMBER': int(lineEdit_sale_number.text()),
        'BUY_NUMBER': int(lineEdit_buy_number.text()),
        'PROFIT_MARGIN': int(lineEdit_profit_margin.text()),
        'SAVE_PAGE': lineEdit_save_page.isChecked()
    }

    config_file_path = './ptvicomo/config_ptvicomo_04.py'
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
    # ptvicomo.selenium_ptvicomo_cookie_04.main()
    print("Running now!")


async def update_progress_bar(progress_bar: QProgressBar):
    try:
        for i in range(10000):
            progress_bar.setValue(i + 1)
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Exception:{e}")


def run_now_process_bar(status_bar: QStatusBar):
    progress_bar = QProgressBar()
    status_bar.addWidget(progress_bar)
    progress_bar.setMaximum(10000)
    asyncio.run(update_progress_bar(progress_bar))
    status_bar.removeWidget(progress_bar)


# slots.py
def initialize_ui(ui, config):
    ui.lineEdit_chrome_driver_path.setText(config.CHROME_DRIVER_PATH)
    ui.lineEdit_db_host.setText(config.DB_CONFIG['host'])
    ui.lineEdit_db_port.setText(str(config.DB_CONFIG['port']))
    ui.lineEdit_db_user.setText(config.DB_CONFIG['user'])
    ui.lineEdit_db_password.setText(config.DB_CONFIG['password'])
    ui.lineEdit_db_database.setText(config.DB_CONFIG['database'])
    ui.lineEdit_table_name.setText(config.TABLE_NAME)
    ui.lineEdit_website_url.setText(config.WEBSITE_URL)
    ui.lineEdit_login_username.setText(config.LOGIN_USERNAME)
    ui.lineEdit_login_password.setText(config.LOGIN_PASSWORD)

    ui.spinBox_wait_timeout.setValue(config.WAIT_TIMEOUT)
    ui.spinBox_sale_number.setRange(0, 9999)
    ui.spinBox_sale_number.setValue(config.SALE_NUMBER)
    ui.spinBox_buy_number.setRange(1, 9999)
    ui.spinBox_buy_number.setValue(config.BUY_NUMBER)
    ui.doubleSpinBox_profit_margin.setValue(config.PROFIT_MARGIN)

    ui.checkBox_save_page.setChecked(config.SAVE_PAGE)

    time_button_group = QButtonGroup()
    radio1 = ui.radioButton_day
    radio2 = ui.radioButton_hour
    radio3 = ui.radioButton_minutes
    print(radio1.text(), radio2.text(), radio3.text())
    time_button_group.addButton(radio1)
    time_button_group.addButton(radio2)
    time_button_group.addButton(radio3)

    pushButton_read_settings = ui.pushButton_read_settings.text()


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/pop_dialog.ui", self)
        self.setWindowTitle("象岛设置")

        self.save_button.clicked.connect(self.save_settings)

    @pyqtSlot()
    def save_settings(self):
        print("保存设置")
        self.close()


def open_settings_dialog():
    settings_dialog = SettingsDialog()
    settings_dialog.show()
    sys.exit(settings_dialog.exec())


def bind_slots(ui):
    # 象岛设置按钮
    ui.pushButton_read_settings.clicked.connect(lambda: open_settings_dialog())

    ui.button_update_config.clicked.connect(
        lambda: update_config(ui.lineEdit_sale_number, ui.lineEdit_buy_number, ui.lineEdit_profit_margin,
                              ui.checkBox_save_page))
    ui.pushButton_run_now.clicked.connect(run_now)
    ui.pushButton_run_now.clicked.connect(lambda: run_now_process_bar(ui.statusbar))

    ui.pushButton_6.clicked.connect(
        lambda: cal(int(ui.lineEdit_4.text()), int(ui.lineEdit_5.text()), ui.lineEdit_6) if validate_input(
            ui.lineEdit_4, ui.lineEdit_5) else None)
    ui.pushButton_6.clicked.connect(lambda: style(ui.lineEdit_6))

    ui.pushButton_6.clicked.connect(lambda: print_result(ui.plainTextEdit))
