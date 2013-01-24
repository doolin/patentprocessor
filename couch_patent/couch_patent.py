#!/usr/bin/env python

import sys
import couchdb
import unittest

sys.path.append('../lib')
from patXML import *

sys.path.append('..')
import parse

basedir = os.path.join(os.curdir, '../test')
testdir = os.path.join(basedir, 'fixtures/xml/')


class TestCouchPatent(unittest.TestCase):

    def setUp(self):
        #setup CouchDB
        self.couch = couchdb.Server()
        self.db = None
        if 'patents' in self.couch:
            self.db = self.couch['patents']
        else:
            self.db = self.couch.create('patents')
        self.assertTrue('patents' in self.couch)
        #establish test xml file
        self.testfile = XMLPatentBase(open(testdir+'ipg120327.one.xml').read())
        self.assertTrue(self.testfile)
        self.attrs = ['country', 'patent', 'kind', 'date_grant', 'pat_type', \
                      'date_app', 'country_app', 'patent_app', 'code_app', \
                      'clm_num', 'classes', 'abstract', 'invention_title', \
                      'asg_list', 'cit_list', 'rel_list', \
                      'inv_list', 'law_list']


unittest.main()
