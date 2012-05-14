#!/usr/bin/env python

import unittest
import imp
from yaml import load, dump

from  sql_patent import SQLPatent

#imp.load_source("sql_patent", ".")

xmlfile = open('xml/ipg120327.one.xml')

class TestSQLPatent(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_dummy(self):
        assert(1 == 1)


if __name__ == '__main__':
    unittest.main()
