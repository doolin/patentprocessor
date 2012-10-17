#!/usr/bin/env python

# `locfunc.py` will probably be renamed to something a little
# more suggestive as to its purpose.

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

#import imp
#from yaml import load, dump

from locFunc import *

class TestLocFunc(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_dummy(self):
        assert(1 == 1)


if __name__ == '__main__':
    unittest.main()
