#! /usr/bin/env python

import sys
import re
import StringIO
import logging
import htmlentitydefs
import datetime
import sqlite3 as sql
from xml.sax import make_parser, handler, parseString, saxutils

claim_list = []

# Claims class for setting up files
class Claims():

    def __init__(self):
      self.XMLs = []
     
    def handle_file(self, filename):
      # print "Setting up XML files to be parsed..."
      with open(filename, "U") as filename: 
        self.XMLs = re.findall(
            r"""
                ([<]PATDOC.*?[>]       #all XML starts with ?xml
                .*?
                [<][/]PATDOC[>])    #and here is the end tag
             """, filename.read(),  re.I + re.S + re.X)
             
    def handle_claims(self, content_handler):
      i = 0
      for i, xml in enumerate(self.XMLs):
        try:
          #if (i%1000 == 0):
          # print "Parsing Patent:", i
          parseString(self.handle_special_entities(xml), content_handler)
        except Exception as e:
          print "found error", e
          logging.error("\n\nError at Patent: %d" % (i+1))
          logging.error(xml)
      # print "Processed:", i+1, "Patents!"
          
    def handle_special_entities(self, s):
      # Currently removing all special characters
      # But this needs to change. 
      return re.sub(r'&.*?;',"", s)

    def store_claims(self, claims):
      claim_list.append(claims)
        
    def print_claims(self):
      for claims in claim_list:
        print "current claim is:", claims 

    def return_claims(self):
      return claim_list

    def reset_claims(self):
      claim_list = []

# Claim class to handle SAX Parsing
class Claim(handler.ContentHandler):

    def __init__(self):
        claim_list = []
        self.claims = []
        self.patent = None
        self.b110tag = False
        self.dnumtag = False
        self.pdattag = False
        self.cltag = False
        self.clmtag = False
        self.paratag = False
        self.ptexttag = False
        self.pdattag = False
        self.patdoctag = False
        
    def startElement(self, name, attrs):
        if name == "PATDOC":
            self.patdoctag = True
        if name == "B110":
            self.b110tag = True
        if name == "DNUM":
            self.dnumtag = True
        if name == "PDAT":
            self.pdattag = True
        if name == "CL":
            self.cltag = True
        if name == "CLM":
            self.clmtag = True
        if name == "PARA":
            self.paratag = True
        if name == "PTEXT":
            self.ptexttag = True
        if name == "PDAT":
            self.pdattag = True
              
    def endElement(self, name):
        if name == "PATDOC":
            self.patdoctag = False
        if name == "B110":
            self.b110tag = False
        if name == "DNUM":
            self.dnumtag = False
        if name == "PDAT":
            self.pdat = False
        if name == "CL":
            self.cltag = False
        if name == "CLM":
            self.clmtag = False
        if name == "PARA":
            self.paratag = False
        if name == "PTEXT":
            self.ptexttag = False
        if name == "PDAT":
            self.pdattag = False
    
    def characters(self, content):
        if (self.b110tag and self.dnumtag and self.pdattag):
            self.patent = content
        if (self.cltag and self.clmtag and self.paratag and 
            self.ptexttag and self.pdattag):
            self.claims.append((self.patent, content))

    def endDocument(self):
        for cl in self.claims:
            claim_list.append(cl)
        self.claims = []

    def reset_claims(self):
        claim_list = []
        self.claims = []
        
        
# SQL Class to handle cursors, database creation
class Claims_SQL():

  def __init__(self):
    self.con = None
    self.cursor = None
    
  def initialize_con_database(self, con_db_name):
    # Set Up SQL Connectionss
    # Database to connect to
    self.con = sql.connect(con_db_name)
    self.cursor = self.con.cursor()   
    self.cursor.execute("DROP TABLE IF EXISTS claims;")
    # Schema for Claims
    self.cursor.execute("""CREATE TABLE claims(
                           Patent TEXT,
                           Claims TEXT);
                    	""")
                    	    
  def insert_claims(self, claim_list):
    for claim_tuple in claim_list:
      self.cursor.execute("""INSERT OR 
                          IGNORE INTO claims VALUES (?,?);""" ,
                          claim_tuple)
    self.con.commit()






