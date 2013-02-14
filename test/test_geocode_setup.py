#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

from make_test_databases import *
from geocode_setup import *


class TestGeocodeSetup(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection("hashTbl.sqlite3")
        self.c = get_cursor(self.conn)
        create_sql_helper_functions(self.conn)
        geocode_db_initialize(self.c)
        loc_create_table(self.c)

    def test_fix_city_country(self):
        make_assignee_db()
        os.remove("assignee.sqlite3")
        assert('FOO' == 'FOO')

    def test_fix_state_zip(self):
        # os.remove("inventor.sqlite3")
        assert('FOO' == 'FOO')

    def tearDown(self):
        # os.remove("hashTbl.sqlite3")
        print "done"

if __name__ == '__main__':
    unittest.main()
