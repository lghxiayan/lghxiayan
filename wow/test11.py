import ctypes
from netAssist import time

import win32gui, win32con, win32api

hwnd_title = dict()
findList = []


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)
for h, t in hwnd_title.items():
    if t == '*无标题 - 记事本':
        print(h, t)
        findList.append(hex(h))

print(findList[0])

win32gui.SetForegroundWindow(184751238)

VK_CODE = {"f": 70}
for i in range(10):
    win32api.keybd_event(VK_CODE["f"], 0, 0, 0)
    time.sleep(0.1)

# def pressKey():
#     PBYTE256 = ctypes.c_ubyte * 256
#     _user32 = ctypes.windll('user32')
#
#     GetKeyBoardState = _user32.GetKeyBoardState
#     SetKeyboardState = _user32.SetKeyboardState
#     MapVirtualKeyA = _user32.MapVirtualKeyA
#     AttachThreadInput = _user32.AttachThreadInput
#     oldKeyboardState = PBYTE256
#     keyboardStateBuffer = PBYTE256()
#     GetKeyBoardState(ctypes.byref(oldKeyboardState))
#
#     hwnd1 = findList[0]
#
#     current = win32api.GetCurrentThreadId()
#     win32gui.SendMessage(hwnd1, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
#     AttachThreadInput(current, hwnd1, True)
#
#     # GetKeyBoardState(ctypes.byref(oldKeyboardState))
#     SetKeyboardState(ctypes.byref(keyboardStateBuffer))
#
#     for i in range(10):
#         lparam1 = win32api.MAKELONG(0, MapVirtualKeyA(ord('Z')), 0)
#
