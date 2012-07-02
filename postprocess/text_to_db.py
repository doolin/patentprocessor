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
# Database to connect to

# invpat_final_from_DVN taken from DVN Folder (disambiguated results)
con = sql.connect('invpat_final_from_DVN.sqlite3') 

# Database to write to, can be initially empty
# First cold run, final_orig_invnum empty
# After that, values overwritten

fin = sql.connect('final_orig_invnum.sqlite3')

# Logging
logging.basicConfig(filename=log_file, level=logging.DEBUG)
open(log_file, "w")


# Create Final table to be inserted into
with fin:
    fin_cur = fin.cursor()

    # Chose to drop table because it is easier to test, without having to
    # copy over the invpat_final_from_DVN sqlite3 db everytime.

    fin_cur.execute("DROP TABLE IF EXISTS Final;")

    # Schema for invpat
    # fin_cur.execute("""       
    #            CREATE TABLE Final(
    #            Firstname TEXT,
    #            Lastname TEXT,
    #            Street TEXT,
    #            City TEXT,
    #            State TEXT,
    #            Country TEXT,
    #            Zipcode TEXT,
    #            Lat REAL,
    #            Lng REAL,
    #            InvSeq INT,
    #            Patent TEXT,
    #            AppYear INT,
    #            GYear INT,
    #            AppDate TEXT,
    #            Assignee TEXT,
    #            AsgNum INT,
    #            Class TEXT,
    #            Invnum TEXT,
    #            Invnum_N TEXT,
    #            Invnum_N_UC,
    #            Density REAL,
    #            Precision REAL,
    #            Recall REAL,
    #            Finalnum INT,
    #            Reldocs TEXT
    #            );
    #            """)

    # Schema for invpat_final
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
                Lon,
                InvSeq INT,
                Patent TEXT,
                GYear INT,
                AppYearStr TEXT,
                AppDateStr TEXT,
                Assignee TEXT,
                AsgNum INT,
                Class TEXT,
                Invnum PRIMARY KEY,
                lower,
                upper,
                Finalnum INT,
                Reldocs TEXT
                );
                """)


# Match out of con, append, and join operation into fin
with con:
    con_cur = con.cursor()
    logging.info("Beginning to query database")

    # Variables used in Logging
    count = 0
    success = 0
    errors = 0
    relpats = 0
    relpaterrors = 0

    print "Starting to build final database...."
    while True:
 
        line_read = opened_file.readline()
        if not line_read:
            break
        
        # Inv_Num ### Number ### Inv_Num

        count = count + 1

        if (count % 10000 == 0):
            print "Starting patent", count
        # print count

        text_line = line_read.rstrip(',\n').split("###")
        inv_num = text_line[0]
        num = int(text_line[1]) # Convert str to int to be consistent. 
        related_invs = text_line[2]
        related_invs_split = related_invs.split(',')

        # print inv_num, "###", num, "###", related_invs

        con_cur.execute("SELECT * FROM invpat WHERE (Invnum = \"%s\");" % inv_num)
        
        # con_cur.execute("SELECT * FROM invpat WHERE (Lastname
        # = \"FLEMING\" and Firstname = \"LEE\");") # Sanity Check
        
        fetched_value = con_cur.fetchone()  # Get match

        if fetched_value:
            success = success + 1
            value_to_insert = list(fetched_value)
            value_to_insert.append(num)
            value_to_insert.append(related_invs)
            fin_cur.execute("""INSERT OR IGNORE INTO Final VALUES (?,?,?,?,?,?,?,?,?,
                                ?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                tuple(value_to_insert))

            for related_inv in related_invs_split:
                # rel_patent_number = related_inv.split("-")[0]
                # rel_patent_number = related_inv.split("-")[0]
                # print rel_patent_number 
                con_cur.execute("SELECT * FROM invpat WHERE Invnum = \"%s\";"
                                % related_inv)
                fetched_value = con_cur.fetchone()  # Get match
                
                # print fetched_value

                if fetched_value:
                    relpats = relpats + 1
                    value_to_insert = list(fetched_value)
                    value_to_insert.append(num)
                    value_to_insert.append(related_invs)
                    fin_cur.execute("""INSERT OR IGNORE INTO Final VALUES (?,?,?,?,?,?,?,?,?,
                                       ?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                       tuple(value_to_insert))
                else:
                    relpaterrors = relpaterrors + 1
                    logging.error("Did not find a match for rel pat %s for invnum %s"
                                   % (rel_patent_number, inv_num))
        else:
            errors = errors + 1
            logging.error("Did not find a match for Invnum %s"
                          % inv_num)

logging.info("Successfully did %d invnums" % success)
logging.info("Successfully did %d relpats" % relpats)
logging.info("Failed %d invnums" % errors)
logging.info("Failed %d related patentss" % relpaterrors)
logging.info("Total %d querys" % count)
fin.commit()

    
                

