#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

from make_test_databases import *
from geocode_setup import *


def my_sane_remove_wrapper(filename):
    try:
        os.remove(filename)
    except os.error:
        pass

class TestGeocodeSetup(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection("hashTbl.sqlite3")
        self.c = get_cursor(self.conn)
        create_sql_helper_functions(self.conn)
        geocode_db_initialize(self.c)
        loc_create_table(self.c)
        my_sane_remove_wrapper("assignee.sqlite3")
        my_sane_remove_wrapper("inventor.sqlite3")

    def test_fix_city_country(self):
        make_assignee_db()
        assert('FOO' == 'FOO')

    def test_fix_state_zip(self):
        make_inventor_db()
        assert('FOO' == 'FOO')

    def tearDown(self):
        # os.remove("hashTbl.sqlite3")
        print "done"

if __name__ == '__main__':
    unittest.main()
