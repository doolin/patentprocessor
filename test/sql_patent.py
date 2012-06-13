from xml.dom import minidom
from types import *
import datetime, csv, os, re, sqlite3
import copy


class SQLPatent:

    def dbBuild(self, q, tbl, week=0, legacy=True):
##        if legacy:
##            table = os.path.isfile(tbl+"_l.sqlite3")
##            conn = sqlite3.connect(tbl+"_l.sqlite3")
##        else:
        table = os.path.isfile("%s.sqlite3" % tbl)
        conn = sqlite3.connect("%s.sqlite3" % tbl)
        c = conn.cursor()
        ##c.execute("PRAGMA synchronous = 0")
        self.dbTbl(tbl=tbl, c=c, legacy=legacy)

        if c.execute("SELECT count(*) FROM gXML WHERE week=?", (week,)).fetchone()[0]==0:
            #INSERT STUFF
            if tbl=="assignee":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""" % tbl, q)
                # q is the list of lists
            elif tbl=="citation":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" % tbl, q)
            elif tbl=="class":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?)""" % tbl, q)
            elif tbl=="inventor":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" % tbl, q)
            elif tbl=="patent":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" % tbl, q) #add one more ?
            elif tbl=="patdesc":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?)""" % tbl, q)
            elif tbl=="lawyer":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?)""" % tbl, q)
            elif tbl=="sciref":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?)""" % tbl, q)
            elif tbl=="usreldoc":
                c.executemany("""INSERT OR IGNORE INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" % tbl, q)
            c.execute("INSERT INTO gXML VALUES (?)", (week,))

        conn.commit()
        c=None
        conn=None

    def dbFinal(self, tbl, legacy=True):
        conn = sqlite3.connect("%s.sqlite3" % tbl)
        c = conn.cursor()

        if tbl=="assignee":
##            c.execute("CREATE INDEX IF NOT EXISTS idx_pata ON %s (Patent, AsgSeq)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_asg    ON %s (Assignee)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_asgtyp ON %s (AsgType)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_stt ON %s (State)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_cty ON %s (Country)" % tbl)

        elif tbl=="citation":
##            print "[citation] to be continued..."
            c.execute("CREATE INDEX IF NOT EXISTS idx_patc ON %s (Patent, Citation)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_cit ON %s (Citation)" % tbl)

        elif tbl=="class":
##            c.execute("CREATE INDEX IF NOT EXISTS idx_patcs ON %s (Patent, Class, SubClass)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_prim ON %s (Prim)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_cls  ON %s (Class)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_scls ON %s (SubClass)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_cscl ON %s (Class,SubClass)" % tbl)

        elif tbl=="inventor":
##            c.execute("CREATE INDEX IF NOT EXISTS idx_pati ON %s (Patent, InvSeq)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_stt ON %s (State)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_cty ON %s (Country)" % tbl)

        elif tbl=="patent":
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_ayr ON %s (AppYear)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_gyr ON %s (GYear)" % tbl)

        elif tbl=="patdesc":
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)

        elif tbl=="lawyer":
            c.execute("CREATE INDEX IF NOT EXISTS idx_patl ON %s (Patent, LawSeq)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)

        elif tbl=="sciref":
##            c.execute("CREATE INDEX IF NOT EXISTS idx_patc ON %s (Patent, CitSeq)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)

        elif tbl=="usreldoc":
##            c.execute("CREATE INDEX IF NOT EXISTS idx_pator ON %s (Patent, OrderSeq, RelPatent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_patent ON %s (Patent)" % tbl)
            c.execute("CREATE INDEX IF NOT EXISTS idx_relpat ON %s (RelPatent)" % tbl)

        c.close()
        conn.close()


    def dbTbl(self, tbl, c, legacy=True):

        c.execute("CREATE TABLE IF NOT EXISTS gXML ( week VARCHAR )")

        if tbl=="assignee":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS assignee (
                    Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                    City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                    Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER);
                CREATE UNIQUE INDEX IF NOT EXISTS uqAsg ON assignee (Patent, AsgSeq);
                DROP INDEX IF EXISTS idx_pata;
                DROP INDEX IF EXISTS idx_patent;
                DROP INDEX IF EXISTS idx_asgtyp;
                DROP INDEX IF EXISTS idx_stt;
                DROP INDEX IF EXISTS idx_cty;
                """)

        elif tbl=="citation":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS citation (
                    Patent VARCHAR(8),      Cit_Date INTEGER,       Cit_Name VARCHAR(10),
                    Cit_Kind VARCHAR(1),    Cit_Country VARCHAR(2), Citation VARCHAR(8),
                    Category VARCHAR(15),   CitSeq INTEGER);
                CREATE UNIQUE INDEX IF NOT EXISTS uqCit ON citation (Patent, CitSeq);
                DROP INDEX IF EXISTS idx_patc;
                DROP INDEX IF EXISTS idx_patent;
                DROP INDEX IF EXISTS idx_cit;
                """)

        elif tbl=="class":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS class (
                    Patent VARCHAR(8),      Prim INTEGER,
                    Class VARCHAR(3),       SubClass VARCHAR(3));
                CREATE UNIQUE INDEX IF NOT EXISTS uqClass ON class (Patent, Class, SubClass);
                DROP INDEX IF EXISTS idx_patcs;
                DROP INDEX IF EXISTS idx_patent;
                DROP INDEX IF EXISTS idx_prim;
                """)

        elif tbl=="inventor":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS inventor (
                    Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                    Street VARCHAR(15),     City VARCHAR(10),
                    State VARCHAR(2),       Country VARCHAR(12),
                    Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER);
                CREATE UNIQUE INDEX IF NOT EXISTS uqInv ON inventor (Patent, InvSeq);
                DROP INDEX IF EXISTS idx_pati;
                DROP INDEX IF EXISTS idx_patent;
                DROP INDEX IF EXISTS idx_stt;
                DROP INDEX IF EXISTS idx_cty;
                """)

        elif tbl=="patent": #add PatType VARCHAR(15)
            c.executescript("""
                CREATE TABLE IF NOT EXISTS patent (
                    Patent VARCHAR(8),      Kind VARCHAR(3),        Claims INTEGER,
                    AppType INTEGER,        AppNum VARCHAR(8),
                    GDate INTEGER,          GYear INTEGER,
                    AppDate INTEGER,        AppYear INTEGER, PatType VARCHAR(15) );
                CREATE UNIQUE INDEX IF NOT EXISTS uqPat on patent (Patent);
                DROP INDEX IF EXISTS idx_patent;
                DROP INDEX IF EXISTS idx_ayr;
                DROP INDEX IF EXISTS idx_gyr;
                """)

        elif tbl=="patdesc":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS patdesc (
                    Patent VARCHAR(8),
                    Abstract VARCHAR(50),   Title VARCHAR(20));
                CREATE UNIQUE INDEX IF NOT EXISTS uqPatDesc ON patdesc (Patent);
                DROP INDEX IF EXISTS idx_patent;
                """)

        elif tbl=="lawyer":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS lawyer (
                    Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                    LawCountry VARCHAR(2),  OrgName VARCHAR(20),    LawSeq INTEGER);
                CREATE UNIQUE INDEX IF NOT EXISTS uqLawyer ON lawyer (Patent, LawSeq);
                DROP INDEX IF EXISTS idx_patl;
                DROP INDEX IF EXISTS idx_patent;
                """)

        elif tbl=="sciref":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS sciref (
                    Patent VARCHAR(8),      Descrip VARCHAR(20),    CitSeq INTEGER);
                CREATE UNIQUE INDEX IF NOT EXISTS uqSciref ON sciref (Patent, CitSeq);
                DROP INDEX IF EXISTS idx_patc;
                DROP INDEX IF EXISTS idx_patent;
                """)

        elif tbl=="usreldoc":
            c.executescript("""
                CREATE TABLE IF NOT EXISTS usreldoc (
                    Patent VARCHAR(8),      DocType VARCHAR(10),    OrderSeq INTEGER,
                    Country VARCHAR(2),     RelPatent VARCHAR(8),   Kind VARCHAR(2),
                    RelDate INTEGER,        Status VARCHAR(10));
                CREATE UNIQUE INDEX IF NOT EXISTS uqUSRelDoc ON usreldoc (Patent, OrderSeq);
                DROP INDEX IF EXISTS idx_pator;
                DROP INDEX IF EXISTS idx_patent;
                """)


    def tblBuild(self, patents, tbl, legacy=True):
        q = [] # creating the list of lists

        for x in patents:

            if tbl=="assignee":
                for i,y in enumerate(x.asg_list):
                    if y[0]==0:
                        q.extend([[x.patent, y[2], y[1], y[4], y[5], y[6], y[7], y[8], i]])
                    else:
                        q.extend([[x.patent, "00", "%s, %s" % (y[2], y[1]), y[4], y[5], y[6], y[7], y[8], i]])

            elif tbl=="citation":
                cit_list = [y for y in x.cit_list if y[1]!=""]
                for i,y in enumerate(cit_list):
                    q.extend([[x.patent, y[3], y[5], y[4], y[1], y[2], y[0], i]])

            elif tbl=="class":
                for i,y in enumerate(x.classes):
                    q.extend([[x.patent, (i==0)*1, y[0], y[1]]])

            elif tbl=="inventor":
                for i,y in enumerate(x.inv_list):
                    q.extend([[x.patent, y[1], y[0], y[2], y[3], y[4], y[5], y[6], y[8], i]])

            elif tbl=="patent":
                q.extend([[x.patent, x.kind, x.clm_num, x.code_app, x.patent_app, x.date_grant, x.date_grant[:4], x.date_app, x.date_app[:4], x.pat_type]]) #add x.pat_type

            elif tbl=="patdesc":
                q.extend([[x.patent, x.abstract, x.invention_title]])

            elif tbl=="lawyer":
                print "reached lawyer"
                for i,y in enumerate(x.law_list):
                    q.extend([[x.patent, y[1], y[0], y[2], y[3], i]])

            elif tbl=="sciref":
                cit_list = [y for y in x.cit_list if y[1]==""]
                for i,y in enumerate(cit_list):
                    q.extend([[x.patent, y[-1], i]])

            elif tbl=="usreldoc":
                for i,y in enumerate(x.rel_list):
                    if y[1]==1:
                        q.extend([[x.patent, y[0], y[1], y[3], y[2], y[4], y[5], y[6]]])
                    else:
                        q.extend([[x.patent, y[0], y[1], y[3], y[2], y[4], "", ""]])

        return q
