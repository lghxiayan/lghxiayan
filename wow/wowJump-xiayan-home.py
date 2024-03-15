# 这个是用来挂机的，随机sleep1到100秒，然后按一下W
import ctypes, win32con, win32api, win32gui
from netAssist import time
import random

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(
            hwnd) and win32gui.GetWindowText(hwnd) == "魔兽世界":
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

# globals(wowHex='')


for h, t in hwnd_title.items():
    if t == "魔兽世界":
        # if t == "*无标题 - 记事本":
        print(hex(h), t, len(hwnd_title))
        # wowHex=hex(h)

list_wow = list(hwnd_title)


# print(wowHex)

def pressKey():
    PBYTE256 = ctypes.c_ubyte * 256
    _user32 = ctypes.WinDLL("user32")

    GetKeyboardState = _user32.GetKeyboardState
    SetKeyboardState = _user32.SetKeyboardState
    MapVirtualKeyA = _user32.MapVirtualKeyA
    AttachThreadInput = _user32.AttachThreadInput
    oldKeyboardState = PBYTE256()
    keyboardStateBuffer = PBYTE256()

    GetKeyboardState(ctypes.byref(oldKeyboardState))

    hwnd1 = 0x50c10  # 第一个WOW窗口。FS
    # hwnd1 = list_wow[0]  # 第一个WOW窗口。FS

    current = win32api.GetCurrentThreadId()
    win32gui.SendMessage(hwnd1, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    AttachThreadInput(current, hwnd1, True)

    GetKeyboardState(ctypes.byref(oldKeyboardState))
    SetKeyboardState(ctypes.byref(keyboardStateBuffer))

    FS = True

    for i in range(900000):
        if FS:
            FS_list = [ord('S')]
            for j in range(len(FS_list)):
                exec('FSKey' + str(j) + '=' + str(FS_list[j]))
                lparam1 = win32api.MAKELONG(0, MapVirtualKeyA(FS_list[j], 0)) | 0x00000001
                win32api.PostMessage(hwnd1, win32con.WM_KEYDOWN, FS_list[j], lparam1)
                time.sleep(0.01)
                win32api.PostMessage(hwnd1, win32con.WM_KEYUP, FS_list[j], lparam1 | 0xC0000000)
                time.sleep(0.01)
                time.sleep(random.randint(1, 10))
        print(i)

    SetKeyboardState(ctypes.byref(oldKeyboardState))
    time.sleep(5)

    AttachThreadInput(current, hwnd1, False)


pressKey()
