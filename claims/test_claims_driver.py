#! /usr/bin/env python

import unittest
import re
import os
import sys
import logging
from claim_driver import *
from test_claims_data import *



class TestClaimDriver(unittest.TestCase):

    #########################
    # Basic Tests and Setup #
    #########################
    
    def setUp(self):
        self.c = Claims()
        self.c_ten = Claims()
        self.c_hun = Claims()

        self.ch = Claim()
        self.ch_ten = Claim()
        self.ch_hun = Claim()

        self.claim_list = []
        self.claim_list_ten = []
        self.claim_list_hun = []

        self.sq = Claims_SQL()
        self.sq_ten = Claims_SQL()
        self.sq_hun = Claims_SQL()

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
        import claim_driver
        claim_driver.claim_list = []
        self.c.handle_file(test_patent_one)
        self.c.handle_claims(self.ch)
        self.claim_list = self.c.return_claims()
        assert(self.claim_list)

    def test_claims_parse_patent_number(self):
        import claim_driver
        claim_driver.claim_list = []
        self.c.handle_file(test_patent_one)
        self.c.handle_claims(self.ch)
        self.claim_list = self.c.return_claims()
        assert(self.claim_list[0][0] == "D0456588")

    def test_claims_parse_claim(self):
        import claim_driver
        claim_driver.claim_list = []
        self.c.handle_file(test_patent_one)
        self.c.handle_claims(self.ch)
        self.claim_list = self.c.return_claims()     
        assert(self.claim_list[0][1] == claim_string)

    # SQL

    def test_sql_patent_init_sanity(self):
        assert(not self.sq.con)
        assert(not self.sq.cursor)

    def test_sql_claims(self):
        import claim_driver
        claim_driver.claim_list = []
        self.c.handle_file(test_patent_one)
        self.c.handle_claims(self.ch)
        self.claim_list = self.c.return_claims()
        self.sq.initialize_con_database(":memory:")
        self.sq.insert_claims(self.claim_list)
        self.sq.cursor.execute("SELECT * FROM claims;")
        row_data = self.sq.cursor.fetchall()
        # There should only be one row for one patent
        # print row_data
        assert(len(row_data) == 1)
        assert(row_data[0][0] == "D0456588")
        assert(row_data[0][1] == claim_string)

    ########################
    # Test for Ten Patents #
    ########################

    def test_claims_parse_ten(self):
        self.c_ten.handle_file(test_patent_ten)
        self.c_ten.handle_claims(self.ch_ten)
        self.claim_list_ten = self.c_ten.return_claims()
        assert(self.claim_list_ten)

    def test_claims_parse_patent_number_ten(self):
        import claim_driver
        claim_driver.claim_list = []
        self.c_ten.reset_claims()
        self.ch_ten.reset_claims()
        self.c_ten.handle_file(test_patent_ten)
        self.c_ten.handle_claims(self.ch_ten)
        self.claim_list_ten = self.c_ten.return_claims()
        assert(len(self.claim_list_ten) == 10)
        assert(self.claim_list_ten[0][0] == "D0456589")
        assert(self.claim_list_ten[1][0] == "D0456590")
        assert(self.claim_list_ten[2][0] == "D0456591")
        assert(self.claim_list_ten[3][0] == "D0456592")
        assert(self.claim_list_ten[4][0] == "D0456593")
        assert(self.claim_list_ten[5][0] == "D0456594")
        assert(self.claim_list_ten[6][0] == "D0456595")
        assert(self.claim_list_ten[7][0] == "D0456596")
        assert(self.claim_list_ten[8][0] == "D0456597")
        assert(self.claim_list_ten[9][0] == "D0456598")


    def test_claims_parse_claim_ten(self):
        import claim_driver
        claim_driver.claim_list = []
        self.c_ten.handle_file(test_patent_ten)
        self.c_ten.handle_claims(self.ch_ten)
        self.claim_list_ten = self.c_ten.return_claims()
        # print self.claim_list_ten
        assert(len(self.claim_list_ten) == 10)
        assert(self.claim_list_ten[0][1] == claim_string_10_1)
        assert(self.claim_list_ten[1][1] == claim_string_10_2)
        assert(self.claim_list_ten[2][1] == claim_string_10_3)
        assert(self.claim_list_ten[3][1] == claim_string_10_4)
        assert(self.claim_list_ten[4][1] == claim_string_10_5)
        assert(self.claim_list_ten[5][1] == claim_string_10_6)
        assert(self.claim_list_ten[6][1] == claim_string_10_7)
        assert(self.claim_list_ten[7][1] == claim_string_10_8)
        assert(self.claim_list_ten[8][1] == claim_string_10_9)
        assert(self.claim_list_ten[9][1] == claim_string_10_10)
        
 

if __name__ == '__main__':
    unittest.main()



