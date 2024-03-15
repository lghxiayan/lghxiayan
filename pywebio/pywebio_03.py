from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from netAssist import time


def set_now_ts(set_value):
    set_value(int(netAssist.time()))


def main():
    ts = input('Timestamp', type=NUMBER, action=('NOW', set_now_ts))
    put_text('Timestamp:', ts)


if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
