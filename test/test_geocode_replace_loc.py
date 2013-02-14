#!/usr/bin/env python

import sys
import sqlite3
import unittest

sys.path.append( '.' )
sys.path.append( '../lib/' )

from make_test_databases import *
from geocode_setup import create_hashtbl
from geocode_setup import create_sql_helper_functions


class TestGeocode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        remove_existing_databases()
        make_assignee_db()
        make_inventor_db()
        self.conn = sqlite3.connect("hashTbl.sqlite3")
        cursor = self.conn.cursor()
        create_sql_helper_functions(self.conn)
        create_hashtbl(cursor, self.conn)

    def test_domestic_sql(self):
        pass


if __name__ == '__main__':
    unittest.main()
