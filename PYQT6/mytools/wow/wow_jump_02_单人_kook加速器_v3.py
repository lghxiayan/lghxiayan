"""
该代码适合单人按键使用，使用的是ctypes库，这个相对比较复杂。
按下左Ctrl键后，会自动运行。按下ESC键后，会停止运行。再次按CTRL后又会重新运行。
不管是直接运行wow.exe还是使用加速器启动wow.exe，目前可以正常运行。

运行本脚本，需要使用管理员权限运行pycharm,否则可能不能向目标窗口发送按键

对于使用加速器启动wow.exe，加速器应该是给wow.exe加了一层窗口，导致v1版本无法找到wow窗口。现在直接寻找类，就没有问题了。

之前使用进程名（例如 wow.exe）来查找目标窗口，还是有一些问题。
下面是之前使用的方案，还是有问题，所以就使用类来寻找。
使用一些系统级别的库来实现，在 Python 中，你可以使用 psutil 库来获取进程信息，并结合 pygetwindow 或 win32gui 库来查找窗口


"""

import ctypes
import time
import random
import win32api
import win32con
import win32gui
from pynput import keyboard
import threading
import logging.config
import os
from config_wowjump_01 import CONFIG

config_file_path = os.path.join(os.path.dirname(__file__), 'logging_wowjump.conf')
logging.config.fileConfig(config_file_path, encoding='utf-8')
logger = logging.getLogger('wowjump_log')
logger.setLevel(logging.INFO)


class WoWKeyPresser:
    def __init__(self, config):
        self.config = config
        # 标志变量，控制main函数的运行状态
        self.is_running = False
        self.main_thread = None
        # 是否使用随机睡眠
        self.is_sleep_random = False

    def find_wow_window(self):
        def callback(hwnd, _):
            class_name = win32gui.GetClassName(hwnd)
            window_title = win32gui.GetWindowText(hwnd)
            if class_name == self.config["WOW_CLASS_NAME"] or self.config["WINDOW_TITLE"] in window_title:
                wow_window_hwnds.append(hwnd)
            return True

        wow_window_hwnds = []
        win32gui.EnumWindows(callback, None)
        return wow_window_hwnds[0] if wow_window_hwnds else None

    def press_key(self, hwnd, keys=None, interval=None):
        """
        模拟按键操作
        :param hwnd: 窗口句柄
        :param keys: 要按下的键列表
        :param interval: 按键之间的间隔时间
        """
        if keys is None:
            keys = self.config["KEYS_TO_PRESS"]
        if interval is None:
            interval = self.config["INTERVAL_BETWEEN_KEYS"]

        try:
            pbyte256 = ctypes.c_ubyte * 256
            _user32 = ctypes.WinDLL("user32")
            old_keyboard_state = pbyte256()

            current_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            time.sleep(0.1)  # 确保窗口已激活
            _user32.AttachThreadInput(current_thread_id, hwnd, True)

            for _ in range(interval):
                for key in keys:
                    key_code = ord(key)
                    lparam = win32api.MAKELONG(0, _user32.MapVirtualKeyA(key_code, 0)) | 0x00000001
                    ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYDOWN, key_code, lparam)
                    time.sleep(0.1)
                    ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYUP, key_code, lparam | 0xC0000000)
                    time.sleep(0.1)
            _user32.GetKeyboardState(ctypes.byref(old_keyboard_state))
            _user32.AttachThreadInput(current_thread_id, hwnd, False)
        except Exception as e:
            logging.error(f"模拟按键操作时出错：{e}")

    def on_press(self, key):
        try:
            if key == keyboard.Key.ctrl_l:  # 检测左Ctrl键
                logging.info(f"按下了按键：{key}")
                if not self.is_running:
                    self.is_running = True
                    self.main_thread = threading.Thread(target=self.main)
                    self.main_thread.start()
            elif key == keyboard.Key.esc:
                logging.info(f"按下了按键：{key}")
                if self.is_running:
                    self.is_running = False
                    logging.info("停止运行main函数")
                    if self.main_thread and self.main_thread.is_alive():
                        self.main_thread.join(timeout=1)
        except Exception as e:
            logging.error(f"处理按键时出错：{e}")

    @staticmethod
    def on_release(key):
        try:
            if key == keyboard.Key.esc:  # 检测esc键退出监听
                logging.info(f"释放了按键：{key}")
        except Exception as e:
            logging.error(f"处理按键释放时出错：{e}")

    def main(self):
        hwnd = None
        for attempt in range(self.config["RETRY_ATTEMPTS"]):
            hwnd = self.find_wow_window()
            if hwnd:
                logging.info(
                    f"找到窗口：{self.config['WINDOW_TITLE']}，窗口句柄为：{hex(hwnd)}")  # 找到窗口：魔兽世界，窗口句柄为：0x31638
                break
            else:
                logging.info(f"未找到窗口：{self.config['WINDOW_TITLE']}，尝试第 {attempt + 1} 次重试...")
                time.sleep(1)
        if hwnd:
            while self.is_running:
                self.press_key(hwnd, self.config["KEYS_TO_PRESS"])
                if self.is_sleep_random:
                    time.sleep(random.randint(*self.config["SLEEP_TIME_RANGE"]))
        else:
            logging.error(f"经过 {self.config['RETRY_ATTEMPTS']} 次尝试后仍未找到窗口：{self.config['WINDOW_TITLE']}")


if __name__ == '__main__':
    key_presser = WoWKeyPresser(CONFIG)
    key_presser.is_sleep_random = False
    with keyboard.Listener(on_press=key_presser.on_press, on_release=key_presser.on_release) as listener:
        listener.join()
