import socket
from unittest import TestCase

from discover.handler import DiscoverConnection


class ConnectionTest(TestCase):
    def setUp(self):
        first_connection_ip = 'localhost'
        first_connection_port = 8000
        second_connection_ip = 'localhost'
        second_connection_port = 8888
        self.first_connection_conf = (first_connection_ip, first_connection_port)
        self.second_connection_conf = (second_connection_ip, second_connection_port)
        self.first_connection = DiscoverConnection(*self.first_connection_conf)
        self.second_connection = DiscoverConnection(*self.second_connection_conf)

    def test_receiver(self):
        self.first_connection.send_zone(*self.second_connection_conf)
        self.second_connection.send_zone(*self.first_connection_conf)
        self.first_connection.close()
        self.second_connection.close()

