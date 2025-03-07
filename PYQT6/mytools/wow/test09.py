import ctypes, win32con, win32api, win32gui
from netAssist import time

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")

GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
MapVirtualKeyA = _user32.MapVirtualKeyA
AttachThreadInput = _user32.AttachThreadInput
oldKeyboardState = PBYTE256()
keyboardStateBuffer = PBYTE256()
GetKeyboardState(ctypes.byref(oldKeyboardState))

hwnd = 0x000D1494  # hwnd окна Edit процесса notepad
current = win32api.GetCurrentThreadId()

key = 'A'
key = ord(key)

lparam = win32api.MAKELONG(0, MapVirtualKeyA(key, 0)) | 0x00000001
lparam_ctrl = win32api.MAKELONG(0, MapVirtualKeyA(win32con.VK_CONTROL, 0)) | 0x00000001

win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

AttachThreadInput(current, hwnd, True)

GetKeyboardState(ctypes.byref(oldKeyboardState))
keyboardStateBuffer[win32con.VK_CONTROL] |= 128
SetKeyboardState(ctypes.byref(keyboardStateBuffer))

time.sleep(0.1)  # тестирования ради
win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, lparam_ctrl)
time.sleep(0.1)
win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam)
time.sleep(0.1)
win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam | 0xC0000000)
time.sleep(0.1)
win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, lparam_ctrl | 0xC0000000)
time.sleep(0.1)

SetKeyboardState(ctypes.byref(oldKeyboardState))
time.sleep(0.1)

AttachThreadInput(current, hwnd, False)
