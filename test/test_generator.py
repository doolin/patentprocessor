#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys
import logging
import unittest

sys.path.append( '.' )
sys.path.append( '../lib/' )
from generator import *

"""
TODO: Add documentation as needed.
"""


class TestGenerator(unittest.TestCase):

    def setUp(self):
        print "setup"

    def test_process_line(self):
        # TODO: Document how white space and escaped quotes get handled
        line = "1,foo,bar,01234567"
        assert(["1","foo", "bar", "01234567"] == process_line(line))

if __name__ == '__main__':
    unittest.main()
