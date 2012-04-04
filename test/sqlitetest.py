#!/usr/bin/env python

import unittest
import sys
import sqlite3
sys.path.append('../')
import SQLite

# TODO: Get a database connection for testing merge

def create_connections():
    cls.conn1 = sqlite3.connect(':memory:')
    cls.conn2 = sqlite3.connect(':memory:')

def close_connections():
    conn1.close()
    conn2.close()


class TestSQLite(unittest.TestCase):

    @classmethod
    def setUp(cls):
        #print "Setting up..."
        cls.conn1 = sqlite3.connect(':memory:')
        cls.conn2 = sqlite3.connect(':memory:')
        #create_connections()

    @classmethod
    def tearDown(cls):
        #print "Tearing down..."
        cls.conn1.close()
        cls.conn2.close()
        #close_connections()

    def test_constructor_empty(self):
        s = SQLite.SQLite()
        assert(s.db == ':memory:')
        assert(s.tbl == 'main')

    def test_constructor_dbname(self):
        s = SQLite.SQLite(db='foobar.sqlite3')
        assert(s.db == 'foobar.sqlite3')
        assert(s.tbl == 'main')

    def test_constructor_dbname_tbl(self):
        s = SQLite.SQLite(db='foobar.sqlite3', tbl='tbl_foo')
        assert(s.db == 'foobar.sqlite3')
        assert(s.tbl == 'tbl_foo')

    def test_constructor_dbname_tbl_table(self):
        s = SQLite.SQLite(db='foobar.sqlite3', tbl='tbl_foo', table='table_foo')
        assert(s.db == 'foobar.sqlite3')
        assert(s.tbl == 'tbl_foo')

    def test_constructor_dbname_table(self):
        s = SQLite.SQLite(db='foobar.sqlite3', table='table_foo')
        assert(s.db == 'foobar.sqlite3')
        assert(s.tbl == 'table_foo')



    #def test_indexes(self):

if __name__ == '__main__':
    unittest.main()
