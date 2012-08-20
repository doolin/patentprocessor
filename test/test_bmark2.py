#!/usr/bin/env python

# `fwork.py` will probably be renamed to something a little
# more suggestive as to its purpose.

import unittest
import sys

sys.path.append( '.' )
sys.path.append( '..' )
sys.path.append( '../lib/' )

from  bmark2 import *

class TestBMark2(unittest.TestCase):

    def removeFile(self, file):
        #delete a file if it exists
        if os.path.isfile(file):
            os.system("rm {file}".format(file=file))


    def setUp(self):
        self.foo = 'bar'

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

if __name__ == '__main__':
    unittest.main()
