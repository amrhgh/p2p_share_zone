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

    def test_send_and_receive(self):
        first_connection = DiscoverConnection(*self.first_connection_conf)
        second_connection = DiscoverConnection(*self.second_connection_conf)
        self.assertEqual(second_connection.sock.sendto(b'hi', self.first_connection_conf), 2)
        first_connection.close()
        second_connection.close()
        open('/home/user/projects/pyTorrent/discover/zone.txt', 'w').close()

    def test_send_zone(self):
        self.first_connection = DiscoverConnection(*self.first_connection_conf)
        self.second_connection = DiscoverConnection(*self.second_connection_conf)
        self.second_connection.send_zone(*self.first_connection_conf)
        self.first_connection.close()
        self.second_connection.close()