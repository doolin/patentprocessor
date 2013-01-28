import sys
import datetime, csv, os, re, sqlite3, unicodedata
sys.path.append("lib")
import SQLite
from locFunc import uniasc, cityctry
from fwork import *
from config import *

# TODO: Find a file that represents US Cities and Zipcodes
#       for now, use CD_ZIP.sqlite3

s = SQLite.SQLite(loc["db"], tbl=loc["nat_tbl"])
s.attach(loc["us_db"])
s.replicate(tbl=loc["us_tbl"], db="db")
s.addSQL(loc["us_tbl"], db="db", errlog=loc["nat_error"], header=True)

s.c.executescript("""
    CREATE TABLE IF NOT EXISTS typos (
        City       VARCHAR,
        State      VARCHAR,
        Country    VARCHAR,
        NewCity    VARCHAR,
        NewState   VARCHAR,
        NewCountry VARCHAR);
    """)

s.chgTbl("typos")
s.index(["City", "State", "Country"], unique=True)
s.index(["Country"])
s.index(["City", "State"])
s.index(["City", "Country"])
s.addSQL(loc["typo"])
s.close()
