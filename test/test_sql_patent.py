#!/usr/bin/env python

import unittest
import imp
from yaml import load, dump

from  sql_patent import SQLPatent

class TestSQLPatent(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_dummy(self):
        assert(1 == 1)

    def test_sql_patent(self):
        sqlpatent = SQLPatent()
        assert(sqlpatent)



if __name__ == '__main__':
    unittest.main()
