from unittest import TestCase

from discover.zone_manager import return_zone
from pyTorrent_conf.conf_reader import config


class ZoneTest(TestCase):
    def test_return_zone_contain_it_self(self):
        name = config['General']['name']
        ip = config['General']['ip']
        port = config['Discover']['port']
        output = return_zone()
        self.assertTrue(f'{name} {ip} {port}' in output)
