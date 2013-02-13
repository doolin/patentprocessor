#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import unittest
import sys
#import sqlite3

sys.path.append( '.' )
sys.path.append( '../lib/' )

from geocode_setup import *

class TestGeocodeSetup(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection("hashTbl.sqlite3")
        self.c = get_cursor(self.conn)
        create_sql_helper_functions(self.conn)
        geocode_db_initialize(self.c)
        loc_create_table(self.c)

    def test_dummy(self):
        assert('FOO' == 'FOO')

    def tearDown(self):
        # remove hastabl db
        print "done"

if __name__ == '__main__':
    unittest.main()
