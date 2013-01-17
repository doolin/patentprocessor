#!/usr/bin/env python

import os
import re
import sys
import unittest
from xml_driver import XMLElement, XMLHandler, Patent
from xml.sax import make_parser, handler
from cgi import escape as html_escape

# Directory of test files
basedir = os.curdir
testdir = os.path.join(basedir, 'fixtures/unittest/fixtures/')

class Test_XMLElement_Basic(unittest.TestCase):
    
    def setUp(self):
        # setup basic.xml parser/handler
        xmlhandler = XMLHandler()
        parser = make_parser()
        parser.setContentHandler(xmlhandler)
        parser.setFeature(handler.feature_external_ges, False)
        parser.parse(testdir+'basic.xml')
        self.assertTrue(xmlhandler.root)
        self.root = xmlhandler.root

    def test_basic_xml_tag_counts(self):
        self.assertTrue(len(self.root.a) == 1)
        self.assertTrue(len(self.root.a.b) == 2)
        self.assertTrue(len(self.root.a.b.c) == 3)
        self.assertTrue(len(self.root.a.b.d) == 2)
        self.assertTrue(len(self.root.a.c) == 3)

    def test_basic_xml_tag_contents(self):
        self.assertTrue(self.root.a.b.c[0].get_content()  == 'hello', \
            "{0} should be {1}".format(self.root.a.b.c[0].get_content(), 'hello'))
        self.assertTrue(self.root.a.b.c[1].get_content()  == 'world', \
            "{0} should be {1}".format(self.root.a.b.c[1].get_content(), 'world'))
        self.assertTrue(self.root.a.b.c[2].get_content()  == '3', \
            "{0} should be {1}".format(self.root.a.b.c[2].get_content(), '3'))
        self.assertTrue(self.root.a.b.d[0].get_content()  == '1', \
            "{0} should be {1}".format(self.root.a.b.c[0].get_content(), '1'))
        self.assertTrue(self.root.a.b.d[1].get_content()  == '2', \
            "{0} should be {1}".format(self.root.a.b.c[1].get_content(), '2'))
    
    def test_basic_xml_contents_of(self):
        self.assertTrue(self.root.a.b.contents_of('c') == ['hello','world','3'])
        self.assertTrue(self.root.a.b[0].contents_of('c') == ['hello','world'])

class Test_Patent_XMLElement(unittest.TestCase):
    def setUp(self):
        testfile = 'fixtures/xml/ipg120327.one.xml'
        self.patent = Patent(open(testfile))
        self.assertTrue(self.patent)

    def test_flatten(self):
        testlist = [ [1,4,7], [2,5,8], [3,6,9] ]
        reslist = self.patent._flatten(testlist)
        goallist = [ [1,2,3], [4,5,6], [7,8,9] ]
        self.assertTrue(reslist == goallist, \
            "{0}\nshould be\n{1}".format(reslist,goallist))

    def test_extend_padding(self):
        testlist = [ [1,2,3], [4,5], [5,6,7,8] ]
        reslist = self.patent._extend_padding(testlist,0)
        goallist = [ [1,2,3,0], [4,5,0,0], [5,6,7,8] ]
        self.assertTrue(reslist == goallist, \
            "{0}\nshould be\n{1}".format(reslist,goallist))

    def test_extend_padding_string(self):
        testlist = [ ['a','b','c'], ['d'] ]
        reslist = self.patent._extend_padding(testlist)
        goallist = [ ['a','b','c'], ['d','',''] ]
        self.assertTrue(reslist == goallist, \
            "{0}\nshould be\n{1}".format(reslist,goallist))

    def test_flatten_with_extend(self):
        testlist = [ [1,4,7], [2,5,8], [3,6] ]
        testlist = self.patent._extend_padding(testlist,0)
        reslist = self.patent._flatten(testlist)
        goallist = [ [1,2,3], [4,5,6], [7,8,0] ]
        self.assertTrue(reslist == goallist, \
            "{0}\nshould be\n{1}".format(reslist,goallist))

    def test_flatten_with_extend_multiple(self):
        testlist = [ [1,4,7], [2], [3,6] ]
        testlist = self.patent._extend_padding(testlist,0)
        reslist = self.patent._flatten(testlist)
        goallist = [ [1,2,3], [4,0,6], [7,0,0] ]
        self.assertTrue(reslist == goallist, \
            "{0}\nshould be\n{1}".format(reslist,goallist))

    def test_escape_html_nosub(self):
        teststring = "<tag1> ampersand here: & </tag1>"
        resstring = self.patent._escape_html_nosub(teststring)
        goalstring = html_escape(teststring)
        self.assertTrue(resstring == goalstring, \
            "{0}\nshould be\n{1}".format(resstring,goalstring))

    def test_escape_html_nosub(self):
        substart = "<sub>"
        subend = "</sub>"
        teststring = "<escape & skip sub tags>"
        resstring = self.patent._escape_html_nosub(substart+teststring+subend)
        goalstring = substart+html_escape(teststring)+subend
        self.assertTrue(resstring == goalstring, \
            "{0}\nshould be\n{1}".format(resstring,goalstring))

unittest.main()
