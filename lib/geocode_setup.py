# sets up the geocoding databases

# Bring in one function at a time.

# TODO: Find a way to unit test fix_city_country
def fix_city_country(conn):
    conn.executescript("""
        CREATE TEMPORARY TABLE temp AS
            SELECT  Upper(City) as CityX, Upper(State) as StateX,
                    Upper(Country) as CountryX, count(*) as Cnt
              FROM  asg.assignee
             WHERE  City!=""
          GROUP BY  CityX, StateX, CountryX;
        CREATE TEMPORARY TABLE temp2 AS
            SELECT  sum(Cnt) as Cnt,
                    cityctry(CityX, CountryX, 'city') as CityY, StateX as StateY,
                    cityctry(CityX, CountryX, 'ctry') as CtryY, '' as ZipcodeY
              FROM  temp
             WHERE  CityY!=""
          GROUP BY  CityY, StateY, CtryY;
        INSERT OR REPLACE INTO loc
            SELECT  a.*, SUBSTR(CityY,1,3), b.NewCity, b.NewState, b.NewCountry
              FROM  temp2 AS a
         LEFT JOIN  loc.typos AS b
                ON  a.CityY=b.City AND a.StateY=b.State AND a.CtryY=b.Country;
        DROP TABLE  temp;
        DROP TABLE  temp2;
        """)

# TODO: Find a way to unit test fix_state_zip
def fix_state_zip(conn):
    conn.executescript("""
        CREATE TEMPORARY TABLE temp AS
            SELECT  Upper(City) as CityX, Upper(State) as StateX,
                    Upper(Country) as CountryX, Zipcode, count(*) as Cnt
              FROM  inv.inventor
             WHERE  City!="" OR (City="" AND Zipcode!="")
          GROUP BY  CityX, StateX, CountryX, Zipcode;
        CREATE TEMPORARY TABLE temp2 AS
            SELECT  sum(Cnt) as Cnt,
                    cityctry(CityX, CountryX, 'city') as CityY, StateX as StateY,
                    cityctry(CityX, CountryX, 'ctry') as CtryY, Zipcode as ZipcodeY
              FROM  temp
             WHERE  CityY!=""
          GROUP BY  CityY, StateY, CtryY, ZipcodeY;
        INSERT OR REPLACE INTO loc
            SELECT  a.*, SUBSTR(CityY,1,3), b.NewCity, b.NewState, b.NewCountry
              FROM  temp2 AS a
         LEFT JOIN  loc.typos AS b
                ON  a.CityY=b.City AND a.StateY=b.State AND a.CtryY=b.Country;
        DROP TABLE  temp;
        DROP TABLE  temp2;
        """)


