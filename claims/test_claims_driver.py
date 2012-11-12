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


class TestClaimDriver(unittest.TestCase):
    
    def setUp(self):
        self.c = Claims()
        self.claim_list = []

    def test_claims_init_sanity(self):
        # Tests init of Claims() works as intended
        # Namely, to see if c.XMLs == []
        assert(not self.c.XMLs)

    def test_claims_handle_file(self):
        self.c.handle_file(test_patent_one)
        # self.c.XMLs should be the xml passed in to be
        # parsed at this point
        assert(self.c.XMLs)

    def test_remove_special_entities(self):
        special_entity_string = "&.*?;"
        special_entity_string = self.c.handle_special_entities(special_entity_string)
        # Special characters should be removed
        assert(not special_entity_string)

    def test_claim_store(self):
        self.c.store_claims("claim1")
        self.c.store_claims("claim2")
        self.c.store_claims("claim3")
        self.c.store_claims("claim4")
        from claim_driver import claim_list as cl
        assert(cl[0] == "claim1")
        assert(cl[1] == "claim2")
        assert(cl[2] == "claim3")
        assert(cl[3] == "claim4")
        # Reset claims
        self.c.claim_list = []
        
        
        

        




if __name__ == '__main__':
    unittest.main()



