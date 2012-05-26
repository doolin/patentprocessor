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

dir = os.path.dirname(__file__) # Store directory of file 
test_folder = os.path.join(dir, 'unittest') # Folder path with xml unit test files
log_folder = os.path.join(dir, 'unittest/log/test-log.txt') # Folder path unit test log

open(log_folder, 'w') # Erase the log and start over for each run (just a test)
logging.basicConfig(filename=log_folder, level=logging.DEBUG) # Set up log in case its needed

#xml_file = open(('xml/ipg120327.one.xml'), 'U') #example file


class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        t1 = datetime.datetime.now() #set up time in case it will be used
        files = [x for x in os.listdir(test_folder) if re.match(r"unit-test.xml", x, re.I)!=None] # list collection of files to be used for unit-testing
        for file in files:
            total_count = 0
            total_patents = 0
            for filenum, filename in enumerate(files):
                print " Testing file: %s" % filename
                XMLs = re.findall(
                    r"""
                    ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
                    .*?
                    [<][/]us[-]patent[-]grant[>])    #and here is the end tag
                     """,
                    open((flder+"/"+files[filenum]), 'U').read(), re.I + re.S + re.X)
                print "   - Total Patents: %d" % (len(XMLs))

            xmllist = []
            count = 0
            patents = 0     

    def test_dummy(self):
        assert(1 == 1)
        

        

if __name__ == '__main__':
    unittest.main()




    
    
