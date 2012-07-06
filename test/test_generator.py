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
        print "setup"

    def test_process_csv(self):
        file_name = open("gen_sample.csv", "rb")
        csv_reader = process_csv(file_name)
        for i, row in enumerate(csv_reader):
            assert([str(i),"foo", "bar", "01234567"] == row)

if __name__ == '__main__':
    unittest.main()
