from pywebio.input import *
from pywebio.output import *
from pywebio import start_server


def check_form(data):
    if len(data['name']) > 6:
        return ('name', 'Name to long!')
    if data['age'] <= 0:
        return ('age', 'Age cannot be negative!')


def main():
    data = input_group('Basic info', [
        input('Input your name', name='name'),
        input('Repeat your age', name='age', type=NUMBER)
    ], validate=check_form)

    put_text(data['name'], data['age'])


if __name__ == '__main__':
    start_server(main, port=8088)
