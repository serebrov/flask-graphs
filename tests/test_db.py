import unittest
import time

import os
import sys
PATH=os.path.dirname(os.path.realpath(__file__))
sys.path.append(PATH + '/..')

import database
import application


class DBTest(unittest.TestCase):

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
        self.start = self.end = None
        self.search_fn = (
            lambda item:
                (not self.start or (self.start and item['ts'] >= self.start)) and
                (not self.end or (self.end and item['ts'] <= self.end))
        )

    def tearDown(self):
        pass

    def test_find_all(self):
        self.start = self.end = None
        result = database.find_if(self.search_fn)
        self.assertEquals(self.expected_data, result)

    def test_find_by_end(self):
        self.start = None
        self.end = 150
        result = database.find_if(self.search_fn)
        self.assertEquals({'Nick|100': self.player1}, result)

    def test_find_by_start(self):
        self.start = 150
        self.end = None
        result = database.find_if(self.search_fn)
        self.assertEquals({'Ken|200': self.player2}, result)

    def test_query(self):
        result = database.query(player='Nick')
        self.assertEquals({'Nick|100': self.player1}, result)


if __name__ == "__main__":
    unittest.main()
