from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from datetime import date, timedelta


def select_date(set_value):
    # with popup('Select Date'):
    put_buttons(['Today'], onclick=[lambda: set_value(date.today(), 'Today')])
    put_buttons(['Yesterday'], onclick=[lambda: set_value(date.today() - timedelta(days=1), 'Yesterday')])


def main():
    d = input('Date', action=('Select', select_date), readonly=True)
    put_text(type(d), d)


if __name__ == '__main__':
    start_server(main, port=8080)
