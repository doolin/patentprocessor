import sqlite3 as sql
import sys
import os
import logging

# TODO: 
# Need to verify correctness
# Use command-line args to pass in file names
# Make this better, refactor, test
# Remove precision, density, recall

def initialize_con_database(con_db_name):
    # Set Up SQL Connections
    # Database to connect to
    con = sql.connect(con_db_name)
    con_cur = con.cursor()

def initialize_fin_database(fin_db_name):
    # Database to write to 
    fin = sql.connect(fin_db_name) 
    fin_cur = fin.cursor()

def initialize_logging(log_file):
    # Logging
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    open(log_file, "w")
    count = 0
    success = 0
    errors = 0

def make_final_table():
    # Create Final table to be inserted into
    with fin:
        # fin_cur = fin.cursor()
        fin_cur.execute("DROP TABLE IF EXISTS invpat;")
        # Schema for invpat
        fin_cur.execute("""CREATE TABLE invpat(
                           Firstname TEXT,
                           Lastname TEXT,
                	   Street TEXT,
                	   City TEXT,
                	   State TEXT,
                	   Country TEXT,
                	   Zipcode TEXT,
                	   Latitude REAL,
                	   Longitude REAL,
                	   InvSeq INT,
                	   Patent TEXT,
                	   AppYear INT,
                	   GYear INT,
                	   AppDate TEXT,
                	   Assignee TEXT,
                	   AsgNum INT,
                	   Class TEXT,
                	   Invnum TEXT,
                	   Invnum_N TEXT,
                	   Invnum_N_UC,
                	   Density REAL,
                	   Precision REAL,
                	   Recall REAL,
                           Middlename TEXT,
                	   Unique_Record_ID TEXT,
                	   ApplyYear INT,
                	   Coauthor TEXT
                           );
                        """)

def reset_logging():
    open(log_file, "w")
    count = 0
    success = 0
    errors = 0

def commit_changes():
    with fin:
        fin.commit()

def con_sql_match(first_name, last_name, patent_number):
    with con:
        con_cur.execute("""SELECT * FROM invpat WHERE 
                          (Firstname = \"%s\" and Lastname = \"%s\"
                           and Patent = \"%s\");""" % (first_name, last_name, patent_number))
        return con_cur.fetchone()

def con_sql_match(first_name, last_name, patent_number):
    with con:
        con_cur.execute("""SELECT * FROM invpat WHERE 
                          (Firstname = \"%s\" and Lastname = \"%s\"
                           and Patent = \"%s\");""" % (first_name, last_name, patent_number))
        return con_cur.fetchone()

def process_line(line):
    sl = line.split(",")
    #print sl
    return sl
