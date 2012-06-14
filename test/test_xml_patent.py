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
first_patent = "17900731"

# Directory of test files and logs
dir = os.path.dirname(__file__)
folder = os.path.join(dir, 'unittest/')
log_file = os.path.join(dir, 'unittest/log/unit-test.log')
xml_files = [x for x in os.listdir(folder)
             if re.match(r"patent.*?xml", x) != None]

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

    def test_patent_construction(self):
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
                patent_count = patent_count + 1
            except Exception as exPatError:
                logging.error("Construction Error at patent %d, filename %s"
                             % (i+1, xml))
            # Storing tuple (original XML file, parsed XML) for finer block testing
            parsed_xml.append((xml, xml_patent))

        logging.info("%d Patents have passed construction!", patent_count)
        if patent_count is len(xml_files):
            logging.info("All patents passed construction!")

    def test_pat_type(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            try:
                self.assertTrue(parsed_fields.pat_type.isalnum()
                                or not parsed_fields.pat_type)
            except Exception as assertionError:
                logging.error("Patent %s, pattern type: %s is not valid"
                              % (xml_tuple[0], parsed_fields.pat_type))

    def test_patent_number(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            try:
                self.assertTrue(parsed_fields.patent.isalnum()
                                or not parsed_fields.patent.isalnum())
            except Exception as assertionError:
                logging.error("Patent %s, patent doc number: %s is not valid"
                              % (xml_tuple[0], parsed_fields.patent))

    def test_country(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            try:
                self.assertTrue(parsed_fields.country.isalnum()
                                or not parsed_fields.country)
            except Exception as assertionError:
                logging.error("Patent %s, country: %s is not valid"
                              % (xml_tuple[0], parsed_fields.country))

    def test_country_app(self):
         for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            try:
                self.assertTrue(parsed_fields.country_app.isalnum()
                                or not parsed_fields.country_app)
            except Exception as assertionError:
                logging.error("Patent %s, country: %s is not valid"
                              % (xml_tuple[0], parsed_fields.country_app))

    def test_kind(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]

            try:
                self.assertTrue(parsed_fields.kind.isalnum()
                                or not parsed_fields.kind)
                field_count = field_count + 1
            except Exception as assertionError:
                logging.error("Patent %s, kind: %s is not valid"
                              % (xml_tuple[0], parsed_fields.kind))

    def test_date_grant(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
            try:
                self.assertTrue((parsed_fields.date_grant.isdigit()
                                 and len(parsed_fields.date_grant) is 8)
                                 or not parsed_fields.date_grant)
            except Exception as assertionError:
                logging.error("Patent %s, date grant: %s is not valid"
                              % (xml_tuple[0], parsed_fields.date_grant))
            if parsed_fields.date_grant:
                try:
                    self.assertTrue((parsed_fields.date_grant[0:4] <= max_years)
                                     and (parsed_fields.date_grant[4:6] <= max_months)
                                     and (parsed_fields.date_grant[6:8] <= max_days)
                                     and (parsed_fields.date_grant >= first_patent))
                except Exception as assertionError:
                    logging.error("Patent %s, date grant field: %s is not valid"
                                  % (xml_tuple[0], parsed_fields.date_grant))

    def test_date_app(self):
        for i, xml_tuple in enumerate(parsed_xml):
            parsed_fields = xml_tuple[1]
<<<<<<< HEAD

=======
>>>>>>> 8119219c192b66938459f65343e7fdbcb3cd1835
            try:
                self.assertTrue((parsed_fields.date_app.isdigit()
                                 and len(parsed_fields.date_app) is 8)
                                 or not parsed_fields.date_app)
            except Exception as assertionError:
                logging.error("Patent %s, date app: %s is not valid"
                              % (xml_tuple[0], parsed_fields.date_app))      
            if parsed_fields.date_app:
                try:
                    self.assertTrue((parsed_fields.date_app[0:4] <= max_years)
                                     and (parsed_fields.date_app[4:6] <= max_months)
                                     and (parsed_fields.date_app[6:8] <= max_days)
                                     and (parsed_fields.date_app >= first_patent))

                except Exception as assertionError:
                    logging.error("Patent %s, date app field: %s is not valid"
                                  % (xml_tuple[0], parsed_fields.date_grant))
    def test_country_xml(self):
        for i, xml_tuple in enumerate(parsed_xml):
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            country_match = re.search(r"[<]document-id[>].*?[<]country[>]"+parsed_fields.country+
                                       "[<][/]country[>].*?[<][/]document-id[>]",
                                       original_xml_string, re.I + re.S + re.X)
            try:
                self.assertTrue(country_match)
            except Exception as assertionError:
                logging.error("Patent %s, xml presence not detected of field: %s"
                               % (xml_tuple[0], parsed_fields.country))
    def test_kind_xml(self):
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (xml_file, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            kind_match = re.search(r"[<]document-id[>].*?[<]kind[>]"+parsed_fields.kind+
                                    "[<][/]kind[>].*?[<][/]document-id[>]",
                                    original_xml_string, re.I + re.S + re.X)
            try:
                self.assertTrue(country_match)
            except Exception as assertionError:
                logging.error("Patent %s, xml presence not detected of field: %s"
                               % (xml_tuple[0], parsed_fields.country))

    def test_inv_xml(self):
        for i, xml_tuple in enumerate(parsed_xml):
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            inv_title_match = re.search(r"[<][/]invention-title[>]",
                                          original_xml_string, re.I + re.S + re.X)
            if parsed_fields.invention_title: # Still needs work
                try:
                    self.assertTrue(inv_title_match)
                except Exception as assertionError:
                    logging.error("Patent %s, xml presence not detected of field: %s"
                                   % (xml_tuple[0], parsed_fields.invention_title))

    def test_pat_xml(self):
        for i, xml_tuple in enumerate(parsed_xml): 
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            pat_type_match = re.search(r"appl-type=\""+parsed_fields.pat_type+"\"",
                                         original_xml_string, re.I + re.S + re.X)
            if parsed_fields.pat_type:
                try:
                    self.assertTrue(pat_type_match)
                except Exception as assertionError:
                    logging.error("Patent %s, xml presence not detected of field: %s"
                                   % (xml_tuple[0], parsed_fields.pat_type))
            else:
                try:
                    self.assertTrue(not pat_type_match)
                except Exception as assertionError:
                    logging.error("Patent %s, xml presence detected of field: %s"
                                   % (xml_tuple[0], parsed_fields.pat_type))

    def test_asg_xml(self):
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (xml_file, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            # Now going through lists (asg, cit, rel, inv, law)

            # Asg List

            for (a1, orgname, role, address, city, state,
                 country, postcode, nationality, residence) in parsed_fields.asg_list:

                # Note: a1 in XMLPatent() is used to denote orgname from first/last-name

                if a1 is 0: # Assignees

                    org_string = "[<]assignee[>](.*?)[<]orgname[>](.*?)[<][/]orgname[>](.*?)[<][/]assignee[>]"
                    role_string = "[<]assignee[>](.*?)[<]role[>]"+role+"[<][/]role[>](.*?)[<][/]assignee[>]"
                    city_string = "[<]assignee[>](.*?)[<]city[>](.*?)[<][/]city[>](.*?)[<][/]assignee[>]"
                    state_string = "[<]assignee[>](.*?)[<]state[>]"+state+"[<][/]state[>](.*?)[<][/]assignee[>]"
                    country_string = "[<]assignee[>](.*?)[<]country[>]"+country+"[<][/]country[>](.*?)[<][/]assignee[>]"
                    postcode_string = "[<]assignee[>](.*?)[<]postcode[>]"+postcode+"[<][/]postcode[>](.*?)[<][/]assignee[>]"

                    if orgname:
                        org_match = re.search(org_string, original_xml_string,
                                              re.I + re.S + re.X)
                        try:
                            self.assertTrue(org_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, Orgname field %s exists in asg,
                                             but orgname tags do not!"""
                                             % (xml_tuple[0], orgname))
                    if role:
                        role_match = re.search(role_string, original_xml_string,
                                               re.I + re.S + re.X)
                        try:
                            self.assertTrue(role_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, role field %s exists in asg,
                                             but role tags do not!"""
                                             % (xml_tuple[0], role))
                    if city:
                        city_match = re.search(city_string, original_xml_string,
                                               re.I + re.S + re.X)
                        try:
                            self.assertTrue(city_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, city field %s exists in asg
                                             ,but city tags do not!"""
                                             % (xml_tuple[0], city))

                    if state:
                        state_match = re.search(state_string, original_xml_string,
                                                re.I + re.S + re.X)
                        try:
                            self.assertTrue(state_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, state field %s exists in asg,
                                             but state tags do not!"""
                                             % (xml_tuple[0], state))
                    if country:
                        country_match = re.search(country_string, original_xml_string,
                                                 re.I + re.S + re.X)
                        try:
                            self.assertTrue(country_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, country field %s exists in asg,
                                             but country tags do not!"""
                                             % (xml_tuple[0], country))
                    if postcode:
                        postcode_match = re.search(postcode_string, original_xml_string,
                                                  re.I + re.S + re.X)
                        try:
                            self.assertTrue(postcode_match)
                        except Exception as assertionError:
                            logging.error("""File:%s, postcode field %s exists in asg,
                                             but postcode tags do not!"""
                                             % (xml_tuple[0], postcode))

    def test_cit_xml(self):
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (xml_file, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
            # Cit List
            for (cited_by, country, doc_number,
                 date, kind, name, reference) in parsed_fields.cit_list:
                
                country_string = "[<]references-cited[>](.*?)[<]country[>]"+country+"[<][/]country[>](.*?)[<][/]references-cited[>]"
                doc_string = "[<]references-cited[>](.*?)[<]doc-number[>]"+doc_number+"[<][/]doc-number[>](.*?)[<][/]references-cited[>]"
                kind_string = "[<]references-cited[>](.*?)[<]kind[>]"+kind+"[<][/]kind[>](.*?)[<][/]references-cited[>]"
                name_string = "[<]references-cited[>](.*?)[<]name[>](.*?)[<][/]name[>](.*?)[<][/]references-cited[>]" # needs more work
                date_string = "[<]references-cited[>](.*?)[<]date[>](.*?)[<][/]date[>](.*?)[<][/]references-cited[>]"
                date_string = "[<]references-cited[>](.*?)[<]date[>]"+date+"[<][/]date[>](.*?)[<][/]references-cited[>]"

                if date < "17900731" and date: # Null-check
                    logging.error("""Date %s in citation list,
                                     referenced before first patent, possible problem!!"""
                                     % (date))
                if date:
                    try:
                        self.assertTrue(parsed_fields.date_app[0:4] <= max_years
                                        and parsed_fields.date_app[4:6] <= max_months
                                        and parsed_fields.date_app[6:8] <= max_days)
                    except Exception as assertionError:
                        logging.error("File:%s, date field %s is invalid!"
                                       % (xml_tuple[0], parsed_fields.date_app))
                if country:
                    postcode_match = re.search(country_string, original_xml_string,
                                               re.I + re.S + re.X)
                    try:
                        self.assertTrue(country_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, country field %s exists in cit list,
                                         but country tags do not!"""
                                         % (xml_tuple[0], country))
                if doc_number:
                    doc_number_match = re.search(doc_string, original_xml_string,
                                                 re.I + re.S + re.X)
                    try:
                        self.assertTrue(doc_number)
                    except Exception as assertionError:
                        logging.error("""File:%s, doc_number field %s exists in cit list,
                                         but doc_number tags do not!"""
                                         % (xml_tuple[0], doc_number))
                if date:
                    date_match = re.search(date_string, original_xml_string,
                                           re.I + re.S + re.X)
                    try:
                        self.assertTrue(date_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, date field %s exists in cit list,
                                         but date tags do not!"""
                                         % (xml_tuple[0], date))

                if name:
                    name_match = re.search(name_string, original_xml_string,
                                           re.I + re.S + re.X)
                    try:
                        self.assertTrue(name_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, name field %s exists in cit list,
                                         but name tags do not!"""
                                         % (xml_tuple[0], name))

    def test_rel_list(self):
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (xml_file, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]

            for entry in parsed_fields.rel_list:

                # Tags = {continuation-in-part, continuation, division, reissue}

                related_tag = entry[0]

                if related_tag:
                    related_tag_search = re.search(related_tag, original_xml_string,
                                                   re.I + re.S + re.X)
                    try:
                        self.assertTrue(related_tag_search)
                    except Exception as assertionError:
                        logging.error("""File:%s, related field %s exists in rel,
                                         but %s tags do not!"""
                                         % (xml_tuple[0], related_tag, related_tag))

    def test_law_xml(self):
        for i, xml_tuple in enumerate(parsed_xml): # xml_tuple = (xml_file, XMLpatent(xml))
            original_xml_string = open(folder + xml_tuple[0]).read() # rstrip('\t\n\r')
            parsed_fields = xml_tuple[1]
        
            # Law list

            for (last_name, first_name, country, orgname) in parsed_fields.law_list:

                last_name_string = "[<]parties[>](.*?)[<]last-name[>]"+last_name+"[<][/]last-name[>](.*?)[<][/]parties[>]"
                first_name_string = "[<]parties[>](.*?)[<]first-name[>](.*?)[<][/]first-name[>](.*?)[<][/]parties[>]"
                country_string = "[<]parties[>](.*?)[<]country[>](.*?)[<][/]country[>](.*?)[<][/]parties[>]"
                orgname_string = "[<]parties[>](.*?)[<]orgname[>](.*?)[<][/]orgname[>](.*?)[<][/]parties[>]"

                if last_name:
                    last_name_match = re.search(last_name_string, original_xml_string,
                                                re.I + re.S + re.X)
                    try:
                        self.assertTrue(last_name_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, last_name field %s exists in law,
                                         but last_name tags do not!"""
                                         % (xml_tuple[0], last_name))

                if first_name:
                    first_name_match = re.search(first_name_string, original_xml_string,
                                                 re.I + re.S + re.X)
                    try:
                        self.assertTrue(first_name_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, first_name field %s exists in law,
                                         but first_name tags do not!"""
                                         % (xml_tuple[0], first_name))

                if country:
                    country_match = re.search(country_string, original_xml_string,
                                             re.I + re.S + re.X)
                    try:
                        self.assertTrue(country_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, country field %s exists in law,
                                         but country tags do not!"""
                                         % (xml_tuple[0], country))

                if orgname:
                    orgname_match = re.search(orgname_string, original_xml_string,
                                              re.I + re.S + re.X)
                    try:
                        self.assertTrue(orgname_match)
                    except Exception as assertionError:
                        logging.error("""File:%s, orgname field %s exists in law,
                                         but orgname tags do not!"""
                                         % (xml_tuple[0], orgname))

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
