import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf.conf_reader import config
from db.models import Zone

zone_path = os.path.dirname(__file__) + '/zone.txt'

db_path = os.path.dirname(__file__) + '/database.sqlite'

engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def get_client_record():
    name = config.get('General', 'name')
    ip = config.get('General', 'ip')
    port = config.get('Discover', 'port')
    return f'{name} {ip} {port}'


def return_zone():
    """
    :return: zone file as list witch the current client info is included
    """
    records = session.query(Zone).all()
    records.append(get_client_record())
    return records


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
    if received_zone == b'':  # in the event that nothing to update
        return
    received_zone = received_zone.decode()
    zone_list = return_zone()
    new_records = list()
    for record in received_zone.split('\n'):
        name, ip, port = record.split()
        if record not in zone_list:
            new_records.append(record)
    if new_records:
        append_list_to_file(zone_path, new_records)


def get_nodes_name(zone_list):
    """
    get names of all nodes exist in zone list
    """
    names = list()
    for node in zone_list:
        name, address = node.split(' ', 1)
        names.append(name)
    return names


def zone_list_to_dict(zone_list):
    zone_dic = dict()
    for record in zone_list:
        name, ip, port = record.split()
        zone_dic.update({name: {'ip': ip, 'port': port}})
    return zone_dic