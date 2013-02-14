#!/usr/bin/env python

import sys
import sqlite3
import unittest

sys.path.append( '.' )
sys.path.append( '../lib/' )

from make_test_databases import *
from geocode_setup import create_hashtbl
from geocode_setup import create_sql_helper_functions
from geocode_replace_loc import *

class TestGeocodeReplaceLoc(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        remove_existing_databases()
        make_assignee_db()
        make_inventor_db()
        self.conn = sqlite3.connect("hashTbl.sqlite3")
        self.cursor = self.conn.cursor()
        create_sql_helper_functions(self.conn)
        create_hashtbl(self.cursor, self.conn)

    def test_domestic_sql(self):
        query = domestic_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        #print rows
        query = domestic_sql() % (0, 0)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        #print rows
        pass

    def test_domestic_block_remove_sql(self):
        query = domestic_block_remove_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_domestic_first3_jaro_winkler_sql(self):
        query = domestic_first3_jaro_winkler_sql() % (-1, -1, "10.92", -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_domestic_last4_jaro_winkler_sql(self):
        query = domestic_last4_jaro_winkler_sql() % (-1, -1, "10.90", -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_full_name_1_sql(self):
        query = foreign_full_name_1_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_full_name_2_sql(self):
        query = foreign_full_name_2_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_short_form_sql(self):
        query = foreign_short_form_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_block_split_sql(self):
        query = foreign_block_split_sql() % (-1, -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_first3_jaro_winkler_sql(self):
        query = foreign_first3_jaro_winkler_sql() % (-1, -1, "20.92", -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_last4_jaro_winkler_sql(self):
        query = foreign_last4_jaro_winkler_sql() % (-1, -1, "20.90", -1)
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_domestic_2nd_layer_sql(self):
        query = domestic_2nd_layer_sql()
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_domestic_first3_2nd_jaro_winkler_sql(self):
        query = domestic_first3_2nd_jaro_winkler_sql() % "14.95"
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_full_name_2nd_layer_sql(self):
        query = foreign_full_name_2nd_layer_sql()
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_full_nd_2nd_layer_sql(self):
        query = foreign_full_nd_2nd_layer_sql()
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_no_space_2nd_layer_sql(self):
        query = foreign_no_space_2nd_layer_sql()
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_foreign_first3_2nd_jaro_winkler_sql(self):
        query = foreign_first3_2nd_jaro_winkler_sql() % "24.95"
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass

    def test_domestic_zipcode_sql(self):
        query = domestic_zipcode_sql()
        result = self.cursor.execute(query)
        rows = result.fetchall()
        pass


if __name__ == '__main__':
    unittest.main()
