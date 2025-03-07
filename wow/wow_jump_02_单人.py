"""
该代码适合单人按键使用，使用的是ctypes库，这个相对比较复杂。
按下左Ctrl键后，会自动运行。按下ESC键后，会停止运行。再次按CTRL后又会重新运行。
目前可以正常运行。

现在已经转到【按键同步助手.exe】中去了，这个个
"""

import ctypes
import time
import random
import win32api
import win32con
import win32gui
from pynput import keyboard
import threading

# 配置项
# 指定窗口标题为"魔兽世界"，乌龟服为"World of Warcraft(32 位)",不对，找不到。
WINDOW_TITLE = "魔兽世界"
# WINDOW_TITLE = "World of Warcraft(32 位)"
# 需要按下的键列表，包括 'W', 'B', '2'
KEYS_TO_PRESS = ['W']
# 每个按键之间的间隔时间为1秒。
INTERVAL_BETWEEN_KEYS = 1
# 重试次数为3次。
RETRY_ATTEMPTS = 3
# 是否使用随机睡眠
IS_SLEEP_RANDOM = False
# 随机睡眠时间范围为1到5秒
SLEEP_TIME_RANGE = (1, 50)

# 标志变量，控制main函数的运行状态
IS_RUNNING = False
main_thread = None


def get_window_handle(title):
    """
    根据窗口标题获取窗口句柄
    :param title: 窗口标题
    :return: 窗口句柄或None
    """
    try:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd and \
                win32gui.IsWindow(hwnd) and \
                win32gui.IsWindowEnabled(hwnd) and \
                win32gui.IsWindowVisible(hwnd):
            return hwnd
        else:
            raise ValueError(f"窗口标题为 {title} 的窗口未找到。")
    except ValueError as ve:
        print(f"获取窗口句柄时出错：{ve}")
        return None
    except Exception as e:
        print(f"获取窗口句柄时发生未知错误：{e}")
        return None


def press_key(hwnd, keys=KEYS_TO_PRESS, interval=INTERVAL_BETWEEN_KEYS):
    """
    模拟按键操作
    :param hwnd: 窗口句柄
    :param keys: 要按下的键列表
    :param interval: 按键之间的间隔时间
    """
    try:
        # 定义类型和加载DLL：定义256字节的字节数组类型，并加载user32.dll
        PBYTE256 = ctypes.c_ubyte * 256
        _user32 = ctypes.WinDLL("user32")

        # 获取和设置键盘状态
        get_keyboard_state = _user32.GetKeyboardState
        set_keyboard_state = _user32.SetKeyboardState
        # 映射虚拟键：使用MapVirtualKeyA函数将虚拟键码映射到扫描码。
        map_virtual_key_a = _user32.MapVirtualKeyA
        # 附加线程输入：使用AttachThreadInput函数将当前线程的输入附加到指定窗口线程。
        attach_thread_input = _user32.AttachThreadInput

        old_keyboard_state = PBYTE256()
        key_board_state_buffer = PBYTE256()

        get_keyboard_state(ctypes.byref(old_keyboard_state))

        current_thread_id = win32api.GetCurrentThreadId()
        # 激活窗口并等待：通过SendMessage发送激活消息给窗口，并短暂休眠确保窗口已激活。
        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        time.sleep(0.1)  # 确保窗口已激活
        attach_thread_input(current_thread_id, hwnd, True)

        for _ in range(interval):
            for key in keys:
                key_code = ord(key)
                lparam = win32api.MAKELONG(0, map_virtual_key_a(key_code, 0)) | 0x00000001
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, lparam)
                time.sleep(0.1)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, lparam | 0xC0000000)
                time.sleep(0.1)

        set_keyboard_state(ctypes.byref(old_keyboard_state))
        attach_thread_input(current_thread_id, hwnd, False)

    except Exception as e:
        print(f"模拟按键操作时出错：{e}")


def main():
    hwnd = None
    for attempt in range(RETRY_ATTEMPTS):
        hwnd = get_window_handle(WINDOW_TITLE)
        if hwnd:
            print(f"找到窗口：{WINDOW_TITLE}，窗口句柄为：{hex(hwnd)}")
            break
        else:
            print(f"未找到窗口：{WINDOW_TITLE}，尝试第 {attempt + 1} 次重试...")
            time.sleep(1)

    if hwnd:
        global IS_RUNNING
        while IS_RUNNING:
            # for i in range(10000):
            press_key(hwnd, KEYS_TO_PRESS)
            # print(i)
            if IS_SLEEP_RANDOM:
                time.sleep(random.randint(*SLEEP_TIME_RANGE))
    else:
        print(f"经过 {RETRY_ATTEMPTS} 次尝试后仍未找到窗口：{WINDOW_TITLE}")


def on_press(key):
    try:
        global IS_RUNNING, main_thread
        if key == keyboard.Key.ctrl_l:  # 检测左Ctrl键
            print(f"按下了按键：{key}")
            if not IS_RUNNING:
                IS_RUNNING = True
                print("开始运行main函数")
                main_thread = threading.Thread(target=main)
                main_thread.start()
        elif key == keyboard.Key.esc:
            print(f"按下了按键：{key}")
            if IS_RUNNING:
                IS_RUNNING = False
                print("停止运行main函数")
                if main_thread and main_thread.is_alive():
                    main_thread.join(timeout=1)
    except Exception as e:
        print(f"处理按键时出错：{e}")


def on_release(key):
    try:
        if key == keyboard.Key.esc:  # 检测esc键退出监听
            print(f"释放了按键：{key}")
            # return False
    except Exception as e:
        print(f"处理按键释放时出错：{e}")


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
