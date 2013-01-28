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
testfile = XMLPatentBase(open(testdir+'ipg120327.one.xml').read())
attrs = ['country', 'patent', 'kind', 'date_grant', 'pat_type', \
         'date_app', 'country_app', 'patent_app', 'code_app', \
         'clm_num', 'classes', 'abstract', 'invention_title', \
         'asg_list', 'cit_list', 'rel_list', \
         'inv_list', 'law_list']

couch = couchdb.Server()
db = None
if 'patents' in couch:
    db = couch['patents']
else:
    db = couch.create('patents')
patentroot = '.'
xmlregex = r'ipg120327.one.xml'
filelist = parse.list_files([testdir], patentroot, xmlregex)
grant_list = parse.parallel_parse(filelist)
parsed_grants = parse.parse_patent(grant_list)

def get_metadata(patent):
    """
    Return metadata dictionary of the patent
    """
    metadata = {}
    metadata['publication_id'] = patent.patent
    metadata['application_id'] = patent.patent_app
    metadata['xml'] = patent.orig_xmlstring
    metadata['attributes'] = {}
    for attr in attrs:
        metadata['attributes'][attr] = patent.__getattribute__(attr)
    return metadata

def add_doc(metadata):
    """
    Adds metadata to couch database
    """
    doc_id, doc_rev = db.save(metadata)
    return doc_id

def query(tag, value):
    """
    Composes a javascript query to be run on the database
    """
    mapfun = """function(doc) {{
                  if(doc.{0} == "{1}")
                    emit(doc, doc.{0})
                }}""".format(tag,value)
    res = db.query(mapfun).rows
    return res[0].key['xml'] if res else None

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
