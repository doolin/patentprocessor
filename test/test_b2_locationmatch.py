#!/usr/bin/env python

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )


import B2_LocationMatch

class TestLocFunc(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'


if __name__ == '__main__':
    unittest.main()
