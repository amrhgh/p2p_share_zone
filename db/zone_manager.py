import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from conf.conf_reader import config
from db.models import Zone

zone_path = os.path.dirname(__file__) + '/zone.txt'

db_path = os.path.dirname(__file__) + '/database.sqlite'

engine = create_engine(f'sqlite:///{db_path}', echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class DBConnection:
    """
    this class create because session is not thread safe and each thread should have its own session
    """
    session_dic = dict()

    def __call__(self, *args, **kwargs):
        thread_id = threading.get_ident()
        session = self.session_dic.get(thread_id)
        if not session:
            session = Session()
            self.session_dic.update({thread_id: session})
        return session


session = DBConnection()


def get_client_record():
    name = config.get('General', 'name')
    ip = config.get('General', 'ip')
    port = config.get('Discover', 'port')
    return Zone(name=name, client_ip=ip, client_port=port, distance=0)


def return_zone_in_string():
    """
    :return: zone file as list witch the current client info is included
    """
    records = session().query(Zone).all()
    records.append(get_client_record())
    records = [f'{item.name} {item.client_ip} {item.client_port} {item.distance}' for item in records]
    return records


def append_list_to_database(new_records, update_records, sender_address):
    """
    append new records to database
    """
    new_nodes = list()
    for record in new_records:
        new_nodes.append(
            Zone(name=record[0],
                 interface_ip=sender_address[0],
                 interface_port=sender_address[1],
                 client_ip=record[1],
                 client_port=record[2],
                 distance=int(record[3]) + 1))
    session().add_all(new_nodes)
    for record in update_records:
        obj = session().query(Zone).get(record[0])
        obj.interface_ip = sender_address[0]
        obj.interface_port = sender_address[1]
        obj.distance = record[1]
    session().commit()


def update_zone(received_zone, sender_address):
    """
    add new records to zone
    """
    if received_zone == b'':  # in the event that nothing to update
        return
    received_zone = received_zone.decode()
    new_records = list()
    update_records = list()
    for record in received_zone.split('\n'):
        name, client_ip, client_port, distance = record.split()
        if name == config.get('General', 'name'):
            continue
        if exist_record := session().query(Zone).filter_by(name=name).first():
            if exist_record.distance > int(distance) + 1:
                update_records.append([name, distance])
        else:
            new_records.append([name, client_ip, client_port, distance])
    if new_records:
        append_list_to_database(new_records, update_records, sender_address)
