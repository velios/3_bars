import json
import os
import argparse
from math import hypot


def load_json_data(filepath, encoding='utf-8'):
    if not os.path.exists(filepath):
        print('Неверное имя или файл "{0}" не существет'.format(filepath))
    with open(filepath, 'r', encoding=encoding) as data_file:
        return json.loads(data_file.read())


def pretty_print_json(prepared_json_data):
    return json.dumps(prepared_json_data, sort_keys=True, indent=4,
                      separators=(',', ': '), ensure_ascii=False)


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
        distance_between_me_and_bar = hypot(longitude_difference,
                                            latitude_difference)
        if closest_bar_distance is None:
            closest_bar_distance = distance_between_me_and_bar
            closest_bar = bar['Name']
        else:
            if closest_bar_distance > distance_between_me_and_bar:
                closest_bar_distance = distance_between_me_and_bar
                closest_bar = bar['Name']
    return closest_bar, int(closest_bar_distance*100000)


if __name__ == '__main__':
    parser_description = """
    Скрипт на вход принимает путь до файла содержащих информацию о барах Москвы в JSON формате и определяет
    самый большой, маленький и ближайший к точке назначения бар
    Файл для примера можно скачать на https://data.mos.ru/
    """
    cmd_argument_parser = argparse.ArgumentParser(description=parser_description)
    cmd_argument_parser.add_argument('filepath', help='Файл с данными о барах Москвы в JSON формате', type=str)
    cmd_argument_parser.add_argument('-t', '--test', action='store_true', help='Не потребуется вводить данные с клавиатуры. Тестовый режим.')
    cmd_arguments = cmd_argument_parser.parse_args()

    bars_data = load_json_data(cmd_arguments.filepath, encoding='cp1251')

    if not cmd_arguments.test:
        current_longitude = float(input('Пожалуйста введите долготу(например 37.566316):'))
        current_latitude = float(input('Пожалуйста введите широту(например 55.723065):'))
    else:
        current_longitude = 37.566316
        current_latitude = 55.723065
        print('Тестовый режим. Заранее заданные значения долготы:{} и широты:{}'.format(current_latitude,current_longitude))

    biggest_bar, biggest_bar_number_of_seats = get_biggest_bar(bars_data)
    smallest_bar, smallest_bar_number_of_seats = get_smallest_bar(bars_data)
    closest_bar, closest_bar_distance = get_closest_bar(bars_data,
                                                        current_longitude, current_latitude)


    print('\nСамый вместительный бар это {0} на {1} мест'.format(biggest_bar,
                                                               biggest_bar_number_of_seats))
    print('Самый маленький бар это {0} на {1} мест'.format(smallest_bar,
                                                           smallest_bar_number_of_seats))
    print('Ближайший к вам бар это {0} на расстоянии {1} метра\n'.format(closest_bar,
                                                                       closest_bar_distance))
    print('Спасибо что воспользовались приложением.')

