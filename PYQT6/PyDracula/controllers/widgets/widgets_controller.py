from PySide6.QtWidgets import QPushButton


class WidgetsController:
    def __init__(self, ui):
        self.ui = ui
        self.setup_connections()

    def setup_connections(self):
        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        print("Widgets里面的 pushButton 被点击了！")
        plainTextEdit = self.ui.plainTextEdit
        plainTextEdit.appendPlainText("Widgets里面的 pushButton 被点击了！")
