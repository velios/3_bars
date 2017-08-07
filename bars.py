import json
import os
from math import hypot


def load_json_data(filepath, encoding='utf-8'):
    if not os.path.exists(filepath):
        print('Неверное имя или файл "{0}" не существет'.format(filepath))
    with open(filepath, 'r', encoding=encoding) as data_file:
        return json.loads(data_file.read())


def pretty_print_json(prepared_json_data):
    return json.dumps(prepared_json_data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


def get_biggest_bar(bars_data):
    biggest_bar_number_of_seats = 0
    for bar in bars_data:
        if bar['SeatsCount'] > biggest_bar_number_of_seats:
            biggest_bar_number_of_seats = bar['SeatsCount']
            biggest_bar = bar['Name']
    return biggest_bar, biggest_bar_number_of_seats


def get_smallest_bar(bars_data):
    smallest_bar_number_of_seats = bars_data[0]['SeatsCount']
    for bar in bars_data:
        if bar['SeatsCount'] < smallest_bar_number_of_seats:
            smallest_bar_number_of_seats = bar['SeatsCount']
            smallest_bar = bar['Name']
    return smallest_bar, smallest_bar_number_of_seats


def get_closest_bar(bars_data, longitude, latitude):
    closest_bar, closest_bar_distance = None, None
    for bar in bars_data:
        bar_longitude = float(bar['Longitude_WGS84'])
        bar_latitude = float(bar['Latitude_WGS84'])
        longitude_difference = longitude - bar_longitude
        latitude_difference = latitude - bar_latitude
        distance_between_me_and_bar = hypot(longitude_difference, latitude_difference)
        if closest_bar_distance is None:
            closest_bar_distance = distance_between_me_and_bar
            closest_bar = bar['Name']
        else:
            if closest_bar_distance > distance_between_me_and_bar:
                closest_bar_distance = distance_between_me_and_bar
                closest_bar = bar['Name']

    return closest_bar, int(closest_bar_distance*100000)


if __name__ == '__main__':
    # Пропишете путь до списка московских баров в JSON формате с сайта https://data.mos.ru/opendata/7710881420-bary
    PATH_TO_DATA_FILE = 'data-2897-2016-11-23.json'

    try:
        bars_data = load_json_data(PATH_TO_DATA_FILE, encoding='cp1251')

        current_longitude = float(input('Пожалуйста введите долготу(например 37.566316): '))
        current_latitude = float(input('Пожалуйста введите широту(например 55.723065): '))

        biggest_bar, biggest_bar_number_of_seats = get_biggest_bar(bars_data)
        smallest_bar, smallest_bar_number_of_seats = get_smallest_bar(bars_data)
        closest_bar, closest_bar_distance = get_closest_bar(bars_data, current_longitude, current_latitude)

        print('Самый вместительный бар это {0} на {1} мест'.format(biggest_bar, biggest_bar_number_of_seats))
        print('Самый маленький бар это {0} на {1} мест'.format(smallest_bar, smallest_bar_number_of_seats))
        print('Ближайший к вам бар это {0} на расстоянии {1} метра'.format(closest_bar, closest_bar_distance))
        print('Спасибо что воспользовались приложением.')
    except:
        print('Что-то пошло не так. Проверьте правильно ли вы указали путь до файла.')
