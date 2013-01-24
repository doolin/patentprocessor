#!/usr/bin/env python

import sys
import couchdb
import unittest

sys.path.append('../lib')
from patXML import *

basedir = os.path.join(os.curdir, '../test')
testdir = os.path.join(basedir, 'fixtures/xml/')


class TestCouchPatent(unittest.TestCase):

    def setUp(self):
        self.couch = couchdb.Server()
        self.db = None
        if not 'patents' in self.couch:
            self.db = self.couch['patents']
        else:
            self.db = self.couch.create('patents')
        self.assertTrue('patents' in self.couch)
        #establish test xml file
        self.testfile = XMLPatentBase(open(testdir+'ipg120327.one.xml').read())
        self.assertTrue(self.testfile)

