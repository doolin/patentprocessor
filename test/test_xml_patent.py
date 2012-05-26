#!/usr/bin/env python

import unittest
import sys
import imp
import os
from xml.dom.minidom import parse, parseString
from yaml import load, dump
from xml_patent import XMLPatent

dir = os.path.dirname(__file__) # Store directory of file 
test_folder = os.path.join(dir, 'xml/unittest') # Folder path with xml unit test files
log_folder = os.path.join(dir, 'xml/unittest/test-log.txt') # Folder path unit test log

open(logfile, 'w') # Erase the log and start over for each run (just a test)
logging.basicConfig(filename=logfile, level=logging.DEBUG) # Set up log in case its needed




#xml_file = open(('xml/ipg120327.one.xml'), 'U') #example file


class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        t1 = datetime.datetime.now() #set up time in case it will be used
        files = [x for x in os.listdir(test_folder) if re.match(r"unit-test.xml", x, re.I)!=None] # list collection of files to be used for unit-testing
        

    def test_dummy(self):
        assert(1 == 1)

    def test_patents(self):
        for 

        

if __name__ == '__main__':
    unittest.main()




    
    
