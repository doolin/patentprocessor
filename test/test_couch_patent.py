#!/usr/bin/env python

import sys
import unittest

sys.path.append('..')
from couch_patent import *

sys.path.append('../lib/')
from patXML import *

import parse

basedir = os.path.join(os.curdir, '../test')
testdir = os.path.join(basedir, 'fixtures/xml/')
testfile = XMLPatentBase(open(testdir+'ipg120327.one.xml').read())
patentroot = '.'
xmlregex = r'ipg120327.one.xml'
filelist = parse.list_files([testdir], patentroot, xmlregex)
grant_list = parse.parallel_parse(filelist)
parsed_grants = list(parse.parse_patent(grant_list))

class TestCouchPatent(unittest.TestCase):

    def setUp(self):
        self.assertTrue(testfile)

    def test_get_doc_metadata(self):
        """
        Tests that get_metadata retrieves the requisite information from a
        parsed xml file
        """
        metadata = get_metadata(parsed_grants[0])
        self.assertTrue(isinstance(metadata, dict))
        self.assertTrue(metadata['publication_id'] == parsed_grants[0].patent)
        self.assertTrue(metadata['application_id'] == parsed_grants[0].patent_app)
        self.assertTrue(metadata['xml'] == parsed_grants[0].orig_xmlstring)
        for attr in attrs:
            self.assertTrue(metadata['attributes'][attr] == \
                            parsed_grants[0].__getattribute__(attr))

    def test_add_doc(self):
        """
        Tests adding an xml doc with all its information to the database
        """
        metadata = get_metadata(parsed_grants[0])
        doc_id = add_doc(metadata)
        stored_doc = dict(db.get(doc_id))
        self.assertTrue(stored_doc == metadata)
        db.delete(metadata)
        self.assertFalse(db.get(doc_id))

    def test_query_publication_id(self):
        metadata = get_metadata(parsed_grants[0])
        doc_id = add_doc(metadata)
        stored_doc = dict(db.get(doc_id))
        queried_doc = query('publication_id',parsed_grants[0].patent)
        self.assertTrue(queried_doc == parsed_grants[0].orig_xmlstring)

    def test_query_application_id(self):
        metadata = get_metadata(parsed_grants[0])
        doc_id = add_doc(metadata)
        stored_doc = dict(db.get(doc_id))
        queried_doc = query('application_id',parsed_grants[0].patent_app)
        self.assertTrue(queried_doc == parsed_grants[0].orig_xmlstring)

unittest.main()
