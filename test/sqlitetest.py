#!/usr/bin/env python

import unittest
import sys
import sqlite3
sys.path.append('../')
import SQLite

# TODO: Get a database connection for testing merge

class TestSQLite(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print "Setting up..."
        #cls._connection = createExpensiveConnectionObject()
        assert(1 == 1)

    @classmethod
    def tearDown(cls):
        print "Tearing down..."
        #cls._connection.destroy()
        assert(1 == 1)

    def test_sqlite(self):
        assert(1 == 1)

    def test_constructor(self):
        s = SQLite.SQLite()
        assert(1 == 1)

    #def test_indexes(self):

if __name__ == '__main__':
    unittest.main()
