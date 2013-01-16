#!/usr/bin/env python

import os
import sys
import unittest
import logging

sys.path.append('..')
sys.path.append('../lib')
import parse
from patXML import *

basedir = os.path.dirname(__file__)
testdir = os.path.join(basedir, './fixtures/xml/')
testfileone = 'ipg120327.one.xml'
testfiletwo = 'ipg120327.two.xml'
regex = re.compile(r"""
 ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
.*?
[<][/]us[-]patent[-]grant[>])    #and here is the end tag
""", re.I+re.S+re.X)
xmlclasses = [AssigneeXML, CitationXML, ClassXML, InventorXML, \
              PatentXML, PatdescXML, LawyerXML, ScirefXML, UsreldocXML]

class TestParseFile(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_parse_file_one(self):
        parsed_output = parse.parse_file(testdir+testfileone)
        self.assertTrue(isinstance(parsed_output, list))
        self.assertTrue(len(parsed_output) == 1)
        self.assertTrue(isinstance(parsed_output[0], str))
        self.assertTrue(regex.match(parsed_output[0]))

    def test_parallel_parse_one(self):
        filelist = [testdir+testfileone]
        parsed_output = parse.parallel_parse(filelist)
        self.assertTrue(isinstance(parsed_output,list))
        self.assertTrue(len(parsed_output) == 1)
        self.assertTrue(isinstance(parsed_output[0],list))
        self.assertTrue(len(parsed_output[0]) == 1)
        self.assertTrue(isinstance(parsed_output[0][0], str))
        self.assertTrue(regex.match(parsed_output[0]))

    def test_parse_file_two(self):
        parsed_output = parse.parse_file(testdir+testfiletwo)
        self.assertTrue(isinstance(parsed_output, list))
        self.assertTrue(len(parsed_output) == 2)
        self.assertTrue(isinstance(parsed_output[0], str))
        self.assertTrue(isinstance(parsed_output[1], str))
        self.assertTrue(regex.match(parsed_output[0]))
        self.assertTrue(regex.match(parsed_output[1]))

    def test_parallel_parse_two(self):
        filelist = [testdir+testfiletwo]
        parsed_output = parse.parallel_parse(filelist)
        self.assertTrue(isinstance(parsed_output,list))
        self.assertTrue(len(parsed_output) == 1)
        self.assertTrue(isinstance(parsed_output[0],list))
        self.assertTrue(len(parsed_output[0]) == 2)
        self.assertTrue(isinstance(parsed_output[0][0], str))
        self.assertTrue(isinstance(parsed_output[0][1], str))
        self.assertTrue(regex.match(parsed_output[0]))
        self.assertTrue(regex.match(parsed_output[1]))
    
    def test_use_parallel_parse_one(self):
        filelist = [testdir+testfileone]
        parsed_output = parse.parallel_parse(filelist)
        parsed_xml = [xmlclass(parsed_output[0][0]) for xmlclass in xmlclasses]
        self.assertTrue(len(parsed_xml) == len(xmlclasses))
        self.assertTrue(all(parsed_xml))

    def test_use_parallel_parse_two(self):
        filelist = [testdir+testfiletwo]
        parsed_output = parse.parallel_parse(filelist)
        parsed_xml = []
        for us_patent_grant in parsed_output[0]:
            self.assertTrue(isinstance(us_patent_grant, str))
            for xmlclass in xmlclasses:
                parsed_xml.append(xmlclass(us_patent_grant))
        self.assertTrue(len(parsed_xml) == 2 * len(xmlclasses))
        self.assertTrue(all(parsed_xml))
    
    def test_list_files(self):
        patentroot = '.'
        testdir = [os.path.join(basedir, './fixtures/unittest/fixtures')]
        xmlregex = r'2012_\d.xml'
        files = parse.list_files(testdir, patentroot, xmlregex)
        self.assertTrue(isinstance(files, list))
        self.assertTrue(len(files) == 9)
        self.assertTrue(all(filter(lambda x: isinstance(x, str), files)))
        self.assertTrue(all(map(lambda x: os.path.exists(x), files)))

        


if __name__ == '__main__':
    unittest.main()
