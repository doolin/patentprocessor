#!/usr/bin/env python

import os
import re
import sys
import unittest
from xml_driver import XMLElement, XMLHandler, Patent
from xml.sax import make_parser, handler

sys.path.append('..')
from patXML import *

# Directory of test files
xml_files = [x for x in os.listdir('test_xml_files')
             if re.match(r"2012_\d.xml", x) != None] # Match fixtures

parsed_xml_old = []
parsed_xml_new = []
for xf in xml_files:
    old = XMLPatentBase(open('test_xml_files/'+xf).read())
    parser = make_parser()
    new = XMLHandler()
    parser.setContentHandler(new)
    parser.setFeature(handler.feature_external_ges, False)
    parser.parse('test_xml_files/'+xf)

    parsed_xml_old.append(old)
    parsed_xml_new.append(new.root.us_patent_grant.us_bibliographic_data_grant)

class Test_XMLElement(unittest.TestCase):
    
    def setUp(self):
        # setup basic.xml parser/handler
        xmlhandler = XMLHandler()
        parser.setContentHandler(xmlhandler)
        parser.setFeature(handler.feature_external_ges, False)
        parser.parse('test_xml_files/basic.xml')
        self.assertTrue(xmlhandler.root)
        self.root = xmlhandler.root

    def test_basic_xml_tag_counts(self):
        self.assertTrue(len(self.root.a) == 1)
        self.assertTrue(len(self.root.a.b) == 2)
        self.assertTrue(len(self.root.a.b.c) == 3)
        self.assertTrue(len(self.root.a.b.d) == 2)

    def test_basic_xml_tag_contents(self):
        self.assertTrue(self.root.a.b.c[0].content  == 'hello', \
            "{0} should be {1}".format(self.root.a.b.c[0].content, 'hello'))
        self.assertTrue(self.root.a.b.c[1].content  == 'world', \
            "{0} should be {1}".format(self.root.a.b.c[1].content, 'world'))
        self.assertTrue(self.root.a.b.c[2].content  == '3', \
            "{0} should be {1}".format(self.root.a.b.c[2].content, '3'))
        self.assertTrue(self.root.a.b.d[0].content  == '1', \
            "{0} should be {1}".format(self.root.a.b.c[0].content, '1'))
        self.assertTrue(self.root.a.b.d[1].content  == '2', \
            "{0} should be {1}".format(self.root.a.b.c[1].content, '2'))
    
    def test_basic_xml_contents_of(self):
        self.assertTrue(self.root.a.b.contents_of('c') == ['hello','world','3'])
        self.assertTrue(self.root.a.b[0].contents_of('c') == ['hello','world'])

unittest.main()
