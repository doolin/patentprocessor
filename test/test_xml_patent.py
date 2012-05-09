#!/usr/bin/env python

import unittest
import imp
from yaml import load, dump

from  xml_patent import XMLPatent

#imp.load_source("xml_patent", ".")

xmlfile = open('xml/ipg120327.one.xml')

class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_dummy(self):
        assert(1 == 1)

    def test_patent(self):
        attlist = XMLPatent(xmlfile.read())
        #print attlist
        # Assert against whatever python uses for array or list
        # element presence.
        assert(attlist)


if __name__ == '__main__':
    unittest.main()
