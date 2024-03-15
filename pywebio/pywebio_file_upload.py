from pywebio.input import *
from pywebio.output import *
from pywebio import start_server


def main():
    imgs = file_upload('Select some pictures', accept='image/*', multiple=True)
    for img in imgs:
        put_image(img['content'])


if __name__ == '__main__':
    start_server(main, port=8080)
