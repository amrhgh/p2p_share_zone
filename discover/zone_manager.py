import os

from pyTorrent_conf.conf_reader import config

zone_path = os.path.dirname(__file__) + '/zone.txt'


def get_client_record():
    name = config['General']['name']
    ip = config['General']['ip']
    port = config['Discover']['port']
    return f'{name} {ip} {port}'


def return_zone():
    with open(zone_path, 'r') as file:
        zone_file = file.readlines()
    zone_file.append(get_client_record())
    return bytes('\n'.join(zone_file), encoding='UTF-8')

