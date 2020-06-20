import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from conf.conf_reader import config
from db.models import Zone

zone_path = os.path.dirname(__file__) + '/zone.txt'

db_path = os.path.dirname(__file__) + '/database.sqlite'

engine = create_engine(f'sqlite:///{db_path}', echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


def get_client_record():
    name = config.get('General', 'name')
    ip = config.get('General', 'ip')
    port = config.get('Discover', 'port')
    return Zone(name=name, ip=ip, port=port)


def return_zone_in_string():
    """
    :return: zone file as list witch the current client info is included
    """
    records = session.query(Zone).all()
    records.append(get_client_record())
    records = [f'{item.name} {item.ip} {item.port}' for item in records]
    return records


def append_list_to_database(new_records):
    """
    append new records to database
    """
    new_nodes = list()
    for record in new_records:
        name, ip, port = record.split()
        new_nodes.append(Zone(name=name, ip=ip, port=port))
    session.add_all(new_nodes)
    session.commit()


def update_zone(received_zone):
    """
    add new records to zone
    """
    if received_zone == b'':  # in the event that nothing to update
        return
    received_zone = received_zone.decode()
    new_records = list()
    for record in received_zone.split('\n'):
        name, ip, port = record.split()
        if not session.query(Zone).filter_by(name=name).first():
            new_records.append(record)
    if new_records:
        append_list_to_database(new_records)
