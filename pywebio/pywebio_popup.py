from pywebio.output import *
from pywebio import start_server


def main():
    popup('popup title', [
        put_html('<h3>Popup Content</h3>'),
        'html:<br/>',
        put_table([['A', 'B'], ['C', 'D']]),
        put_buttons(['close_popup()'], onclick=lambda _: close_popup())
    ])


if __name__ == '__main__':
    start_server(main, 8088)
