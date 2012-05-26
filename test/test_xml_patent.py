#!/usr/bin/env python

import unittest
import sys
import imp
import os
import datetime
import re
import logging
from xml.dom.minidom import parse, parseString
from xml_patent import XMLPatent

xml_file1 = open(('unittest/ipg120327.one.xml'), 'U') #example file
xml_file2 = open(('unittest/test2.xml'), 'U')
xml_file3 = open(('unittest/test3.xml'), 'U')

xml_files = []
parsed_xml = []


# Fields useful for legacy testing: self.country, self.patent, self.kind, self.date_grant
# self.pat_type, self.date_app, self.country_app, self.patent_app
# self.code_app, self.clm_num, self.classes

class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        xml_files.append(xml_file1) # Want to append all files to test.
        xml_files.append(xml_file2)
        xml_files.append(xml_file3)
        self.assertTrue(xml_files is not None) # Make sure you aren't testing nothing..
        
    def test_patent_construction(self):
        for xml in xml_files:
            xml_patent = XMLPatent(xml)
            parsed_xml.append((xml, xml_patent)) # Storing original XML and parsed XML for later testing
            print xml_patent

    def test_patent_fields(self):
        for parsed_fields in parsed_xml:
            fields = parsed_fields[1]
            self.assertTrue(fields.pat_type.isalnum()) # Testing legitimate pattern type, e.g. design, scientific, etc...
            self.assertTrue(fields.patent.isalnum()) # Testing patent , e.g. D0656296
            self.assertTrue(fields.date_grant.isdigit()) # Testing date of grant, e.g. 20123456
            self.assertTrue(fields.date_app.isdigit()) # Testing date grant applied, e.g. 20124567
            
        
    

        

if __name__ == '__main__':
    unittest.main()




    
    
