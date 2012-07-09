import sqlite3 as sql
import sys
import os
import logging
import csv

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

def process_line(line):
    return line

# Started 1:30PM, Finished 1:49PM
def process_csv(opened_file_name):
    return_list = []
    csv_reader = csv.reader(opened_file_name)
    for row in csv_reader:
        return_list.append(process_line(row))
    return return_list

# Started 1:54, Finished 2:15PM
def build_query_string(first_name, last_name, patent_number):
    query_string = """SELECT * FROM invpat WHERE 
                        (Firstname = \"%s\" and Lastname = \"%s\"
                         and Patent = \"%s\");""" % (first_name, last_name, patent_number)
    return query_string

# Started 2:30PM, Finished 3:15PM
def con_sql_match(query_string, database):
    con = sql.connect(database)
    con_cur = con.cursor()
    con_cur.execute(query_string)
    return con_cur.fetchone()

def con_sql_match_all(query_string, database):
    con = sql.connect(database)
    con_cur = con.cursor()
    con_cur.execute(query_string)
    return con_cur.fetchall()

# Started 11:26AM, Finished 
def process_input_db_query_drop(tuple_result):
    result_as_list = list(tuple_result)
    result_as_list.pop(20)
    result_as_list.pop(20)
    result_as_list.pop(20)
    return tuple(result_as_list)
    








    

