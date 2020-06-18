import os

from pyTorrent_conf.conf_reader import config

zone_path = os.path.dirname(__file__) + '/zone.txt'


def get_client_record():
    name = config.get('General', 'name')
    ip = config.get('General', 'ip')
    port = config.get('Discover', 'port')
    return f'{name} {ip} {port}'


def return_zone():
    """
    :return: zone file as list witch the current client info is included
    """
    with open(zone_path, 'r') as file:
        zone_file = file.read().splitlines()
    zone_file.append(get_client_record())
    return zone_file


def append_list_to_file(path, new_lines):
    file = open(path, 'a+')
    new_lines = '\n'.join(new_lines)
    if file.tell() != 0:
        file.write('\n' + new_lines)
    else:
        file.write(new_lines)
    file.close()


def update_zone(received_zone):
    """
    add new records to zone
    :param received_zone: get current zone records appended current client info
    """
    received_zone = received_zone.decode()
    zone_list = return_zone()
    new_records = list()
    for record in received_zone.split('\n'):
        if record not in zone_list:
            new_records.append(record)
    if new_records:
        append_list_to_file(zone_path, new_records)
