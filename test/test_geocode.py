#!/usr/bin/env python

import unittest
import sys
sys.path.append( '.' )
sys.path.append( '../lib/' )

import geocode


class TestGeocode(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'


if __name__ == '__main__':
    unittest.main()
