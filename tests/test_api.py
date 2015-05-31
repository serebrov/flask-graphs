import unittest
import simplejson as json

import os
import sys
PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(PATH + '/..')

import database
import application


class APITest(unittest.TestCase):

    def setUp(self):
        self.app = application.app.test_client()
        self.player1 = {
            'player': 'Nick', 'floor': 'Ground',
            'position': {'x': 0, 'y': 0}, 'ts': 100
        }
        self.player2 = {
            'player': 'Ken', 'floor': 'TowerTop',
            'position': {'x': 100, 'y': 50}, 'ts': 200
        }
        self.expected_data = {
            'Nick|100': self.player1,
            'Ken|200': self.player2
        }
        database.put(self.player1)
        database.put(self.player2)
        self.assertEquals(self.expected_data, database.data)

    def tearDown(self):
        pass

    def test_get_all(self):
        result = self.app.get('/data')
        result = json.loads(result.data)
        self.assertEquals(self.expected_data.values(), result['data'])

    def test_find_by_end(self):
        result = self.app.get('/data?end=150')
        result = json.loads(result.data)
        self.assertEquals([self.player1], result['data'])

    def test_find_by_start(self):
        result = self.app.get('/data?start=150')
        result = json.loads(result.data)
        self.assertEquals([self.player2], result['data'])

    def test_find_by_start_end(self):
        result = self.app.get('/data?start=150&end=250')
        result = json.loads(result.data)
        self.assertEquals([self.player2], result['data'])


if __name__ == "__main__":
    unittest.main()
