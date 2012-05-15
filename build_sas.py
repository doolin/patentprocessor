# US LOC
# http://geonames.usgs.gov/domestic/download_data.htm
# http://geonames.usgs.gov/docs/stategaz/NationalFile_20120204.zip

import datetime, csv, os, re, sqlite3, unicodedata
from locFunc import uniasc, cityctry

conn = sqlite3.connect("loctbl.sqlite3")
c = conn.cursor()

flderUS = "/var/share/patentdata/Typos/SAS"
fnameUS = [x for x in os.listdir(flderUS) if re.search(r'[.]csv', x, re.I)!=None]

c.executescript("""
    CREATE TABLE IF NOT EXISTS usloc (
        Zipcode INTEGER,
        Lat FLOAT,          Long FLOAT,
        City VARCHAR(10),   State VARCHAR(2),
        StateName VARCHAR(10),
        UNIQUE(Zipcode, City, State));
    CREATE INDEX IF NOT EXISTS uidx_all ON usloc (Zipcode, City, State);
    CREATE INDEX IF NOT EXISTS uidx_zip ON usloc (Zipcode);
    CREATE INDEX IF NOT EXISTS uidx_cty ON usloc (City);
    CREATE INDEX IF NOT EXISTS uidx_st  ON usloc (State);
    """)

for x in fnameUS:
    c.executemany("INSERT OR REPLACE INTO usloc VALUES (?,?,?,?,?,?)", 
            [x for x in csv.reader(open("%s/%s" % (flderUS, x), "r"))][1:])


# TYPOS
typos = [[cityctry(x[0], x[2]), x[1], cityctry(x[0], x[2], ret="ctry"),
          uniasc(unicode(x[3], "latin-1")).upper(), x[4], x[5]]
         #for x in csv.reader(open("Typos\Typos.csv", "rb"))][1:]
         for x in csv.reader(open("/var/share/patentdata/Typos/typos.csv", "rb"))][1:]

c.executescript("""
    DROP TABLE IF EXISTS typos;
    CREATE TABLE IF NOT EXISTS typos (
        City VARCHAR,       State VARCHAR,      Country VARCHAR,
        NewCity VARCHAR,    NewState VARCHAR,   NewCountry VARCHAR,
        UNIQUE(City, State, Country));
    CREATE INDEX IF NOT EXISTS typos_all   ON typos (City, State, Country);
    CREATE INDEX IF NOT EXISTS typos_ctry  ON typos (Country);
    CREATE INDEX IF NOT EXISTS typos_ctate ON typos (City, State);
    CREATE INDEX IF NOT EXISTS typos_cctry ON typos (City, Country);
    """)
c.executemany("INSERT OR REPLACE INTO typos VALUES (?, ?, ?, ?, ?, ?)", typos)

conn.commit()
c.close()
conn.close()
