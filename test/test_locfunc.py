#!/usr/bin/env python

# The main purpose of these tests is watching
# the general behavior of the cityctry function.
# Not every case needs to be tested, but at least
# a few cases should be checked. Also, at the time
# of this writing, there was a bug in the location
# handling code, so hitting these unit tests helps
# ensure that the bug wasn't part of that problem.


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

    def test_us(self):
        city = cityctry("St Claire", "US")
        print city
        assert("SAINT CLAIRE" == city)


if __name__ == '__main__':
    unittest.main()
