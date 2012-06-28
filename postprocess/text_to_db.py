import sqlite3 as sql
import sys
import os
import logging

# TODO: 
# Need to verify correctness
# Use command-line args to pass in file names

# Files
txt_file = 'final.txt'
opened_file = open(txt_file, 'U')
log_file = 't2db.log'

# Set Up SQL Connections
con = sql.connect('invpat.sqlite3') # Database to connect to
fin = sql.connect('final_Invnum.sqlite3')  # Database to write to

# Logging
logging.basicConfig(filename=log_file, level=logging.DEBUG)
open(log_file, "w")


# Create Final table to be inserted into
with fin:
    fin_cur = fin.cursor()
    fin_cur.execute("DROP TABLE IF EXISTS Final;")
    fin_cur.execute("""
                CREATE TABLE Final(
                Firstname TEXT,
                Lastname TEXT,
                Street TEXT,
                City TEXT,
                State TEXT,
                Country TEXT,
                Zipcode TEXT,
                Lat REAL,
                Lng REAL,
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
                Finalnum INT,
                Reldocs TEXT
                );
                """)
# Match out of con, append, and join operation into fin
with con:
    con_cur = con.cursor()
    logging.info("Beginning to query database")
    count = 0
    success = 0
    errors = 0
    con_cur.execute("CREATE INDEX index_invnum ON invpat (Invnum)");
    while True:
        line_read = opened_file.readline()
        if not line_read:
            break
        
        # Inv_Num ### Number ### Record-ID

        count = count + 1
        text_line = line_read.rstrip(',\n').split("###")
        inv_num = text_line[0]
        num = int(text_line[1]) # Convert str to int to be consistent. 
        final_docs = text_line[2]
        # print inv_num, "###", num, "###", final_docs
        con_cur.execute("SELECT * FROM invpat WHERE (Invnum = \"%s\");" % inv_num)
        
        # con_cur.execute("SELECT * FROM invpat WHERE (Lastname
        # = \"FLEMING\" and Firstname = \"LEE\");") # Sanity Check
        
        fetched_value = con_cur.fetchone()  # Get match

        if fetched_value:
            success = success + 1
            value_to_insert = list(fetched_value)
            value_to_insert.append(num)
            value_to_insert.append(final_docs)
            fin_cur.execute("""INSERT INTO Final VALUES (?,?,?,?,?,?,?,?,?,
                            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                            tuple(value_to_insert))
        else:
            errors = errors + 1
            logging.error("Did not find a match for Invnum %s" % inv_num)

logging.info("Successfully did %d querys" % success)
logging.info("Failed %d querys" % errors)
logging.info("Total %d querys" % count)
fin.commit()

    
                
