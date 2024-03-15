# 最小化也能用，厉害
import ctypes, win32con, win32api, win32gui
from netAssist import time

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t == "魔兽世界":
        print(hex(h), t)

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")

GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
MapVirtualKeyA = _user32.MapVirtualKeyA
AttachThreadInput = _user32.AttachThreadInput
oldKeyboardState = PBYTE256()
keyboardStateBuffer = PBYTE256()
GetKeyboardState(ctypes.byref(oldKeyboardState))

# hwnd = 0x00050BB4  # hwnd окна Edit процесса notepad
hwnd1 = 0x000d19a2  # 第一个WOW窗口。FS
hwnd2 = 0x0008195e  # 第二个WOW窗口。FS
current = win32api.GetCurrentThreadId()

key1 = 'E'
key1 = ord(key1)

key2 = 'X'
key2 = ord(key2)

lparam1 = win32api.MAKELONG(0, MapVirtualKeyA(key1, 0)) | 0x00000001
lparam2 = win32api.MAKELONG(0, MapVirtualKeyA(key2, 0)) | 0x00000001

win32gui.SendMessage(hwnd1, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
win32gui.SendMessage(hwnd2, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

AttachThreadInput(current, hwnd1, True)
AttachThreadInput(current, hwnd2, True)

GetKeyboardState(ctypes.byref(oldKeyboardState))
SetKeyboardState(ctypes.byref(keyboardStateBuffer))

first = False

for i in range(30):
    if first:
        win32api.PostMessage(hwnd1, win32con.WM_KEYDOWN, key1, lparam1)
        time.sleep(0.1)
        win32api.PostMessage(hwnd1, win32con.WM_KEYUP, key1, lparam1 | 0xC0000000)
        time.sleep(0.1)
    win32api.PostMessage(hwnd2, win32con.WM_KEYDOWN, key2, lparam2)
    time.sleep(0.1)
    win32api.PostMessage(hwnd2, win32con.WM_KEYUP, key2, lparam2 | 0xC0000000)
    time.sleep(0.1)

    SetKeyboardState(ctypes.byref(oldKeyboardState))
    time.sleep(0.1)

    AttachThreadInput(current, hwnd1, False)
    AttachThreadInput(current, hwnd2, False)
