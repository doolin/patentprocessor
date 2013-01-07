#!/usr/bin/env python

import os
import re
import unittest
from xml_driver import XMLElement, XMLHandler
from xml.sax import make_parser, handler

# Directory of test files
xml_files = [x for x in os.listdir('test_xml_files')
             if re.match(r"2012_\d.xml", x) != None] # Match fixtures

parsed_xml = []
for xf in xml_files:
    parser = make_parser()
    xmlhandler = XMLHandler()
    parser.setContentHandler(xmlhandler)
    parser.setFeature(handler.feature_external_ges, False)
    parser.parse('test_xml_files/'+xf)
    parsed_xml.append(xmlhandler.root)

class Test_XMLElement(unittest.TestCase):
    
    def setUp(self):
        # sanity check
        self.assertTrue(xml_files)

    def test_basic_xml_tag_counts(self):
        xmlhandler = XMLHandler()
        parser.setContentHandler(xmlhandler)
        parser.setFeature(handler.feature_external_ges, False)
        parser.parse('test_xml_files/basic.xml')
        self.assertTrue(xmlhandler.root)
        root = xmlhandler.root
        self.assertTrue(len(root.a.b) == 2)


unittest.main()
