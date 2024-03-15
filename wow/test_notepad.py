# 最小化也能用，厉害
import ctypes, win32con, win32api, win32gui
from netAssist import time
from pykeyboard import PyKeyboardEvent

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and (
            win32gui.GetWindowText(hwnd) == "无标题 - 记事本"):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    # if t == "魔兽世界":
    print(h, t)
    if t == "*无标题 - 记事本":
        print(hex(h), t, len(hwnd_title))
