# -*- coding: utf-8 -*-
import os
import sys

import pyWinhook as pyHook
import pythoncom
import win32api
import win32con
import win32gui
from win32com.client import GetObject

hWndList = []
flag = 0


def onMouseEvent(event):
    global flag
    global hWndList
    # 监听鼠标事件
    # if event.Position == (0, 0): 区域放大点好了
    if event.Position[0] < 3 and event.Position[1] < 3 and flag == 0:
        flag = 1
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        cnt = 0
        for h in hWndList:
            str = show_window_attr(h)
            if "1.txt" in str:
                cnt = cnt + 1
        if cnt < 1:
            # print(cnt,"***************************************")
            if os.path.exists('./1.txt') is True:
                try:
                    os.system("start 1.txt")
                except:
                    win32api.MessageBox(0, "打开1.txt异常", os.path.basename(sys.argv[0]) + "提示",
                                        win32con.MB_OK)
                    print("打开1.txt异常")
            else:
                win32api.MessageBox(0, "1.txt不存在", os.path.basename(sys.argv[0]) + "提示",
                                    win32con.MB_OK)
                print("1.txt不存在")
        else:
            win32api.MessageBox(0, "已打开1.txt", os.path.basename(sys.argv[0]) + "提示",
                                win32con.MB_OK)
            print("已打开1.txt")
        flag = 0

    else:
        if len(hWndList) != 0:
            hWndList.clear()

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def gbk2utf8(s):
    # return s.decode('gbk').encode('utf-8')
    return s.encode('utf-8')


def show_window_attr(hWnd):
    '''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return ""

    # 中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    title = gbk2utf8(title)

    # print("窗口句柄:", hWnd)
    # print("窗口标题:", str(title, encoding="utf-8"))#字节流转字符串
    # print("窗口类名:", clsname)
    return str(title, encoding="utf-8")  # 返回窗口标题字符串


def main():
    wmi = GetObject('winmgmts:')
    processes = wmi.ExecQuery('Select * from Win32_Process where Name = "' + os.path.basename(sys.argv[0]) + '"')
    if len(processes) > 2:
        win32api.MessageBox(0, os.path.basename(sys.argv[0]) + "已在后台运行，请勿重复打开",
                            os.path.basename(sys.argv[0]) + "提示", win32con.MB_OK)
        os._exit(0)
    try:
        # 创建一个“钩子”管理对象
        hm = pyHook.HookManager()

        # 监听所有鼠标事件
        hm.MouseAll = onMouseEvent
        # 设置鼠标“钩子”
        hm.HookMouse()

        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()
    except:
        print("运行失败")


if __name__ == "__main__":
    main()
