#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys
import logging
import unittest
import csv

sys.path.append( '.' )
sys.path.append( '../lib/' )
from generator import *

"""
TODO: Add documentation as needed.
"""


class TestGenerator(unittest.TestCase):

    def setUp(self):
        # print "setup"
        pass 

    def test_process_csv(self):
        file_name = open("gen_sample.csv", "rb")
        csv_reader = process_csv(file_name)
        for i, row in enumerate(csv_reader):
            assert([str(i),"foo", "bar", "01234567"] == row)
    def test_build_query_string(self):
        test_first_name = "FOO"
        test_last_name = "BAR"
        test_patent_number = "D1234567"
        test_result = """SELECT * FROM invpat WHERE 
                        (Firstname = \"%s\" and Lastname = \"%s\"
                         and Patent = \"%s\");""" % (test_first_name, test_last_name, test_patent_number)
        assert(test_result == build_query_string(test_first_name, test_last_name, test_patent_number))
                          

if __name__ == '__main__':
    unittest.main()
