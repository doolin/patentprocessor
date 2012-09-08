#!/usr/bin/env python

# `fwork.py` will probably be renamed to something a little
# more suggestive as to its purpose.

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '..' )
sys.path.append( '../lib/' )

from  bmark2 import *

def removeFile(self, file):
    #delete a file if it exists
    if os.path.isfile(file):
        os.system("rm {file}".format(file=file))


class TestBMark2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
	print "Setting up TestCase..."

    def setUp(self):
        print "Setting up..."
        self.foo = 'bar'

    def test_compute_orig(self):
	    print "Testing compute_orig"

    def test_compute_errm(self):
        print "Testing compute_errm"

    def test_compute_u(self):
	print "Testing compute_u"

    def test_compute_o(self):
        print "Testing compute_o"

    def test_get_filename_suffix(self):
        filename = 'foo.bar.csv'
	assert('csv' == get_filename_suffix(filename))
        filename = 'foo.bar.sqlite3'
	assert('sqlite3' == get_filename_suffix(filename))


    def test_is_csv_file(self):
        filename = 'foo.bar.csv'
	assert(True == is_csv_file(filename))
        filename = 'foo.bar.sqlite3'
	assert(False == is_csv_file(filename))

    def tearDown(self):
        print "Done with testing."

    @classmethod
    def tearDownClass(cls):
        print "Tearing down TestCase."


if __name__ == '__main__':
    unittest.main()
