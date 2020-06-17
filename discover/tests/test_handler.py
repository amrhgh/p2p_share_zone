import socket
from time import sleep
from unittest import TestCase

from discover.handler import DiscoverConnection
from discover.zone_manager import return_zone, zone_path


class ConnectionTest(TestCase):
    def setUp(self):
        first_connection_ip = 'localhost'
        first_connection_port = 8000
        second_connection_ip = 'localhost'
        second_connection_port = 8888
        self.first_connection_conf = (first_connection_ip, first_connection_port)
        self.second_connection_conf = (second_connection_ip, second_connection_port)

    def test_send_and_receive(self):
        open(zone_path, 'w').close()
        try:
            first_connection = DiscoverConnection(*self.first_connection_conf)
            second_connection = DiscoverConnection(*self.second_connection_conf)
            second_connection.send_zone(['hi', ], *self.first_connection_conf)
            sleep(0.5)
            file = open(zone_path)
            file_data = file.read()
        finally:
            file.close()
            first_connection.close()
            second_connection.close()
        self.assertEqual('\nhi', file_data)

    def test_send_zone(self):
        file = open(zone_path, 'w')
        file.write('NS1 127.0.0.1 8888')
        file.close()
        try:
            first_connection = DiscoverConnection(*self.first_connection_conf)
            second_connection = DiscoverConnection(*self.second_connection_conf)
            second_connection.send_zone(return_zone(), *self.first_connection_conf)
            sleep(0.5)
            file = open(zone_path)
            file_data = file.read()
        finally:
            file.close()
            first_connection.close()
            second_connection.close()
        self.assertTrue('NS1 127.0.0.1 8888' in file_data)

    def test_start_send_zone_thread(self):
        file = open(zone_path, 'w')
        file.write('NS1 127.0.0.1 8000')
        file.close()
        try:
            first_connection = DiscoverConnection(*self.first_connection_conf)
            second_connection = DiscoverConnection(*self.second_connection_conf)
            # second_connection.send_zone(return_zone(), *self.first_connection_conf)
            sleep(4)
            file = open(zone_path)
            file_data = file.read()
        finally:
            file.close()
            first_connection.close()
            second_connection.close()
        self.assertTrue('NS1 127.0.0.1 8000' in file_data)
