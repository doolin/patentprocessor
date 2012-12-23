#!/usr/bin/env python

import unittest
import sys
import imp
import os
import datetime
import re
import logging
import copy
from xml.dom.minidom import parse, parseString
from optparse import OptionParser
from sql_patent import SQLPatent
from types import *

sys.path.append('../lib')
from patXML import *


# Data structures/variables used in testing
xmlclasses = [AssigneeXML, CitationXML, ClassXML, InventorXML, \
              PatentXML, PatdescXML, LawyerXML, ScirefXML, UsreldocXML]
debug = False
xml_files = []
parsed_xml = []
max_years = "2012"
max_months = "12"
max_days = "31"
first_patent = "17900731"

dir = os.path.dirname(__file__)
folder = os.path.join(dir, 'unittest/')

# create unittest/log/sql-test-log.log if not exists/readable
if not os.access('unittest/log', os.F_OK):
    os.mkdir('unittest/log')
if not os.access('unittest/log/sql-test-log.log', os.F_OK+os.R_OK):
    os.open('unittest/log/sql-test-log.log', os.O_CREAT)
log_file = os.path.join(dir, 'unittest/log/sql-test-log.log')
xml_files = [x for x in os.listdir(folder)
             if re.match(r".*?patent.*?xml", x) != None]

# Parsing XML to be used in SQLPatent()

for xml in xml_files:
    for xmlclass in xmlclasses:
        parsed_xml.append(xmlclass(open(folder + xml, 'U').read()))

testSQL = SQLPatent()

# Logging setup
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# TODO:
# Update xml presence tests, make it more robust.


"""
Each individual test in unit-testing
should be able to short, independent, to the point.
"""

class TestSQLPatent(unittest.TestCase):

    def setUp(self):
        # Basic sanity check
        self.assertTrue(xml_files)

    def test_patent_XML_construction(self):
        # High-level test, testing legacy code construction,
        # Need XML To parse before it gets to SQLPatent
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
            for xmlclass in xmlclasses:
                try:
                    xml_patent = xmlclass(file_to_open.read())
                    parsed_xml.append(xml_patent)
                except Exception as exPatError:
                    logging.error("Construction Error at patent %d, filename %s"
                                 % (i+1, xml))

    def test_patent_SQL_tblBuild_asg2(self):
        assignees = filter(lambda x: isinstance(x, AssigneeXML), parsed_xml)
        new_table = testSQL.tblBuild(assignees, "assignee")
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
        citations = filter(lambda x: isinstance(x, CitationXML), parsed_xml)
        new_table = testSQL.tblBuild(citations, "citation")
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
        classes = filter(lambda x: isinstance(x, ClassXML), parsed_xml)
        new_table = testSQL.tblBuild(classes, "class")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                class_list = xml.classes[i]
                self.assertTrue(len(table_entry) == 4 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == (i==0)*1)
                self.assertTrue(table_entry[2] == class_list[0])
                self.assertTrue(table_entry[3] == class_list[1])

    def test_patent_SQL_tblBuild_inv(self):
        inventors = filter(lambda x: isinstance(x, InventorXML), parsed_xml)
        new_table = testSQL.tblBuild(inventors, "inventor")
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
        patents = filter(lambda x: isinstance(x, PatentXML), parsed_xml)
        new_table = testSQL.tblBuild(patents, "patent")
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

    def test_patent_SQL_tblBuild_patdesc(self):
        patdescs = filter(lambda x: isinstance(x, PatdescXML), parsed_xml)
        new_table = testSQL.tblBuild(patdescs, "patdesc")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                self.assertTrue(len(table_entry) == 3 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == xml.abstract)
                self.assertTrue(table_entry[2] == xml.invention_title)

    def test_patent_SQL_tblBuild_lawyer(self):
        lawyers = filter(lambda x: isinstance(x, LawyerXML), parsed_xml)
        new_table = testSQL.tblBuild(lawyers, "lawyer")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                law_list = xml.law_list[i]
                self.assertTrue(len(table_entry) == 6 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == law_list[1])
                self.assertTrue(table_entry[2] == law_list[0])
                self.assertTrue(table_entry[3] == law_list[2])
                self.assertTrue(table_entry[4] == law_list[3])

    def test_patent_SQL_tblBuild_sciref(self):
        scirefs = filter(lambda x: isinstance(x, ScirefXML), parsed_xml)
        new_table = testSQL.tblBuild(scirefs, "sciref")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                cit_list = [y for y in xml.cit_list if y[1]==""][i]
                self.assertTrue(len(table_entry) == 3 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == cit_list[-1])

    def test_patent_SQL_tblBuild_usreldoc(self):
        usreldocs = filter(lambda x: isinstance(x, UsreldocXML), parsed_xml)
        new_table = testSQL.tblBuild(usreldocs, "usreldoc")
        for i, table_entry in enumerate(new_table):
            for xml in parsed_xml:
                rel_list = [y for y in xml.rel_list if y[1]==""][i]
                self.assertTrue(len(table_entry) == 7 or not table_entry)
                self.assertTrue(table_entry[0] == xml.patent)
                self.assertTrue(table_entry[1] == rel_list[0])
                self.assertTrue(table_entry[2] == rel_list[1])
                self.assertTrue(table_entry[3] == rel_list[3])
                self.assertTrue(table_entry[4] == rel_list[2])
                self.assertTrue(table_entry[5] == rel_list[4])
                if rel_list[1] == 1:
                    self.assertTrue(table_entry[6] == rel_list[5])
                    self.assertTrue(table_entry[7] == rel_list[6])
                else:
                    self.assertTrue(not table_entry[6])
                    self.assertTrue(not table_entry[7])

    def test_patent_SQL_tblBuild_null(self):
        new_table = testSQL.tblBuild(parsed_xml, "nullcheck")
        for i, table_entry in enumerate(new_table):
            self.assertTrue(not table_entry)
            
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
