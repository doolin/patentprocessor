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


if __name__ == '__main__':
    unittest.main()
