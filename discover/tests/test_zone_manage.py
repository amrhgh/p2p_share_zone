from unittest import TestCase

from discover.zone_manager import return_zone, zone_path, update_zone, get_nodes_name, zone_list_to_dict
from conf.conf_reader import config


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

    def test_get_names_from_zone_list(self):
        zone_list = [
            'NS3 172.28.1.3 8888',
            'NS4 172.28.1.4 8888',
            'NS1 172.28.1.1 8888'
        ]
        names = get_nodes_name(zone_list)
        self.assertEqual(['NS3', 'NS4', 'NS1'], names)


    def test_zone_list_to_dict(self):
        zone_list = [
            'NS3 172.28.1.3 8888',
            'NS4 172.28.1.4 8888',
            'NS1 172.28.1.1 8888'
        ]
        zone_dic = {
            'NS3': {
                'ip': '172.28.1.3',
                'port': '8888'
            },
            'NS4': {
                'ip': '172.28.1.4',
                'port': '8888'
            },
            'NS1': {
                'ip': '172.28.1.1',
                'port': '8888'
            }
        }
        result = zone_list_to_dict(zone_list)
        self.assertEqual(result, zone_dic)