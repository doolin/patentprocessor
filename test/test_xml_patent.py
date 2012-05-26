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

xml_file = open(('unittest/ipg120327.one.xml'), 'U') #example file

xml_files = []
parsed_xml = []

class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        xml_files.append(xml_file) # Want to append all files to test. 
        self.assertTrue(xml_files is not None) # Make sure you aren't testing nothing..
        
    def test_patent_construction(self):
        for xml in xml_files:
            parsed_xml.append((xml, XMLPatent(xml))) # Storing original XML and parsed XML for later testing
        
    

        

if __name__ == '__main__':
    unittest.main()




    
    
