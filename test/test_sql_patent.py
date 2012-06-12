import unittest
import sys
import imp
import os
import datetime
import re
import logging
from xml.dom.minidom import parse, parseString
from xml_patent import XMLPatent
from optparse import OptionParser
from sql_patent import SQLPatent
from types import *
import copy


# Details of xml fixtures can be found on googlegroups

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
 Fields useful for legacy code testing: self.country, self.patent, self.kind,
 self.date_grant, self.pat_type, self.date_app, self.country_app,
 self.patent_app (each patent should have these)

 self.code_app, self.clm_num, self.classes <-- can't easily test these,
 vary differently across all general patents, still thinking of a solution
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
            
        logging.info("%d Patents have passed construction!", patent_count)
        if patent_count is len(xml_files):
            logging.info("All patents passed construction!")

    def test_patent_SQL_tblBuild_asg(self):
        parsed_xml = []
        for xml in xml_files:
            parsed_xml.append(XMLPatent(open(folder + xml, 'U')))
        list_of_tables = []
        testSQL = SQLPatent()
        new_table = testSQL.tblBuild(parsed_xml, "assignee")
        print "new table is...", new_table

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
