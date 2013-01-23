
#######################################################################################################
# geocode_replace_loc.py
# Jill Rabinowitz
# 1/18/2013
# This program consists of the SQL statement that are passed in to function replace_loc in geocode.py. 
# These statements were originally in geocode.py and have been put here both for debugging purposes and to 
# modularize the process.  Each call to replace_loc is now from the functions below.
#######################################################################################################


## DOMESTIC
def get_domestic_sql():  

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

## DOMESTIC BLOCK REMOVE
def get_loc_domestic_block_remove_sql():

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

## DOMESTIC FIRST3 JARO WINKLER
def get_loc_domestic_first3_jaro_winkler_sql():
   
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
          FROM  loc AS a INNER JOIN usloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3) = b.City3
           AND  a.state = b.state
           AND  a.country = 'US'
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ''
      ORDER BY  a.City, a.State, jaro"""

      return stmt;


## DOMESTIC LAST4 JARO WINKLER
def get_loc_domestic_last4_jaro_winkler_sql():
 
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
          FROM  loc AS a INNER JOIN usloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4) = b.City4R
           AND  a.state = b.state
           AND  a.country = 'US'
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.State, jaro"""
        
      return stmt;

## FOREIGN COUNTRY FULL NAME 1
def get_loc_foreign_country_full_name_1_sql():				# JR Code started taking longer to run at this statement
    
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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.full_name_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City!="" """
 
      return stmt;


## FOREIGN COUNTRY FULL NAME 2
def get_loc_foreign_country_full_name_2_sql():

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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.full_name_nd_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """

      return stmt;


## FOREIGN COUNTRY SHORT FORM
def get_loc_foreign_country_short_form_sql():

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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SEP_WRD(a.City, %d) = b.short_form
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """

      return stmt;


## FOREIGN COUNTRY BLOCK SPLIT
def get_loc_foreign_country_block_split_sql():  

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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  BLK_SPLIT(SEP_WRD(a.City, %d)) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  SEP_CNT(a.City) >= %d
           AND  a.City != "" """

      return stmt;

## FOREIGN COUNTRY FIRST3 JARO WINKLER
def get_loc_foreign_country_first3_jaro_winkler_sql():
 
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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  SUBSTR(BLK_SPLIT(SEP_WRD(a.City, %d)),1,3) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.Country, jaro"""
   
      return stmt;



## FOREIGN COUNTRY LAST4 JARO WINKLER
def get_loc_foreign_country_last4_jaro_winkler_sql():
 
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
          FROM  loc AS a INNER JOIN loc.gnsloc AS b
            ON  REV_WRD(BLK_SPLIT(SEP_WRD(a.City, %d)),4) = b.sort_name_ro
           AND  a.country = b.cc1
         WHERE  jaro > %s
           AND  SEP_CNT(a.City) >= %d
           AND  a.City != ""
      ORDER BY  a.City, a.Country, jaro"""

        #""" % (sep, sep, "20.90", scnt))

      return stmt;


## DOMESTIC 2ND LAYER
def get_loc_domestic_2nd_layer_sql():

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
         INNER  JOIN  usloc AS b
            ON  a.NCity = b.city
           AND  a.NState = b.state
           AND  a.NCountry = 'US'"""

      return stmt;

## DOMESTIC FIRST3 2ND JARO WINKLER
def get_loc_domestic_first3_2nd_jaro_winkler_sql():

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
         INNER  JOIN  usloc AS b
            ON  SUBSTR(BLK_SPLIT(a.NCity),1,3) = b.City3
           AND  a.Nstate = b.state
           AND  a.Ncountry ='US'
         WHERE  jaro > %s
      ORDER BY  a.NCity, a.NState, jaro"""

      return stmt;

## FOREIGN FULL NAME 2ND LAYER
def get_loc_foreign_full_name_2nd_layer_sql():

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
    INNER JOIN  loc.gnsloc AS b
            ON  a.NCity = b.full_name_ro
           AND  a.NCountry = b.cc1"""

      return stmt;


## FOREIGN FULL ND 2ND LAYER
def get_loc_foreign_full_nd_2nd_layer_sql():

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
    INNER JOIN  loc.gnsloc AS b
            ON  a.NCity = b.full_name_nd_ro
           AND  a.NCountry = b.cc1"""
  
      return stmt;


## FOREIGN NO SPACE (2nd LAYER)
def get_loc_foreign_no_space_2nd_layer_sql():

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
    INNER JOIN  loc.gnsloc AS b
            ON  BLK_SPLIT(a.NCity) = b.sort_name_ro
           AND  a.NCountry = b.cc1"""
 
      return stmt;
    

## FOREIGN COUNTRY FIRST3 (2nd, JARO WINKLER)
def get_loc_foreign_country_first3_2nd_jaro_winkler_sql():

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
    INNER JOIN  loc.gnsloc AS b
            ON  SUBSTR(BLK_SPLIT(a.NCity),1,3) = b.sort_name_ro
           AND  a.Ncountry = b.cc1
         WHERE  jaro > %s
      ORDER BY  a.NCity, a.NCountry, jaro"""

      return stmt;

## DOMESTIC ZIPCODE
def get_loc_domestic_zipcode_sql():

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
         INNER  JOIN usloc AS b
            ON  a.Zip2 = b.Zipcode"""
    
      return stmt;
