from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


def main():
    for shape in ('border', 'grow'):
        put_html('<br>')
        for color in ('primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'):
            put_text(shape, color, inline=True)
            put_loading(shape=shape, color=color)


start_server(main, port=8080, debug=True)
