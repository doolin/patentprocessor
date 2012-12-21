#!/usr/bin/env python

# `fwork.py` will probably be renamed to something a little
# more suggestive as to its purpose.

import unittest
import sys
import sqlite3

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
    def setUpClass(self):
        #print "Setting up TestCase"
        self.conn = sqlite3.connect("./fixtures/sqlite3/combined.sqlite3")
        self.c = self.conn.cursor() 

    def setUp(self):
        #print "Setting up..."
        self.foo = 'bar'

    def test_compute_orig(self):
            orig = compute_orig(self.c)
	    assert(1442 == orig)

    def test_compute_errm(self):
        errm = compute_errm(self.c)
        assert(60 == errm)

#    def test_compute_u(self):
#        print "Testing compute_u"

#    def test_compute_o(self):
#        print "Testing compute_o"

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
        foo = 1
        #print "Done with testing."

    @classmethod
    def tearDownClass(self):
        #print "\nTearing down TestCase."
        self.c.close()

if __name__ == '__main__':
    unittest.main()
