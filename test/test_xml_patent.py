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

# Details of xml fixtures can be found on googlegroups

# Data structures/variables used in testing
debug = False
xml_files = []
parsed_xml = []
max_years = "2012"
max_months = "12"
max_days = "31"

dir = os.path.dirname(__file__)
folder = os.path.join(dir, 'unittest/')
log_folder = os.path.join(dir, 'unittest/log/unit-test-log.log)
xml_files = [x for x in os.listdir(folder)
             if re.match(r"patent.*?xml", x) != None]

# Logging setup


# TODO:
# Update xml presence tests, make it more robust. 
# Implement logging


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

    def test_patent_construction(self):
        # High-level test, testing legacy code construction,
        # if doesn't construct obviously won't pass other tests, fail-fast mentality
        if debug:
            print "\n     Testing Well-formedness and Construction\n"
        for i, xml in enumerate(xml_files):
            xml_patent = XMLPatent(open(folder + xml, 'U'))
            # Storing tuple (original XML file, parsed XML) for later, finer block testing
            parsed_xml.append((xml, xml_patent))
            if debug:
                print " - Testing Patent: %d ..... Passed!" %(i+1)

    def test_patent_fields(self): # Medium-level test, testing fields of the parsed XML
        if debug:
            print "\n     Testing Logic and Format of Patent Fields\n"
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            self.assertTrue(parsed_fields.pat_type.isalnum() or not
                            parsed_fields.pat_type)
            self.assertTrue(parsed_fields.patent.isalnum() or not
                            parsed_fields.patent.isalnum())
            self.assertTrue(parsed_fields.country.isalnum() or not
                            parsed_fields.country)
            self.assertTrue(parsed_fields.country_app.isalnum() or not
                            parsed_fields.country_app)
            self.assertTrue(parsed_fields.kind.isalnum() or not
                            parsed_fields.kind)
            # Dates must be in following format: yyyy/mm/dd
            self.assertTrue((parsed_fields.date_grant.isdigit() and
                             len(parsed_fields.date_grant) is 8) or not parsed_fields.date_grant)
            self.assertTrue((parsed_fields.date_app.isdigit() and
                             len(parsed_fields.date_app) is 8) or not parsed_fields.date_app)
            if (parsed_fields.date_grant):
                self.assertTrue((parsed_fields.date_grant[0:4] <= max_years) and
                                (parsed_fields.date_grant[4:6] <= max_months) and
                                (parsed_fields.date_grant[6:8] <= max_days))
            if (parsed_fields.date_app):
                self.assertTrue((parsed_fields.date_app[0:4] <= max_years) and
                                (parsed_fields.date_app[4:6] <= max_months) and
                                (parsed_fields.date_app[6:8] <= max_days))
            if debug:
                print " - Testing Patent: %d ..... Passed!" %(i+1)

    def test_patent_validity(self): # Low-level test, testing presence of fields in original XML
        if debug:
            print "\n     Testing XML Presence of Patent Fields\n"
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (file of xml, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read()
            parsed_fields = xml_tuple[1]
            
            # Starting search for xml tags , <tag>field</tag>
            country_match = re.search(r"[<]document-id[>].*?[<]country[>]"+parsed_fields.country+
                                      "[<][/]country[>].*?[<][/]document-id[>]",
                                      original_xml_string, re.I + re.S + re.X)
            self.assertTrue(country_match)
            kind_match = re.search(r"[<]document-id[>].*?[<]kind[>]"+parsed_fields.kind+"[<][/]kind[>].*?[<][/]document-id[>]",
                                   original_xml_string, re.I + re.S + re.X)
            self.assertTrue(kind_match)
            
	    if parsed_fields.pat_type:
	        #app_type_match = re.search(r"[<]application-reference appl-type=\""+parsed_fields.pat_type+"\"[>]",
                #                          original_xml_string, re.I + re.S + re.X)
                app_type_match = re.search(r"appl-type=\""+parsed_fields.pat_type+"\"",
                                          original_xml_string, re.I + re.S + re.X)
	    self.assertTrue(app_type_match)

            if debug:
                print " - Testing Patent: %d ..... Passed!" %(i+1)

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

    unittest.main()
