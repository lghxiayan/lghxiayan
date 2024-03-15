# 最小化也能用，厉害
import ctypes, win32con, win32api, win32gui
from netAssist import time
from pykeyboard import PyKeyboardEvent

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and (
            win32gui.GetWindowText(hwnd) == "魔兽世界"):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t == "魔兽世界":
        # if t == "*无标题 - 记事本":
        print(hex(h), t, len(hwnd_title))

isLoop = True


class Keyb(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.input = ""

    def tap(self, keycode, character, press):
        print(keycode, character, press)
        global isLoop
        if press and keycode == 116:
            pressKey()


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
    GetWindowThreadProcessId = _user32.GetWindowThreadProcessId

    hwnd1 = 0x2040a58  # 第一个WOW窗口。FS
    hwnd2 = 0x4618be  # 第二个WOW窗口。DLY
    hwnd3 = 0xc707c6  # 第三个WOW窗口。qs
    current = win32api.GetCurrentThreadId()
    print('current:' + str(current))

    ThreadId1 = GetWindowThreadProcessId(hwnd1, None)
    print(ThreadId1)
    ThreadId2 = GetWindowThreadProcessId(hwnd2, None)
    print(ThreadId2)
    ThreadId3 = GetWindowThreadProcessId(hwnd3, None)
    print(ThreadId3)

    win32gui.SendMessage(hwnd1, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(hwnd2, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(hwnd3, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

    # AttachThreadInput(current, hwnd1, True)
    # AttachThreadInput(current, hwnd2, True)
    # AttachThreadInput(current, hwnd3, True)
    AttachThreadInput(ThreadId1, hwnd1, True)
    AttachThreadInput(ThreadId2, hwnd2, True)
    AttachThreadInput(ThreadId3, hwnd3, True)

    GetKeyboardState(ctypes.byref(oldKeyboardState))
    SetKeyboardState(ctypes.byref(keyboardStateBuffer))

    FS = True
    MS = False

    DLY = False

    QS = True

    for i in range(30):
        if FS:
            FS_list = [ord('W')]
            for j in range(len(FS_list)):
                exec('FSKey' + str(j) + '=' + str(FS_list[j]))
                lparam1 = win32api.MAKELONG(0, MapVirtualKeyA(FS_list[j], 0)) | 0x00000001
                win32api.PostMessage(hwnd1, win32con.WM_KEYDOWN, FS_list[j], lparam1)
                time.sleep(0.1)
                win32api.PostMessage(hwnd1, win32con.WM_KEYUP, FS_list[j], lparam1 | 0xC0000000)
                time.sleep(0.1)
        if MS:
            MS_list = [ord('X')]
            for j in range(len(MS_list)):
                exec('MSKey' + str(j) + '=' + str(MS_list[j]))
                lparam4 = win32api.MAKELONG(0, MapVirtualKeyA(MS_list[j], 0)) | 0x00000001
                win32api.PostMessage(hwnd3, win32con.WM_KEYDOWN, MS_list[j], lparam4)
                time.sleep(0.1)
                win32api.PostMessage(hwnd3, win32con.WM_KEYUP, MS_list[j], lparam4 | 0xC0000000)
                time.sleep(0.1)

        if DLY:
            DLY_list = [ord('Q')]
            for j in range(len(DLY_list)):
                exec('DLYKey' + str(j) + '=' + str(DLY_list[j]))
                lparam2 = win32api.MAKELONG(0, MapVirtualKeyA(DLY_list[j], 0)) | 0x00000001
                win32api.PostMessage(hwnd2, win32con.WM_KEYDOWN, DLY_list[j], lparam2)
                time.sleep(0.1)
                win32api.PostMessage(hwnd2, win32con.WM_KEYUP, DLY_list[j], lparam2 | 0xC0000000)
                time.sleep(0.1)
        if QS:
            QS_list = [ord('Z')]
            for j in range(len(QS_list)):
                exec('QSKey' + str(j) + '=' + str(QS_list[j]))
                lparam4 = win32api.MAKELONG(0, MapVirtualKeyA(QS_list[j], 0)) | 0x00000001
                win32api.PostMessage(hwnd3, win32con.WM_KEYDOWN, QS_list[j], lparam4)
                time.sleep(0.1)
                win32api.PostMessage(hwnd3, win32con.WM_KEYUP, QS_list[j], lparam4 | 0xC0000000)
                time.sleep(0.1)

        # print(i)

        SetKeyboardState(ctypes.byref(oldKeyboardState))
        time.sleep(0.1)

        # AttachThreadInput(current, hwnd1, False)
        # AttachThreadInput(current, hwnd2, False)
        # AttachThreadInput(current, hwnd3, False)
        AttachThreadInput(ThreadId1, hwnd1, False)
        AttachThreadInput(ThreadId2, hwnd2, False)
        AttachThreadInput(ThreadId3, hwnd3, False)


k = Keyb()
k.run()
