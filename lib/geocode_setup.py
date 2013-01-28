# sets up the geocoding databases


def geocode_db_initialize(cursor):
    cursor.executescript("""
        PRAGMA CACHE_SIZE=20000;
        ATTACH DATABASE 'assignee.sqlite3' AS assigneesdb;
        ATTACH DATABASE 'inventor.sqlite3' AS inventorsdb;
        ATTACH DATABASE 'loctbl'   AS loc;
        """)


# TODO: Ensure this is the correct schema, that is, the
# schema below needs to match the schema in the existing
# loc table. If it doesn't match, we need to find out
# why, and figure out what to do about that.
def loc_create_table(cursor):
    cursor.executescript("""
     /* DROP TABLE IF EXISTS loc; */
        CREATE TABLE IF NOT EXISTS loc (
            Cnt      INTEGER,
            City     VARCHAR(10),
            State    VARCHAR(2),
            Country  VARCHAR(2),
            Zipcode  VARCHAR(5),
            City3    VARCHAR,
            NCity    VARCHAR(10),
            NState   VARCHAR(2),
            NCountry VARCHAR(2),
            UNIQUE(City,State,Country,Zipcode));

        DROP INDEX IF EXISTS loc_idxCC;
        DROP INDEX IF EXISTS loc_idx;
        DROP INDEX IF EXISTS loc_idxCS;
        DROP INDEX IF EXISTS loc_ixnCC;
        DROP INDEX IF EXISTS loc_ixn;
        DROP INDEX IF EXISTS loc_ixnCS;
        DROP INDEX IF EXISTS loc3_idxCC;
        """)


# TODO: Find a way to unit test fix_city_country
def fix_city_country(cursor):
    cursor.executescript("""
        CREATE TEMPORARY TABLE temp AS
            SELECT  Upper(City) as CityX,
                    Upper(State) as StateX,
                    Upper(Country) as CountryX,
                    count(*) as Cnt
              FROM  assigneesdb.assignee
             WHERE  City!=""
          GROUP BY  CityX, StateX, CountryX;

        CREATE TEMPORARY TABLE temp2 AS
            SELECT  sum(Cnt) as Cnt,
                    cityctry(CityX, CountryX, 'city') as CityY,
                    StateX as StateY,
                    cityctry(CityX, CountryX, 'ctry') as CtryY,
                    '' as ZipcodeY
              FROM  temp
             WHERE  CityY!=""
          GROUP BY  CityY, StateY, CtryY;

        INSERT OR REPLACE INTO loc
            SELECT  a.*,
                    SUBSTR(CityY,1,3),
                    b.NewCity,
                    b.NewState,
                    b.NewCountry
              FROM  temp2 AS a
         LEFT JOIN  loc.typos AS b
                ON  a.CityY=b.City
               AND  a.StateY=b.State
               AND  a.CtryY=b.Country;

        DROP TABLE  temp;
        DROP TABLE  temp2;
        """)

# TODO: Find a way to unit test fix_state_zip
def fix_state_zip(cursor):
    cursor.executescript("""
        CREATE TEMPORARY TABLE temp AS
            SELECT  Upper(City) as CityX,
                    Upper(State) as StateX,
                    Upper(Country) as CountryX,
                    Zipcode,
                    count(*) as Cnt
              FROM  inventorsdb.inventor
             WHERE  City!=""
                OR (City="" AND Zipcode!="")
          GROUP BY  CityX, StateX, CountryX, Zipcode;

        CREATE TEMPORARY TABLE temp2 AS
            SELECT  sum(Cnt) as Cnt,
                    cityctry(CityX, CountryX, 'city') as CityY,
                    StateX as StateY,
                    cityctry(CityX, CountryX, 'ctry') as CtryY,
                    Zipcode as ZipcodeY
              FROM  temp
             WHERE  CityY!=""
          GROUP BY  CityY, StateY, CtryY, ZipcodeY;

        INSERT OR REPLACE INTO loc
            SELECT  a.*,
                    SUBSTR(CityY,1,3),
                    b.NewCity,
                    b.NewState,
                    b.NewCountry
              FROM  temp2 AS a
         LEFT JOIN  loc.typos AS b
                ON  a.CityY=b.City
               AND  a.StateY=b.State
               AND  a.CtryY=b.Country;

        DROP TABLE  temp;
        DROP TABLE  temp2;
        """)

# TODO: Find a way to ensure that the correct indexes are created as
# the schemas change.
def create_loc_indexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS loc_idCC3 ON loc (City3,State,Country);
        CREATE INDEX IF NOT EXISTS loc_idxCC ON loc (City,Country);
        CREATE INDEX IF NOT EXISTS loc_idx   ON loc (City,State,Country,Zipcode);
        CREATE INDEX IF NOT EXISTS loc_idxCS ON loc (City,State);
        CREATE INDEX IF NOT EXISTS loc_ixnCC ON loc (NCity,NCountry);
        CREATE INDEX IF NOT EXISTS loc_ixn   ON loc (NCity,NState,NCountry);
        CREATE INDEX IF NOT EXISTS loc_ixnCS ON loc (NCity,NState);
        """)


# TODO: unit test
def create_usloc_table(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usloc AS
            SELECT  Zipcode,
                    Latitude,
                    Longitude,
                    Upper(City) as City,
                    BLK_SPLIT(Upper(City)) as BlkCity,
                    SUBSTR(UPPER(BLK_SPLIT(City)),1,3) as City3,
                    REV_WRD(BLK_SPLIT(City), 4) as City4R,
                    Upper(State) as State,
                    "US" as Country
              FROM  loc.usloc
          GROUP BY  City, State;

        CREATE INDEX If NOT EXISTS usloc_idxZ  on usloc (Zipcode);
        CREATE INDEX If NOT EXISTS usloc_idxCS on usloc (City, State);
        CREATE INDEX If NOT EXISTS usloc_idBCS on usloc (BlkCity, State);
        CREATE INDEX If NOT EXISTS usloc_idC3S on usloc (City3, State);
        CREATE INDEX If NOT EXISTS usloc_idC4R on usloc (City4R, State);

        DETACH DATABASE assigneesdb;
        DETACH DATABASE inventorsdb;

        /*DETACH DATABASE loc;
        CREATE TEMPORARY TABLE gnsloc AS
            SELECT  '' AS zipcode, lat, long,
                    UPPER(full_name_nd) AS city, "" AS State, cc1 AS country
              FROM  loc.gnsloc;
        CREATE INDEX gnsloc_idxCC on gnsloc (City, Country)
        */;
        """)


# TODO: unit test
def create_locMerge_table(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS locMerge (
            Mtch     INTEGER,
            Val      FLOAT,
            Cnt      INTEGER,
            City     VARCHAR,
            State    VARCHAR,
            Country  VARCHAR,
            Zipcode  VARCHAR,
            NCity    VARCHAR,
            NState   VARCHAR,
            NCountry VARCHAR,
            NZipcode VARCHAR,
            NLat     FLOAT,
            NLong    FLOAT,
            City3    VARCHAR,
            UNIQUE(City, State, Country, Zipcode));

        CREATE INDEX IF NOT EXISTS okM_idxCC ON locMerge (City,Country);
        CREATE INDEX IF NOT EXISTS okM_idx   ON locMerge (City,State,Country,Zipcode);
        CREATE INDEX IF NOT EXISTS okM_idxCS ON locMerge (City,State);
        CREATE INDEX IF NOT EXISTS okM_idx3  ON locMerge (City3,State,Country);
        """)


