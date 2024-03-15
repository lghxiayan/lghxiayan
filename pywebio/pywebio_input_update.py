from pywebio.input import *
from pywebio.output import *
from pywebio import start_server


def main():
    country2city = {
        'China': ['BeiJing', 'ShangHai', 'Hong Kong'],
        'USA': ['New York', 'Los Angeles', 'San Francisco']}

    contries = list(country2city.keys())

    location = input_group('Select a location', [
        select('Country', options=contries, name='country',
               onchange=lambda c: input_update('city', options=country2city[c])),
        select('City', options=country2city[contries[0]], name='city')
    ])
    put_text(location)


if __name__ == '__main__':
    start_server(main, port=8088)
