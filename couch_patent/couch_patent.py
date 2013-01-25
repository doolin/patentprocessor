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
attrs = ['country', 'patent', 'kind', 'date_grant', 'pat_type', \
         'date_app', 'country_app', 'patent_app', 'code_app', \
         'clm_num', 'classes', 'abstract', 'invention_title', \
         'asg_list', 'cit_list', 'rel_list', \
         'inv_list', 'law_list']


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


    def test_get_doc_metadata(self):
        """
        Tests that get_metadata retrieves the requisite information from a
        parsed xml file
        """
        patentroot = '.'
        xmlregex = r'ipg120327.one.xml'
        filelist = parse.list_files([testdir], patentroot, xmlregex)
        grant_list = parse.parallel_parse(filelist)
        parsed_grants = parse.parse_patent(grant_list)
        self.assertTrue(len(parsed_grants) == 9)
        metadata = get_metadata(parsed_grants[0])
        self.assertTrue(isinstance(metadata, dict))
        self.assertTrue(metadata['xml'] == \
                        open(testdir+'ipg120327.one.xml').read())
        for attr in self.attrs:
            self.assertTrue(metadata['attributes'][attr] == \
                            parsed_grants[0].__getattr__(attr))

unittest.main()
