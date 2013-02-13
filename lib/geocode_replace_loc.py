
# Create SQL statements for passing in to function replace_loc
# in geocode.py. These statements were originally in geocode.py
# and have been put here both for debugging purposes and to
# modularize the process.

import sys

# TODO: Unit test this so that it and the unit test can be
# eliminated in a future redesign. Also, ensure that this
# is the correct name for this function, and adjust accordingly.
def table_temp1_has_rows(cursor):
    return cursor.execute("SELECT count(*) FROM temp1").fetchone()[0] > 0

def print_table_info(c):
    field = ["[%s]" % x[1] for x in c.execute("PRAGMA TABLE_INFO(temp1)")][2:6]
    var_f = ",".join(field)
    print "var_f: ", var_f


def create_table_temp2(cursor):
    cursor.executescript("""
        CREATE TEMPORARY TABLE temp2 AS
            SELECT  CityA,
                    StateA,
                    CountryA,
                    ZipcodeA,
                    count(*) AS cnt
              FROM  temp1
          GROUP BY  CityA,
                    StateA,
                    CountryA,
                    ZipcodeA;

        CREATE INDEX IF NOT EXISTS t2_idx ON temp2 (CityA, StateA, CountryA, ZipcodeA);
          """)


# TODO: Find a way to unit test this set of queries
def create_loc_and_locmerge_tables(cursor):

    create_table_temp2(cursor)

    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS t1_idx ON temp1 (CityA, StateA, CountryA, ZipcodeA);

        INSERT OR REPLACE INTO locMerge
            SELECT  b.cnt,
                    a.*,
                    SUBSTR(a.CityA,1,3)
              FROM  temp1 AS a
        INNER JOIN  temp2 AS b
                ON  a.CityA = b.CityA
               AND  a.StateA = b.StateA
               AND  a.CountryA = b.CountryA
               AND  a.ZipcodeA = b.ZipcodeA;

        CREATE TEMPORARY TABLE temp3 AS
            SELECT  a.*
              FROM  LOC AS a
              LEFT JOIN locMerge AS b
                ON  a.City = b.City
               AND  a.State = b.State
               AND  a.Country = b.Country
               AND  a.Zipcode = b.Zipcode
             WHERE  b.Zipcode IS NULL;

        DROP TABLE IF EXISTS loc;

        CREATE TABLE loc AS SELECT * FROM temp3;

        CREATE INDEX IF NOT EXISTS loc_idxCC ON loc (City, Country);
        CREATE INDEX IF NOT EXISTS loc_idx   ON loc (City, State, Country, Zipcode);
        CREATE INDEX IF NOT EXISTS loc_idxCS ON loc (City, State);

        DROP TABLE IF EXISTS temp2;
        DROP TABLE IF EXISTS temp3;
          """)



def domestic_sql():

     print sys._getframe().f_code.co_name

     stmt = """SELECT  11,
               a.cnt as cnt,
               a.city as CityA,
               a.state as StateA,
               a.country as CountryA,
               a.zipcode as ZipcodeA,
               b.city,
               b.state,
               'US',
               b.zipcode,
               b.latitude,
               b.longitude
         FROM  loc AS a
   INNER JOIN  usloc AS b
           ON  SEP_WRD(CityA, %d) = b.city
          AND  StateA = b.state
          AND  CountryA = 'US'
        WHERE  SEP_CNT(CityA) >= %d
          AND  CityA != '' """
     return stmt;


def domestic_block_remove_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  11,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.city,
                b.state,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  loc AS a
    INNER JOIN  usloc AS b
            ON  BLK_SPLIT(SEP_WRD(a.City, %d)) = b.blkcity
           AND  a.state = b.state
           AND  a.country = 'US'
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != '' """
      return stmt;


def domestic_first3_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  (10+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)),
                b.BlkCity)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.city,
                b.state,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  loc AS a
    INNER JOIN  usloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3) = b.City3
           AND  a.state = b.state
           AND  a.country = 'US'
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ''
      ORDER BY  a.City, a.State, jaro"""
      return stmt;


def domestic_last4_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  (10+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)),
                b.BlkCity)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.city,
                b.state,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  loc AS a
    INNER JOIN  usloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4) = b.City4R
           AND  a.state = b.state
           AND  a.country = 'US'
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.State, jaro"""
      return stmt;


# JR Code started taking longer to run at this statement
def foreign_full_name_1_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  21,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.full_name_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City!="" """
      return stmt;


def foreign_full_name_2_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  21,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.full_name_nd_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """
      return stmt;


def foreign_short_form_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  21,
                a.cnt     AS cnt,
                a.city    AS CityA,
                a.state   AS StateA,
                a.country AS CountryA,
                a.zipcode AS ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc           AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.short_form
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """
      return stmt;


def foreign_block_split_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  21,
                a.cnt     AS cnt,
                a.city    AS CityA,
                a.state   AS StateA,
                a.country AS CountryA,
                a.zipcode AS ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  BLK_SPLIT(SEP_WRD(a.City, %d)) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """
      return stmt;


def foreign_first3_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  (20+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)),
                b.sort_name_ro)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.Country, jaro"""
      return stmt;



def foreign_last4_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  (20+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)),
                b.sort_name_ro)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                "",
                b.cc1,
                "",
                b.lat,
                b.long
          FROM  loc AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.Country, jaro"""
      #""" % (sep, sep, "20.90", scnt))
      return stmt;


def domestic_2nd_layer_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  15,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.city,
                b.state,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  usloc AS b
            ON  a.NCity = b.city
           AND  a.NState = b.state
           AND  a.NCountry = 'US'"""
      return stmt;


def domestic_first3_2nd_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  14+jarow(BLK_SPLIT(a.NCity),
                b.BlkCity) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.city,
                b.state,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  usloc AS b
            ON  SUBSTR(BLK_SPLIT(a.NCity),1,3) = b.City3
           AND  a.Nstate = b.state
           AND  a.Ncountry ='US'
         WHERE  jaro > %s
      ORDER BY  a.NCity, a.NState, jaro"""
      return stmt;


def foreign_full_name_2nd_layer_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  25,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                '' as state,
                b.cc1,
                '' as zip,
                b.lat,
                b.long
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  a.NCity = b.full_name_ro
           AND  a.NCountry = b.cc1"""
      return stmt;


def foreign_full_nd_2nd_layer_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  25,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                '' as state,
                b.cc1,
                '' as zip,
                b.lat,
                b.long
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  a.NCity = b.full_name_nd_ro
           AND  a.NCountry = b.cc1"""
      return stmt;


def foreign_no_space_2nd_layer_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  25,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                '' as state,
                b.cc1,
                '' as zip,
                b.lat,
                b.long
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  BLK_SPLIT(a.NCity) = b.sort_name_ro
           AND  a.NCountry = b.cc1"""
      return stmt;


def foreign_first3_2nd_jaro_winkler_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  24+jarow(BLK_SPLIT(a.NCity),
                b.sort_name_ro) AS Jaro,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.full_name_nd_ro,
                '' as state,
                b.cc1,
                '' as zip,
                b.lat,
                b.long
          FROM  (SELECT  * FROM  loc WHERE  NCity IS NOT NULL) AS a
    INNER JOIN  loctbl.gnsloc AS b
            ON  SUBSTR(BLK_SPLIT(a.NCity),1,3) = b.sort_name_ro
           AND  a.Ncountry = b.cc1
         WHERE  jaro > %s
      ORDER BY  a.NCity, a.NCountry, jaro"""
      return stmt;


def domestic_zipcode_sql():

      print sys._getframe().f_code.co_name

      stmt = """SELECT  31,
                a.cnt as cnt,
                a.city as CityA,
                a.state as StateA,
                a.country as CountryA,
                a.zipcode as ZipcodeA,
                b.City,
                b.State,
                'US',
                b.zipcode,
                b.latitude,
                b.longitude
          FROM  (SELECT  *, (SEP_WRD(zipcode,0)+0) as Zip2 FROM loc WHERE  Zipcode != '' AND Country = 'US') AS a
    INNER JOIN usloc AS b
            ON  a.Zip2 = b.Zipcode"""
      return stmt;


# TODO: Add this block to its own function, add a commented out call to
# to that function here.
####    ##DOMESTIC (State miscode to Country)
####    replace_loc("""
####        SELECT  31,
####                a.cnt, a.city, a.state, a.country, a.zipcode,
####                b.city, b.state, 'US', b.zipcode, b.lat, b.long
####          FROM  loc AS a INNER JOIN usloc AS b
####            ON  SEP_WRD(a.City, %d)=b.city AND a.country=b.state
####         WHERE  SEP_CNT(a.City)>=%d AND a.City!="";
####        """ % (sep, scnt))


##MISSING JARO (FIRST 3)
#replace_loc("""
#    SELECT  30+jarow(a.City, b.City) AS Jaro,
#            a.cnt, a.city, a.state, a.country, a.zipcode,
#            b.ncity, b.nstate, b.ncountry, b.nzipcode, b.nlat, b.nlong
#      FROM  loc AS a INNER JOIN locMerge AS b
#        ON  a.City3=b.City3 AND a.state=b.state AND a.country=b.country
#     WHERE  jaro>%s AND a.City!=""
#  ORDER BY  a.City, a.State, a.Country, jaro;
#    """ % ("30.95"))
