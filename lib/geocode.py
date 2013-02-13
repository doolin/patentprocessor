# Non_US http://earth-info.nga.mil/gns/html/gis_countryfiles.htm
# US     http://geonames.usgs.gov/domestic/download_data.htm

# NEED TO DO...
# CREATE INDEX IF NOT EXISTS idx_ctc0 ON gnsloc (SORT_NAME, CC1);

import datetime
import csv
import os
import re
import sqlite3

from fwork import tblExist

# TODO: cover geocode setup functions with unit tests.
from geocode_setup import *

conn = get_connection("hashTbl.sqlite3")
c = get_cursor(conn)
create_sql_helper_functions(conn)

print "Start setup for geocoding: ", datetime.datetime.now()
geocode_db_initialize(c)
loc_create_table(c)
if not(tblExist(c, "locMerge")):
    fix_city_country(c)
    fix_state_zip(c)
    create_loc_indexes(conn)

create_usloc_table(c)
create_locMerge_table(c)
print "Finish setup for geocoding: ", datetime.datetime.now()

# End of setup.
# Exiting here gets the initial hashTbl.sqlite3 file when
# executed as `python lib/geocode.py`
#exit()


# geocode_replace_loc consists of a series of functions,
# each with a SQL statement that is passed as a parameter
# to replace_loc. Uses temporary tables for handling
# intermediate relations.
from geocode_replace_loc import *

def print_loc_and_merge(c):
    VarX = c.execute("select count(*) from loc").fetchone()[0]
    VarY = c.execute("select count(*) from locMerge").fetchone()[0]
    print " - Loc =", VarX, " OkM =", VarY, " Total =", VarX+VarY, "  ", datetime.datetime.now()


# TODO: Unit test extensively.
def replace_loc(script):

    c.execute("DROP TABLE IF EXISTS temp1")
    c.execute("CREATE TEMPORARY TABLE temp1 AS %s" % script)
    # Apparently, this tmp1_idx is either superfluous or redundant.
    #c.execute("CREATE INDEX IF NOT EXISTS tmp1_idx ON temp1 (CityA, StateA, CountryA, ZipcodeA)")

    #print_table_info(c)

    # TODO: Which tables will pass this conditional?
    if table_temp1_has_rows(c):
        create_loc_and_locmerge_tables(c)
        print_loc_and_merge(c)

    conn.commit()


# Prefixed tablename (loc) with with dbname (also loc)
print "Loc =", c.execute("select count(*) from loctbl.loc").fetchone()[0]

# TODO: Refactor the range call into it's own function, unit test
# that function extensively.
# TODO: Figure out what these hardcoded parameters mean.
for scnt in range(-1, c.execute("select max(sep_cnt(city)) from loctbl.loc").fetchone()[0]+1):

    sep = scnt
    print "------", scnt, "------"
    replace_loc(domestic_sql()                     % (sep, scnt))
    replace_loc(domestic_block_remove_sql()        % (sep, scnt))
    replace_loc(domestic_first3_jaro_winkler_sql() % (sep, sep, "10.92", scnt))
    replace_loc(domestic_last4_jaro_winkler_sql()  % (sep, sep, "10.90", scnt))
    replace_loc(foreign_full_name_1_sql()          % (sep, scnt))
    replace_loc(foreign_full_name_2_sql()          % (sep, scnt))
    replace_loc(foreign_short_form_sql()           % (sep, scnt))
    replace_loc(foreign_block_split_sql()          % (sep, scnt))
    replace_loc(foreign_first3_jaro_winkler_sql()  % (sep, sep, "20.92", scnt))
    replace_loc(foreign_last4_jaro_winkler_sql()   % (sep, sep, "20.90", scnt))

### End of for loop

print "------ F ------"

# TODO: Put these calls into a function.
replace_loc(domestic_2nd_layer_sql())
replace_loc(domestic_first3_2nd_jaro_winkler_sql() % ("14.95"))
replace_loc(foreign_full_name_2nd_layer_sql())
replace_loc(foreign_full_nd_2nd_layer_sql())
replace_loc(foreign_no_space_2nd_layer_sql())
replace_loc(foreign_first3_2nd_jaro_winkler_sql()  % ("24.95"))
replace_loc(domestic_zipcode_sql())

conn.commit()
c.close()
conn.close()
