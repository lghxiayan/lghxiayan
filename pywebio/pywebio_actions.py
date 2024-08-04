from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


def hello():
    put_markdown('### Hello World!')


def main():
    confirm = actions('确认删除文件?',
                      [{'label': '确认', 'value': 1, 'type': 'submit', 'disabled': False, 'color': 'primary'},
                       {'label': '取消', 'value': 0, 'type': 'submit', 'disabled': False,
                        'color': 'secondary'},
                       {'label': '取消1', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'success'},
                       {'label': '取消2', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'danger'},
                       {'label': '取消3', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'warning'},
                       {'label': '取消4', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'info'},
                       {'label': '取消5', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'light'},
                       {'label': '取消6', 'value': 0, 'type': 'submit', 'disabled': False, 'color': 'dark'}],
                      help_text='文件删除后不能恢复!')
    if confirm == 1:
        hello()
    put_markdown(f'你点击了{confirm}按钮!')


start_server(main, port=8080, debug=True)
