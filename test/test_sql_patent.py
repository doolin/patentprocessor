import unittest
import sys
import imp
import os
import datetime
import re
import logging
import copy
from xml.dom.minidom import parse, parseString
from xml_patent import XMLPatent
from optparse import OptionParser
from sql_patent import SQLPatent
from types import *


# Data structures/variables used in testing
tables = ["assignee", "citation", "class", "inventor",
          "patent", "patdesc", "lawyer", "sciref", "usreldoc"]
debug = False
xml_files = []
parsed_xml = []
max_years = "2012"
max_months = "12"
max_days = "31"
first_patent = "17900731"

dir = os.path.dirname(__file__)
folder = os.path.join(dir, 'unittest/')
log_file = os.path.join(dir, 'unittest/log/unit-test-log.log')
xml_files = [x for x in os.listdir(folder)
             if re.match(r".*?patent.*?xml", x) != None]

# Logging setup
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# TODO:
# Update xml presence tests, make it more robust.


"""
Each individual test in unit-testing should be able to run individually. 
"""

class TestXMLPatent(unittest.TestCase):

    def setUp(self):
        # Basic sanity check
        self.assertTrue(xml_files)

    def test_patent_XML_construction(self):
        # High-level test, testing legacy code construction,
        # if doesn't construct obviously won't pass other tests, fail-fast mentality
        if debug:
            print "\n     Testing Well-formedness and Construction\n"
        logging.info("Testing Construction of %d Patents!" % (len(xml_files)))
        patent_count = 0
        for i, xml in enumerate(xml_files):
            if debug:
                print " - Testing Patent: %s" % (xml)
            try:
                file_to_open = open(folder + xml, 'U')
            except Exception as fileError:
                logging.error("Error opening patent %d, filename: %s" 
                             % (i+1, xml))
            try:
                xml_patent = XMLPatent(file_to_open)
            except Exception as exPatError:
                logging.error("Construction Error at patent %d, filename %s" 
                             % (i+1, xml))
            # Storing tuple (original XML file, parsed XML) for finer block testing
            parsed_xml.append(xml_patent)

    def test_patent_SQL_tblBuild_asg(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "assignee")
        # print "new table is...", new_table, len(new_table)
        for table_entry in new_table:
            for xml in parsed_xml:
                asg_list = xml.asg_list[0]
                self.assertTrue(len(table_entry) == 9 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == asg_list[2])  
                self.assertTrue(table_entry[2] == asg_list[1]) 
                self.assertTrue(table_entry[3] == asg_list[4]) 
                self.assertTrue(table_entry[4] == asg_list[5])
                self.assertTrue(table_entry[5] == asg_list[6])
                self.assertTrue(table_entry[6] == asg_list[7])
                self.assertTrue(table_entry[7] == asg_list[8])

    def test_patent_SQL_tblBuild_asg2(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "assignee")
        # print "new table is...", new_table, len(new_table)
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                asg_list = xml.asg_list[i]
                self.assertTrue(len(table_entry) == 9 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == asg_list[2])  
                self.assertTrue(table_entry[2] == asg_list[1]) 
                self.assertTrue(table_entry[3] == asg_list[4]) 
                self.assertTrue(table_entry[4] == asg_list[5])
                self.assertTrue(table_entry[5] == asg_list[6])
                self.assertTrue(table_entry[6] == asg_list[7])
                self.assertTrue(table_entry[7] == asg_list[8])

    def test_patent_SQL_tblBuild_cit(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "citation")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                cit_list = xml.cit_list[i]
                self.assertTrue(len(table_entry) == 8 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                # print "table entry[2]:", table_entry[2]
                # print "cit_list[5]", cit_list[5]
                self.assertTrue(table_entry[2] == cit_list[5]) 
                self.assertTrue(table_entry[3] == cit_list[4]) 
                self.assertTrue(table_entry[4] == cit_list[1])
                self.assertTrue(table_entry[5] == cit_list[2])
                self.assertTrue(table_entry[6] == cit_list[0])

    def test_patent_SQL_tblBuild_class(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "class")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                class_list = xml.classes[i]
                self.assertTrue(len(table_entry) == 4 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == (i==0)*1)
                self.assertTrue(table_entry[2] == class_list[0])
                self.assertTrue(table_entry[3] == class_list[1])

    def test_patent_SQL_tblBuild_inv(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "inventor")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                inv_list = xml.inv_list[i]
                self.assertTrue(len(table_entry) == 10 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == inv_list[1])
                self.assertTrue(table_entry[2] == inv_list[0])
                self.assertTrue(table_entry[3] == inv_list[2])
                self.assertTrue(table_entry[4] == inv_list[3])
                self.assertTrue(table_entry[5] == inv_list[4])
                self.assertTrue(table_entry[6] == inv_list[5])
                self.assertTrue(table_entry[7] == inv_list[6])
                self.assertTrue(table_entry[8] == inv_list[8])

    def test_patent_SQL_tblBuild_pat(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "patent")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                self.assertTrue(len(table_entry) == 10 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == xml.kind)
                self.assertTrue(table_entry[2] == xml.clm_num)
                self.assertTrue(table_entry[3] == xml.code_app)
                self.assertTrue(table_entry[4] == xml.patent_app)
                self.assertTrue(table_entry[5] == xml.date_grant)
                self.assertTrue(table_entry[6] == xml.date_grant[:4])
                self.assertTrue(table_entry[7] == xml.date_app)
                self.assertTrue(table_entry[8] == xml.date_app[:4])
                self.assertTrue(table_entry[9] == xml.pat_type)

            
            
        
        
        
        

    def tearDown(self):
        #anything needed to be torn down should be added here, pass for now
        pass

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d", "--debugging", dest="debugging", action="store_true")
    (options, args) = parser.parse_args()

    """
        Complications passing in command-line arguments along with unit-testing,
        Need to delete sys.argv from index one onewards or else flag keeps getting
        interpreted, solution found
        http://stackoverflow.com/questions/1029891/python-unittest-is-there-a-way-to-pass-command-line-options-to-the-app
    """

    if options.debugging:
        debug = True
    del sys.argv[1:]
    if debug:
        print "\n     Starting Unit Testing for XMLPatent()"
    open(log_file, 'w')
    unittest.main()
