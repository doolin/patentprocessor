#!/usr/bin/env python

import sys
import couchdb
import unittest

sys.path.append('../lib')
from patXML import *

class TestCouchPatent(unittest.TestCase):

    def setUp(self):
        self.couch = couchdb.Server()
        self.db = None
        if not 'patents' in self.couch:
            self.db = self.couch['patents']
        else:
            self.db = self.couch.create('patents')
        self.assertTrue('patents' in self.couch)

