import ctypes, win32con, win32api, win32gui
from netAssist import time
import random

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(
            hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t == "*无标题 - 记事本":
        print(hex(h), t, len(hwnd_title))

list_wow = list(hwnd_title)
