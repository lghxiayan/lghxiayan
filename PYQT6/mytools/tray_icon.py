from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu


def create_system_tray_icon(app_instance, ui_instance):
    # 创建系统托盘图标
    tray_icon = QSystemTrayIcon(QIcon('./resources/slot.ico'), parent=app_instance)

    # 创建右键菜单
    tray_menu = QMenu()

    # 添加菜单项
    show_action = QAction("显示窗口", app_instance)
    show_action.triggered.connect(ui_instance.show)
    tray_menu.addAction(show_action)

    hide_action = QAction("隐藏窗口", app_instance)
    hide_action.triggered.connect(ui_instance.hide)
    tray_menu.addAction(hide_action)

    quit_action = QAction("退出", app_instance)
    quit_action.triggered.connect(app_instance.quit)
    tray_menu.addAction(quit_action)

    # 设置托盘图标的菜单
    tray_icon.setContextMenu(tray_menu)

    # 显示托盘图标
    tray_icon.show()

    return tray_icon
