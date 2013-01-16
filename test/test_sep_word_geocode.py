#!/usr/bin/env python


import unittest
import sys

sys.path.append( '.' )
sys.path.append( '../lib/' )

from sep_wrd_geocode import sep_wrd

class TestSepWrd(unittest.TestCase):

    def test_sep_wrd_comma(self):
        assert("foo" == sep_wrd("foo,bar", 0))
        assert("bar" == sep_wrd("foo,bar", 1))

    def test_sep_wrd_pipe(self):
        assert("foo" == sep_wrd("foo|bar", 0))
        assert("bar" == sep_wrd("foo|bar", 1))

    def test_nosplit(self):
        result = sep_wrd("foo bar", 0)
        assert("foo bar" == result)
        result = sep_wrd("foo bar", 1)
        assert("" == result)
        # Check out of bounds index, really ought to fail
        assert("" == sep_wrd("foo bar", 2))

    def test_seq_neg1(self):
        assert("foo bar" == sep_wrd("foo bar", -1))


if __name__ == '__main__':
    unittest.main()
