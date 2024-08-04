"""
我写的程序的入口,每个程序一个按钮, 每个按钮对应一个程序
上面是按钮,下面的日志输出窗口
"""
import os.path
import sys
import time

from pywebio.session import local
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import runpy

import concurrent.futures
import threading


def add():
    with use_scope('log_output'):
        bottom_01 = '我点击了按钮1'
        put_text(f'{bottom_01}', scope='log_output')
        get_scope()


def config_selenium_script():
    bottom_02 = '运行配置[象岛数据提取程序]参数'
    with use_scope('log_output', clear=True):
        put_text(bottom_02, scope='log_output')
        get_scope()
        # clear()
        runpy.run_module('config_ptvicomo_04_in_pywebio', run_name='__main__')


def run_selenium_script_in_thread():
    """在单独的线程中运行selenium脚本"""

    def run_script():
        runpy.run_module('selenium_ptvicomo_cookie_04', run_name='__main__')

    thread = threading.Thread(target=run_script)
    thread.start()

    return thread


def run_selenium_script():
    bottom_03 = '运行象岛数据提取程序'
    with use_scope('log_output', clear=True):
        put_text(bottom_03, scope='log_output')
        get_scope()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_selenium_script_in_thread)
            thread = future.result()

        put_progressbar('bar')
        """进度条"""
        for i in range(101):
            set_progressbar('bar', i / 100)
            time.sleep(0.05)

        thread.join()


def get_lgh_form_script():
    bottom_04 = '运行[龙感湖人员信息表单录入]程序'
    with use_scope('log_output', clear=True):
        put_text(bottom_04, scope='log_output')
        get_scope()
        # clear()
        runpy.run_module('input_lgh_info_01_in_pywebio', run_name='__main__')


def main():
    with use_scope('ROOT', clear=True):
        put_buttons(['增加统计数值', '配置[提取象岛数据]参数', '提取象岛数据', '龙感湖人员信息表单录入'],
                    [add, config_selenium_script, run_selenium_script, get_lgh_form_script])

        # confirm = actions('运行我的代码',
        #                   [{'label': '增加统计数值', 'value': add(), 'type': 'submit', 'disabled': False,
        #                     'color': 'primary'},
        #                    {'label': '配置[提取象岛数据]参数', 'value': config_selenium_script(), 'type': 'submit',
        #                     'disabled': False, 'color': 'danger'},
        #                    {'label': '提取象岛数据', 'value': run_selenium_script(), 'type': 'submit',
        #                     'disabled': False,
        #                     'color': 'info'}], help_text='不要点击太频繁!')
        # put_markdown(f'你点击了{confirm}按钮!')

        get_scope()
        put_text('日志输出:')


if __name__ == '__main__':
    try:
        start_server(main, 8001)
    except Exception as e:
        put_text("Server failed to start: %s", str(e))
        # 向用户显示错误信息（仅在开发模式下推荐使用）
        put_text(f"应用发生内部错误: {str(e)}")
        sys.exit(1)
