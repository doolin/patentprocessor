#!/usr/bin/env python

import sqlite3 as sql
import sys
import os
import logging
import csv

from subprocess import call
from optparse import OptionParser

# TODO: 
# Need to verify correctness
# Use command-line args to pass in file names
# Make this better, refactor, test
# Remove precision, density, recall

def initialize_con_database(con_db_name):
    # Set Up SQL Connectionss
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

def make_final_table(connection):
    # Create Final table to be inserted into
    with connection:
        fin_cur = connection.cursor()
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
    # Inconsistences!
    if (type(first_name) is not str):
        first_name = str(first_name)
    if (type(last_name) is not str):
        last_name = str(last_name)
    if (type(patent_number) is not str):
        patent_number = str(patent)

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

# Started 11:26AM, Finished 11:48AM
def process_input_db_query_drop(tuple_result):
    # Drop unneccessary fields
    result_as_list = list(tuple_result)
    result_as_list.pop(20)
    result_as_list.pop(20)
    result_as_list.pop(20)
    return tuple(result_as_list)

# Started 11:50AM, Finished 12:26PM 
def process_input_db_query_add(tuple_result):
    # Add necessary fields
    result_as_list = list(tuple_result)
    firstname_field = result_as_list[0]
    invnum_field = result_as_list[17]
    appyear_field = result_as_list[11]
    coauthor_field = ""
    result_as_list.append(firstname_field)
    result_as_list.append(invnum_field)
    result_as_list.append(appyear_field)
    result_as_list.append(coauthor_field)
    return tuple(result_as_list)

# Started 12:46PM, Finished 1:16PM
def insert_tuple_into_output_db(insert_tuple, output_db):
    fin = sql.connect(output_db)
    fin_cur = fin.cursor()
    # print "length of inserted tuple is...", len(insert_tuple)
    #fin_cur.execute("""INSERT INTO invpat VALUES(?,?,?,?,?,?,?,?,?,?,
    #                   ?,?,?,?,?,?,?,?,?,?,?,?);""", insert_tuple)
    # print insert_tuple
    fin_cur.execute("""INSERT INTO invpat VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""" , insert_tuple)
    fin.commit()


if __name__ == '__main__':

    # Started 2:15, Finished 2:41
    # Do something here
    # 1. Filename.txt (required)
    # 2. Source db (optional)
    # 3. Final db (optional)

    parser = OptionParser()

    parser.add_option("-f", "--file", dest="infilename", default = "../../../e2e/mercury13.csv", help="CSV File Location", metavar="FILE")
    parser.add_option("-i", "--input", dest="indb", default = "../../../e2e/invpat.sqlite3", help="Input Database Location", metavar="FILE")
    parser.add_option("-o", "--output", dest="outdb", default = "testgen.sqlite3", help="Output Database Location", metavar="FILE")
   

    (options, args) = parser.parse_args()

    in_file = options.infilename
    in_db = options.indb
    out_db = options.outdb
    
    print "\nStarting Generator.py    \n\n"
    print "File Locations:\n "
    print "in_file: ", in_file
    print "in_database: ", in_db
    print "out_database: ", out_db
    print "\n---------------------------------\n"

    # Started 2:50PM, Finished 5:15PM

    # Begin main():

    csv_list = process_csv(open(in_file))
    initialize_logging('generator_errors.log')
    make_final_table(sql.connect(out_db))
    for csv in csv_list:
        # fn = csv[0], ln = csv[1], p = csv[2]
        query_string = build_query_string(csv[0],csv[1],csv[2])
        sql_result = con_sql_match(query_string, in_db)
        # Must drop before add
        result_after_drop =  process_input_db_query_drop(sql_result)
        result_after_add = process_input_db_query_add(result_after_drop)
        insert_tuple_into_output_db(result_after_add, out_db)

    s = "sqlite3 -header -csv " + out_db + " 'select * FROM invpat' > generate.csv"
    call(s, shell=True) # Need Shell = True
 
        
        
    
    

    

    
        
    
    







    

