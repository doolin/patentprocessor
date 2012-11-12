#! /usr/bin/env python

import unittest
import re
import os
import sys
import logging
from claim_driver import *

# Have 3 test files, with one, ten, hundred patents.

test_patent_one = "pg020507one.xml"
test_patent_ten = "pg020507ten.xml"
test_patent_hundred = "pg020507hundred.xml"

# For one patent
claim_string = "We claim the ornamental design for a garment, as shown and described."


class TestClaimDriver(unittest.TestCase):
    
    def setUp(self):
        self.c = Claims()
        self.c_ten = Claims()
        self.c_hun = Claims()
        self.claim_list = []
        self.claim_list_ten = []
        self.claim_list_hun = []
        self.sq = Claims_SQL()

    def test_claims_init_sanity(self):
        # Tests init of Claims() works as intended
        # Namely, to see if c.XMLs == []
        assert(not self.c.XMLs)

    def test_remove_special_entities(self):
        special_entity_string = "&.*?;"
        special_entity_string = self.c.handle_special_entities(special_entity_string)
        # Special characters should be removed
        assert(not special_entity_string)

    #######################
    # Test for One Patent #
    #######################

    # Parsing

    def test_claims_handle_file(self):
        self.c.handle_file(test_patent_one)
        # self.c.XMLs should be the xml passed in to be
        # parsed at this point
        assert(self.c.XMLs)

    def test_claims_parse(self):
        self.c.handle_file(test_patent_one)
        self.c.handle_claims()
        self.claim_list = self.c.return_claims()
        assert(self.claim_list)

    def test_claims_parse_patent_number(self):
        self.c.handle_claims()
        self.claim_list = self.c.return_claims()
        assert(self.claim_list[0][0] == "D0456588")

    def test_claims_parse_claim(self):
        self.c.handle_claims()
        self.claim_list = self.c.return_claims()     
        assert(self.claim_list[0][1] == claim_string)

    # SQL

    def test_sql_patent_init_sanity(self):
        assert(not self.sq.con)
        assert(not self.sq.cursor)

    def test_sql_claims(self):
        self.claim_list = self.c.return_claims()
        self.sq.initialize_con_database(":memory:")
        self.sq.insert_claims(self.claim_list)
        self.sq.cursor.execute("SELECT * FROM claims;")
        row_data = self.sq.cursor.fetchall()
        assert(len(row_data) == 1)
        assert(row_data[0][0] == "D0456588")
        assert(row_data[0][1] == claim_string)


if __name__ == '__main__':
    unittest.main()



