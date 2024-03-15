from pywebio.session import local
from pywebio.output import *
from pywebio import start_server


def add():
    local.cnt = (local.cnt or 0) + 1
    print(type(local), local)


def show():
    put_text(local.cnt or 0)


def main():
    put_buttons(['Add counter', 'Show counter'], [add, show])


if __name__ == '__main__':
    start_server(main, 8088)
