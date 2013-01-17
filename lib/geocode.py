#Non_US http://earth-info.nga.mil/gns/html/gis_countryfiles.htm
#US     http://geonames.usgs.gov/domestic/download_data.htm

##NEED TO DO...
##    CREATE INDEX IF NOT EXISTS idx_ctc0 ON gnsloc (SORT_NAME, CC1);

import datetime, csv, os, re, sqlite3

#from fwork import *
# We need to import these one at a time because many of these functions are
# duplicated in multiple places. That is, there are 3 or 4 identical or
# slightly different versions located in a different files.
from fwork import jarow
from fwork import cityctry
from fwork import tblExist

# Extract to its own file and unit test.
# Later, this may be able to go into fwork
def sep_wrd(word, seq):
    if seq==-1:
        return word
    else:
        p = re.compile(" *?[,|] *")
        ln = p.split(word)
        if len(ln)> seq:
            return ln[seq]
        else:
            return ""

conn = sqlite3.connect("hashTbl.sqlite3")
c = conn.cursor()

conn.create_function("blk_split", 1, lambda x: re.sub(" ", "", x))
conn.create_function("sep_cnt",   1, lambda x: len(re.findall("[,|]", x)))
conn.create_function("jarow",     2, jarow)
conn.create_function("cityctry",  3, cityctry)
conn.create_function("sep_wrd",   2, sep_wrd)
conn.create_function("rev_wrd",   2, lambda x,y:x.upper()[::-1][:y])


# NOTE: Keep these imports function-specific until everything
# is covered with unit tests, and we know that the structure
# is maintainable.
from geocode_setup import geocode_db_initialize
from geocode_setup import loc_create_table
from geocode_setup import fix_city_country
from geocode_setup import fix_state_zip
from geocode_setup import create_loc_indexes

geocode_db_initialize(c)
loc_create_table(c)

if not(tblExist(c, "locMerge")):
    print datetime.datetime.now()
    fix_city_country(c)
    print datetime.datetime.now()
    fix_state_zip(c)
    create_loc_indexes(conn)
    print datetime.datetime.now()



from geocode_setup import create_usloc_table
create_usloc_table(c)
print datetime.datetime.now()

from geocode_setup import create_locMerge_table
create_locMerge_table(c)



# This should be the end of the setup, and all the above should be able
# to go into its own file and be imported into this script. One benefit
# of separating it out may be to allow much easier unit testing for the
# location matching which follows.


# TODO: Find a way to unit test this set of queries
def create_loc_and_locmerge_tables(conn):
    conn.executescript("""
        CREATE TEMPORARY TABLE temp2 AS
            SELECT  count(*) as cnt, CityA, StateA, CountryA, ZipcodeA
              FROM  temp1
          GROUP BY  CityA, StateA, CountryA, ZipcodeA;
        CREATE INDEX IF NOT EXISTS t1_idx ON temp1 (CityA, StateA, CountryA, ZipcodeA);
        CREATE INDEX IF NOT EXISTS t2_idx ON temp2 (CityA, StateA, CountryA, ZipcodeA);
        INSERT OR REPLACE INTO locMerge
            SELECT  b.cnt, a.*, SUBSTR(a.CityA,1,3)
              FROM  temp1 AS a
        INNER JOIN  temp2 AS b
                ON  a.CityA=b.CityA AND a.StateA=b.StateA AND a.CountryA=b.CountryA AND a.ZipcodeA=b.ZipcodeA;
        CREATE TEMPORARY TABLE temp3 AS
            SELECT  a.*
              FROM  LOC AS a LEFT JOIN locMerge AS b
                ON  a.City=b.City AND a.State=b.State AND a.Country=b.Country AND a.Zipcode=b.Zipcode
             WHERE  b.Zipcode IS NULL;
        DROP TABLE IF EXISTS loc;
        CREATE TABLE loc AS SELECT * FROM temp3;
        CREATE INDEX IF NOT EXISTS loc_idxCC ON loc (City, Country);
        CREATE INDEX IF NOT EXISTS loc_idx   ON loc (City, State, Country, Zipcode);
        CREATE INDEX IF NOT EXISTS loc_idxCS ON loc (City, State);
        DROP TABLE IF EXISTS temp2;
        DROP TABLE IF EXISTS temp3;
          """)



# TODO: Unit test this so that it and the unit test can be
# eliminated in a future redesign. Also, ensure that this
# is the correct name for this function, and adjust accordingly.
def table_temp1_has_rows(conn):
    return conn.execute("SELECT count(*) FROM temp1").fetchone()[0] > 0


# TODO: Unit test extensively.
def replace_loc(script):

    # TODO: Refactor this next block
    #ALLOWS US TO REPLACE THE PREV LOC DATASET
    c.executescript("""
        DROP TABLE IF EXISTS temp1;
        CREATE TEMPORARY TABLE temp1 AS %s;
        CREATE INDEX IF NOT EXISTS tmp1_idx ON temp1 (CityA, StateA, CountryA, ZipcodeA);;
        """ % script)
    # TODO: Refactor into its own function, unit test.
    # Also, consider deleting, as these do not appear to be
    # used anywhere in the code.
    field = ["[%s]" % x[1] for x in c.execute("PRAGMA TABLE_INFO(temp1)")][2:6]
    var_f = ",".join(field)

    # TODO: Refactor into at least two functions. Main refactor is
    # Handling the body of the if block. The second refactor is
    # handling the conditional expression for the if block.
    #if c.execute("SELECT count(*) FROM temp1").fetchone()[0]>0:
    if table_temp1_has_rows(c):
        create_loc_and_locmerge_tables(c)
        VarX = c.execute("select count(*) from loc").fetchone()[0]
        VarY = c.execute("select count(*) from locMerge").fetchone()[0]
        print " - Loc =", VarX, " OkM =", VarY, " Total =", VarX+VarY, "  ", datetime.datetime.now()

    conn.commit()


print "Loc =", c.execute("select count(*) from loc").fetchone()[0]

# TODO: Refactor the range call into it's own function, unit test
# that function extensively.
for scnt in range(-1, c.execute("select max(sep_cnt(city)) from loc").fetchone()[0]+1):
    sep = scnt
    print "------", scnt, "------"

    ##DOMESTIC
    replace_loc("""
        SELECT  11,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
          FROM  loc AS a INNER JOIN usloc AS b
            ON  SEP_WRD(CityA, %d)=b.city AND StateA=b.state AND CountryA='US'
         WHERE  SEP_CNT(CityA)>=%d AND CityA!="";
        """ % (sep, scnt))

    ##DOMESTIC (Blk Remove)
    replace_loc("""
        SELECT  11,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
          FROM  loc AS a INNER JOIN usloc AS b
            ON  BLK_SPLIT(SEP_WRD(a.City, %d))=b.blkcity AND a.state=b.state AND a.country='US'
         WHERE  SEP_CNT(a.City)>=%d AND a.City!=""
        """ % (sep, scnt))

    ##DOMESTIC FIRST3 (JARO WINKLER)
    replace_loc("""
        SELECT  (10+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)), b.BlkCity)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
          FROM  loc AS a INNER JOIN usloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3)=b.City3 AND a.state=b.state AND a.country='US'
         WHERE  jaro>%s AND SEP_CNT(a.City)>=%d AND a.City!=""
      ORDER BY  a.City, a.State, jaro
        """ % (sep, sep, "10.92", scnt))

    ##DOMESTIC LAST4 (JARO WINKLER)
    replace_loc("""
        SELECT  (10+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)), b.BlkCity)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
          FROM  loc AS a INNER JOIN usloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4)=b.City4R AND a.state=b.state AND a.country='US'
         WHERE  jaro>%s AND SEP_CNT(a.City)>=%d AND a.City!=""
      ORDER BY  a.City, a.State, jaro
        """ % (sep, sep, "10.90", scnt))

    #------------------------------------------#

    ##FOREIGN COUNTRY (Full Name 1)
    replace_loc("""
        SELECT  21,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d)=b.full_name_ro AND a.country=b.cc1
         WHERE  SEP_CNT(a.City)>=%d AND a.City!=""
        """ % (sep, scnt))

    ##FOREIGN COUNTRY (Full Name 2)
    replace_loc("""
        SELECT  21,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d)=b.full_name_nd_ro AND a.country=b.cc1
         WHERE  SEP_CNT(a.City)>=%d AND a.City!="";
        """ % (sep, scnt))

    ##FOREIGN COUNTRY (Short Form)
    replace_loc("""
        SELECT  21,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d)=b.short_form AND a.country=b.cc1
         WHERE  SEP_CNT(a.City)>=%d AND a.City!="";
        """ % (sep, scnt))

    ##FOREIGN COUNTRY (Blk Split)
    replace_loc("""
        SELECT  21,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  BLK_SPLIT(SEP_WRD(a.City, %d))=b.sort_name_ro AND a.country=b.cc1
         WHERE  SEP_CNT(a.City)>=%d AND a.City!="";
        """ % (sep, scnt))

    ##FOREIGN COUNTRY FIRST3 (JARO WINKLER)
    replace_loc("""
        SELECT  (20+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)), b.sort_name_ro)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3)=b.sort_name_ro AND a.country=b.cc1
         WHERE  jaro>%s AND SEP_CNT(a.City)>=%d AND a.City!=""
      ORDER BY  a.City, a.Country, jaro;
        """ % (sep, sep, "20.92", scnt))

    ##FOREIGN COUNTRY LAST4 (JARO WINKLER)
    replace_loc("""
        SELECT  (20+jarow(BLK_SPLIT(SEP_WRD(a.City, %d)), b.sort_name_ro)) AS Jaro,
                a.cnt as cnt,
                a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
                b.full_name_nd_ro, "", b.cc1, "", b.lat, b.long
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4)=b.sort_name_ro AND a.country=b.cc1
         WHERE  jaro>%s AND SEP_CNT(a.City)>=%d AND a.City!=""
      ORDER BY  a.City, a.Country, jaro;
        """ % (sep, sep, "20.90", scnt))

####    ##DOMESTIC (State miscode to Country)
####    replace_loc("""
####        SELECT  31,
####                a.cnt, a.city, a.state, a.country, a.zipcode,
####                b.city, b.state, 'US', b.zipcode, b.lat, b.long
####          FROM  loc AS a INNER JOIN usloc AS b
####            ON  SEP_WRD(a.City, %d)=b.city AND a.country=b.state
####         WHERE  SEP_CNT(a.City)>=%d AND a.City!="";
####        """ % (sep, scnt))

### End of for loop



print "------ F ------"
##DOMESTIC (2nd LAYER)
replace_loc("""
    SELECT  15,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  usloc AS b
        ON  a.NCity=b.city AND a.NState=b.state AND a.NCountry='US';
    """)

##DOMESTIC FIRST3 (2nd, JARO WINKLER)
replace_loc("""
    SELECT  14+jarow(BLK_SPLIT(a.NCity), b.BlkCity) AS Jaro,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.city, b.state, 'US', b.zipcode, b.latitude, b.longitude
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  usloc AS b
        ON  SUBSTR(BLK_SPLIT(a.NCity),1,3)=b.City3 AND a.Nstate=b.state AND a.Ncountry='US'
     WHERE  jaro>%s
  ORDER BY  a.NCity, a.NState, jaro
    """ % "14.95")

##FOREIGN FULL NAME (2nd LAYER)
replace_loc("""
    SELECT  25,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.full_name_nd_ro, '' as state, b.cc1, '' as zip, b.lat, b.long
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  loc.gnsloc AS b
        ON  a.NCity=b.full_name_ro AND a.NCountry=b.cc1;
    """)

##FOREIGN FULL ND (2nd LAYER)
replace_loc("""
    SELECT  25,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.full_name_nd_ro, '' as state, b.cc1, '' as zip, b.lat, b.long
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  loc.gnsloc AS b
        ON  a.NCity=b.full_name_nd_ro AND a.NCountry=b.cc1;
    """)

##FOREIGN NO SPACE (2nd LAYER)
replace_loc("""
    SELECT  25,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.full_name_nd_ro, '' as state, b.cc1, '' as zip, b.lat, b.long
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  loc.gnsloc AS b
        ON  BLK_SPLIT(a.NCity)=b.sort_name_ro AND a.NCountry=b.cc1;
    """)

##FOREIGN COUNTRY FIRST3 (2nd, JARO WINKLER)
replace_loc("""
    SELECT  24+jarow(BLK_SPLIT(a.NCity), b.sort_name_ro) AS Jaro,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.full_name_nd_ro, '' as state, b.cc1, '' as zip, b.lat, b.long
      FROM  (SELECT  *
               FROM  loc
              WHERE  NCity IS NOT NULL) AS a
INNER JOIN  loc.gnsloc AS b
        ON  SUBSTR(BLK_SPLIT(a.NCity),1,3)=b.sort_name_ro AND a.Ncountry=b.cc1
     WHERE  jaro>%s
  ORDER BY  a.NCity, a.NCountry, jaro;
    """ % "24.95")

##DOMESTIC ZIPCODE
replace_loc("""
    SELECT  31,
            a.cnt as cnt,
            a.city as CityA, a.state as StateA, a.country as CountryA, a.zipcode as ZipcodeA,
            b.City, b.State, 'US', b.zipcode, b.latitude, b.longitude
      FROM  (SELECT  *, (SEP_WRD(zipcode,0)+0) as Zip2
               FROM  loc
              WHERE  Zipcode!='' AND Country='US') AS a
              INNER JOIN usloc AS b
        ON  a.Zip2=b.Zipcode;
    """)

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

conn.commit()
c.close()
conn.close()
