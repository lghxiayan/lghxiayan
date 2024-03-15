from pywebio.output import *
from pywebio import start_server
from netAssist import time


def main():
    put_processbar('bar')
    for i in range(1, 100):
        set_processbar('bar', i / 200)
        time.sleep(0.1)


if __name__ == '__main__':
    start_server(main, 8088)
