#!/usr/bin/env python

# `fwork.py` will probably be renamed to something a little
# more suggestive as to its purpose.

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

#import imp
#from yaml import load, dump

from  fwork import *

class TestFWork(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_dummy(self):
        assert(1 == 1)

    def test_int(self):
        assert('1' == ascit('1'))

    def test_float(self):
        # Default strict=True removes periods.
        result = ascit('1.0', strict=False)
        assert('1.0' == result)

    def test_remove_period(self):
        assert('10' == ascit('1.0', strict=True))


if __name__ == '__main__':
    unittest.main()
