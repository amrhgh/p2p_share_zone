from db.zone_manager import return_zone_in_string, zone_path, session
from time import sleep
from unittest import TestCase

from db.models import Zone
from discover.handler import DiscoverConnection


class ConnectionTest(TestCase):
    def setUp(self):
        first_connection_ip = 'localhost'
        first_connection_port = 8000
        second_connection_ip = 'localhost'
        second_connection_port = 8888
        self.first_connection_conf = (first_connection_ip, first_connection_port)
        self.second_connection_conf = (second_connection_ip, second_connection_port)

    def test_send_and_receive(self):
        session().query(Zone).delete()
        session().commit()
        try:
            first_connection = DiscoverConnection(*self.first_connection_conf, start_send_zone_thread=False)
            second_connection = DiscoverConnection(*self.second_connection_conf, start_send_zone_thread=False
                                                   , start_receiving_server=False)
            second_connection.send_zone(['NS10 1.0.0.1 8888 1', ], *self.first_connection_conf)
            sleep(0.5)
        finally:
            first_connection.close()
            second_connection.close()
        obj = session().query(Zone).filter_by(name='NS10').first()
        self.assertIsNotNone(obj)

    def test_check_session_not_raise_exception(self):
        session().query(Zone).delete()
        session().commit()
        try:
            first_connection = DiscoverConnection(*self.first_connection_conf)
            second_connection = DiscoverConnection(*self.second_connection_conf)
            sleep(2)
        finally:
            first_connection.close()
            second_connection.close()
