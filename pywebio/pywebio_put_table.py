from pywebio.output import *
from pywebio import start_server


def main():
    put_table([
        [span('Name', row=2), span('Address', col=2)],
        ['City', 'Country'],
        ['Wang', 'Beijing', 'China'],
        ['Liu', 'New York', 'America']
    ])

    put_table([
        ['Type', 'Content'],
        ['html', put_html('X<sup>2</sup>')],
        ['text', '<hr/>'],
        ['button', put_buttons(['A', 'B'], onclick=put_text)],
        ['markdown', put_markdown('`Awesome PyWebIO!`')],
        ['file', put_file('hello.txt', b'hello world!')],
        ['table', put_table([['A', 'B'], ['C', 'D']])]
    ])

    put_table([
        ['Wang', 'M', 'China'],
        ['Liu', 'W', 'America']
    ], header=['Name', 'Gender', 'Address'])

    put_table([
        {'Course': 'OS', 'Score': '80'},
        {'Course': 'DB', 'Score': '93'}
    ], header=['Course', 'Score'])


if __name__ == '__main__':
    start_server(main, 8088)
