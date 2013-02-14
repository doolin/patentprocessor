#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

from make_test_databases import *
from geocode_setup import *


class TestGeocodeSetup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        remove_existing_databases()
        self.conn = get_connection("hashTbl.sqlite3")
        self.c = get_cursor(self.conn)
        create_sql_helper_functions(self.conn)
        geocode_db_initialize(self.c)
        loc_create_table(self.c)

    def setUp(self):
        pass

    def test_fix_city_country(self):
        make_assignee_db()
        fix_city_country(self.c)
        # Inspect loc table in hashTbl, find something
        # to assert.
        assert('FOO' == 'FOO')

    def test_fix_state_zip(self):
        make_inventor_db()
        fix_state_zip(self.c)
        # Inspect loc table in hashTbl, find something
        # to assert.
        assert('FOO' == 'FOO')

    def test_create_usloc_table(self):
        create_loc_indexes(self.conn)
        create_usloc_table(self.c)
        # Inpect the usloc table, find some assertion to make.
        assert('FOO' == 'FOO')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == '__main__':
    unittest.main()
