import sqlite3 as sql
import sys
import os
import logging


# TODO: 
# Need to verify correctness
# Use command-line args to pass in file names
# Make this better, refactor, test
# Remove precision, density, recall

def initialize_sql_databases():
    # Set Up SQL Connections
    # Database to connect to
    con = sql.connect('invpat.sqlite3')
    # Database to write to 
    fin = sql.connect('mercury2.sqlite3') 

def initialize_logging(log_file):
    # Logging
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    open(log_file, "w")
    count = 0
    success = 0
    errors = 0


