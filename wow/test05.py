# 最小化也能用，厉害
import ctypes, win32con, win32api, win32gui
from netAssist import time
import random


class findWOW:
    def __init__(self):
        self = self.__init__()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    def printFindWindows(self):

        for h, t in hwnd_title.items():
            # if t == "魔兽世界":
            if t == "*无标题 - 记事本":
                print(hex(h), t, len(hwnd_title))


hwnd_title = dict()
findWOW = findWOW()
win32gui.EnumWindows(findWOW.get_all_hwnd(), 0)
findWOW.printFindWindows()
