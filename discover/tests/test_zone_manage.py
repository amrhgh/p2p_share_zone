from unittest import TestCase

from db.models import Zone
from db.zone_manager import return_zone_in_string, update_zone, session


class ZoneTest(TestCase):
    def test_records_return_correctly(self):
        session().query(Zone).delete()
        session().commit()
        obj = Zone(name='NS3', ip='1.28.1.3', port=8888)
        session().add(obj)
        session().commit()
        records = return_zone_in_string()
        self.assertEqual(len(records), 2)

    def test_append_new_records_not_exist_each_of_them(self):
        session().query(Zone).delete()
        session().commit()
        new_records = ['S2 172.28.1.2 8888 1', 'S3 172.28.1.3 8888 1']
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        update_zone(new_records, ('127.0.0.1', '8888'))
        records = return_zone_in_string()
        self.assertEqual(len(records), 3)

    def test_append_new_records_some_are_exist(self):
        session().query(Zone).delete()
        session().commit()
        new_records = ['S2 172.28.1.2 8888 1', 'S3 172.28.1.3 8888 1']
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        update_zone(new_records, ('127.0.0.1', '8888'))
        new_records = ['S2 172.28.1.2 8888 1', 'S3 172.28.1.3 8888 1']
        new_records = bytes('\n'.join(new_records), encoding='UTF-8')
        update_zone(new_records, ('127.0.0.1', '8888'))
        records = return_zone_in_string()
        self.assertEqual(len(records), 3)
