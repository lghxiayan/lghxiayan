# _*_coding:utf-8_*_
# Author      :ories
# File_Name   :fishing.py
# Create_Date :2020-02-26 19:31
# Description :wow fishing script
# IDE         :PyCharm
import math
from netAssist import time

import autopy as at
from pykeyboard import PyKeyboard
import pyscreenshot as ImageGrab
import cv2
import numpy as np
from collections import deque
import pyaudio
import audioop
import sounddevice as sd

# x = 0

k = PyKeyboard()

# import autopy

# 改成True为测试
dev = False
a = sd.query_devices()
# print(a)
#
sd.default.device[0] = 1  # 改成这个之后就直接监听内置声音
print('-----')


# print(a)

def check_screen_size():
    print("Checking screen size")
    img = ImageGrab.grab()
    # img.save('temp.png')
    print('img.size')
    print(img.size)

    global screen_size
    global screen_start_pointt221
    global screen_end_point
    # screen_size = (img.size[0] / 2, img.size[1] / 2)
    screen_size = (img.size[0], img.size[1])

    print(screen_size)
    screen_start_point = (screen_size[0] * 0.35, screen_size[1] * 0.35)
    # print(screen_start_point)
    screen_end_point = (screen_size[0] * 0.65, screen_size[1] * 0.65)
    # print(screen_end_point)
    print("Screen size is " + str(screen_size))


def send_float():
    print('Sending float')
    k.tap_key('1', 1)
    print('Float is sent, waiting animation')
    time.sleep(2)


def make_screenshot():
    print('进入make_screenshot')
    size = (int(screen_start_point[0]), int(screen_start_point[1]), int(screen_end_point[0]), int(screen_end_point[1]))
    print(size)
    screenshot = ImageGrab.grab(bbox=size)
    # global x
    # screenshot_name = 'var/fishing_session' + str(x) + '.png'
    screenshot_name = 'var/fishing_session' + '.png'

    screenshot.save(screenshot_name)
    return screenshot_name


def move_mouse(place):
    # print(place)
    print('进入move_mouse')
    x, y = place[0], place[1]
    # print(x, y)
    # print("Moving cursor to " + str(place))
    # print(screen_start_point[0],screen_start_point[1])
    # print(x, y)
    location_x = int(screen_start_point[0])
    location_y = int(screen_start_point[1])
    # print("location_x, location_y")
    # print(location_x, location_y)
    lx = location_x + x
    ly = location_y + y
    # print('ly, ly')
    # print(lx, ly)
    at.mouse.smooth_move(lx, ly)


def jump():
    print('Jump!')
    # autopy.key.tap(u' ')
    # k.tap_key('', 1)
    time.sleep(1)

    # at.mouse.smooth_move(500,500)


def find_float(img_name):
    print('Looking for float')
    # todo: maybe make some universal float without background?

    # 加载原始的rgb图像
    img_rgb = cv2.imread(img_name)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # 加载将要搜索的图像模板
    template = cv2.imread('var/fishing_float.png', 0)

    height, width = template.shape[:2]
    size = (int(width * 0.5), int(height * 0.5))
    template = cv2.resize(template, size, interpolation=cv2.INTER_AREA)

    # 记录图像模板的尺寸
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF)
    # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF)
    #
    # 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'
    # cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED 是最小值

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)

    print('找到的坐标')
    print(min_loc)
    top_left = (max_loc[0] + 30, max_loc[1] + 30)  # 左上角的位置
    # top_left = max_loc  # 左上角的位置

    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位置

    if dev:
        # 在原图上画矩形，测试代码，测试浮标位置能否找到
        cv2.rectangle(img_rgb, top_left, btottom_right, (0, 0, 255), 2)
        # 显示原图和处理后的图像,
        cv2.imshow("template", template)
        cv2.imshow("processed", img_rgb)
        cv2.waitKey()

    # print(min_loc)
    return top_left


def listen():
    print('Well, now we are listening for loud sounds...')
    CHUNK = 1024  # CHUNKS of bytes to read each time from mic
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 18000
    THRESHOLD = 1000  # The threshold intensity that defines silence
    # and noise signal (an int. lower than THRESHOLD is silence).
    SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
    # only silence is recorded. When this time passes the
    # recording finishes and the file is delivered.
    # Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    cur_data = ''  # current chunk  of audio data
    rel = RATE / CHUNK
    # print(rel)
    slid_win = deque(maxlen=SILENCE_LIMIT * int(rel))

    success = False
    listening_start_time = netAssist.time()
    while True:
        try:
            cur_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if (sum([x > THRESHOLD for x in slid_win]) > 0):
                print('I heart something!')
                success = True
                break
            if netAssist.time() - listening_start_time > 20:
                print('I don\'t hear anything already 20 seconds!')
                break
        except IOError:
            break

    # print "* Done recording: " + str(time.time() - start)
    stream.close()
    p.terminate()
    return success


def snatch():
    print('Snatching!')
    at.mouse.click(at.mouse.Button.RIGHT)
    # time.sleep(0.5)
    # at.mouse.click(at.mouse.Button.RIGHT)


def addBait():
    print('addBait')
    k.tap_key('u')  # u是设置的打开装备面板
    time.sleep(2)
    k.tap_key('3')
    at.mouse.smooth_move(155, 537)
    at.mouse.click(at.mouse.Button.LEFT)
    at.mouse.smooth_move(791, 155)
    at.mouse.click(at.mouse.Button.LEFT)
    time.sleep(15)
    k.tap_key('u')


def autoLogOut():
    print('自动登出')
    at.mouse.smooth_move(837, 780)
    time.sleep(1)
    at.mouse.click(at.mouse.Button.LEFT)
    time.sleep(0.5)
    at.mouse.smooth_move(650, 458)
    at.mouse.click(at.mouse.Button.LEFT)
    time.sleep(60)

    # print(k.function_keys[5])
    # k.tap_key(k.function_keys[5])
    # k.tap_key(k.numpad_keys['Home'])  # Tap 'Home' on the numpad
    # print(k)


def autoLogin():
    print('自动登录')
    at.mouse.smooth_move(1114, 118)
    at.mouse.click(at.mouse.Button.LEFT)
    time.sleep(0.1)
    at.mouse.click(at.mouse.Button.LEFT)
    time.sleep(25)


def smallLoginLogOut():
    autoLogOut()
    autoLogin()


t = 0


def calculate_time():
    t = round(netAssist.time())
    return t


def main():
    if dev:
        # 调试能否找到图片位置
        im = 'var/fishing_session.png'
        place = find_float(im)

    time.sleep(3)
    check_screen_size()
    x = 0
    time_list = []
    # addBait()
    while True:
        doc = open('./record.txt', 'a')
        t = calculate_time()
        time_list.append(t)
        print(time_list)
        if len(time_list) == 2:
            print('比较时间')
            time_difference = time_list[1] - time_list[0]
            print(str(time_difference), end=' ', file=doc)
            if 615 <= time_difference:
                print('add bait,  开始装鱼饵', file=doc)
                addBait()
                time_list.pop(0)
                continue
            time_list.pop()
        print(' start fishing')

        # print(x)
        # x += 1
        # if x % 15 == 0:
        #     print('开始装')
        #     addBait()
        #     for i in range(10):
        #         k.tap_key('q')
        #         time.sleep(1)
        #     k.tap_key('t')
        # elif x % 200 == 0:
        #     smallLoginLogOut()

        # global x
        # x += 1
        k.tap_key('t')
        for i in range(2):
            k.tap_key('2')
        send_float()
        im = make_screenshot()
        place = find_float(im)
        move_mouse(place)
        if not listen():
            print('If we didn\' hear anything, lets try again')
        snatch()
        doc.close()
    # listent221()
    # addBait()


main()
