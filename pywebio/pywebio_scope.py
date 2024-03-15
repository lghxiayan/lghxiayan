from pywebio.input import *
from pywebio.output import *
from pywebio import start_server


def main():
    with use_scope('scope3'):
        put_text('text1 in scope3')
        put_text('text in ROOT scope', scope='ROOT')

    put_text('text in scope3', scope='scope3')


if __name__ == '__main__':
    start_server(main, 8089)
