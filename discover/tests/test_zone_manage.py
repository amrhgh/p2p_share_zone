from unittest import TestCase

from discover.zone_manager import return_zone, zone_path, update_zone
from pyTorrent_conf.conf_reader import config


class ZoneTest(TestCase):
    def test_return_zone_contain_it_self(self):
        name = config['General']['name']
        ip = config['General']['ip']
        port = config['Discover']['port']
        output = return_zone()
        self.assertTrue(f'{name} {ip} {port}' in output)

    def test_append_new_record_as_list_file_is_empty(self):
        new_records = ['S2 172.28.1.2 8888', 'S3 172.28.1.3 8888']
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        file = open(zone_path, 'w')
        file.close()
        update_zone(new_records)
        file = open(zone_path)
        lines = file.readlines()
        self.assertEqual(len(lines), 2)
        file.close()

    def test_append_new_record_as_list_file_is_not_empty(self):
        new_records = ['S2 172.28.1.2 8888', 'S3 172.28.1.3 8888']
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        file = open(zone_path, 'w')
        file.write('S2 172.28.1.2 8888')
        file.close()
        update_zone(new_records)
        file = open(zone_path)
        lines = file.readlines()
        self.assertEqual(len(lines), 2)
        file.close()

    def test_append_empty_record_as_list(self):
        new_records = []
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        file = open(zone_path, 'w')
        file.write('S2 172.28.1.2 8888')
        file.close()
        update_zone(new_records)
        file = open(zone_path)
        lines = file.readlines()
        self.assertEqual(len(lines), 1)
        file.close()