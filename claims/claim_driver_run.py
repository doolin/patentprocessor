#! /usr/bin/env python

import sys
import re
import StringIO
import logging
import htmlentitydefs
import datetime
from claim_driver import Claims, Claim, Claims_SQL
import sqlite3 as sql
from xml.sax import make_parser, handler, parseString, saxutils

# Utility Patents can have 1+ claims, 
# http://www.uspto.gov/web/offices/pac/mpep/s1502.html
# Inserting separately

# Global Variables
handlers = dict()
#claim_list = []
logfile = "./" + 'claim-parsing.log'
open(logfile, "wb")
logging.basicConfig(filename=logfile, level=logging.DEBUG)

# Register Callbacks

# For Claim parsing
t1 = datetime.datetime.now()

c = Claims()
handlers["file"] = c.handle_file
handlers["claims"] = c.handle_claims

# To insert claims into SQL

sq = Claims_SQL()
handlers["db_init"] = sq.initialize_con_database
handlers["insert_claims"] = sq.insert_claims
handlers["file"]()
handlers["claims"]()
handlers["db_init"]("claims.sqlite3") # Change to be CLI argument later

from claim_driver import claim_list
handlers["insert_claims"](claim_list) 

print "end time:", datetime.datetime.now()-t1
      
