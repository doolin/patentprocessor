import sys
sys.path.append( './lib/' )
import SQLite
import datetime
import shutil

t1 = datetime.datetime.now()
print "Start", t1

##Create invpat
ip = SQLite.SQLite(db = 'invpat.sqlite3', tbl = 'invpat')
ip.c.execute("DROP TABLE IF EXISTS invpat")
ip.c.execute("""CREATE TABLE invpat(Firstname TEXT, Middlename TEXT, Lastname TEXT, Street TEXT,
            City TEXT, State TEXT, Country TEXT, Zipcode TEXT, Latitude REAL,
            Longitude REAL, InvSeq INT, Patent TEXT, AppYear TEXT, ApplyYear TEXT, GYear INT,
            AppDate TEXT, Assignee TEXT, AsgNum INT, Class TEXT, Coauthor TEXT, Invnum TEXT,
            Invnum_N TEXT, Unique_Record_ID TEXT);""")

##From inventor.sqlite3: Firstname, Lastname, Street, City, State, Country, Zipcode, Latitude, Longitude, InvSeq
ip.attach('inventor.sqlite3')
ip.c.execute("""INSERT INTO invpat (Firstname, Lastname, Street, City, State, Country, Zipcode, Latitude, Longitude, Patent, InvSeq)
                SELECT Firstname, Lastname, Street, NCity, NState, NCountry, NZipcode, NLat, NLong, Patent, InvSeq FROM db.inventor_1""")
ip.detach()

##From patent.sqlite3: Patent, AppYear, GYear, AppDate
ip.attach('patent.sqlite3')
ip.merge(key = ['AppYear', 'GYear', 'AppDate'], on= ['Patent'], tableFrom = 'patent', db = 'db')
ip.detach()

##From assignee.sqlite3: Assignee, AsgNum
ip.attach('assignee.sqlite3')
ip.merge(key = [['Assignee', 'assigneeAsc'], 'AsgNum'], on = ['Patent'], tableFrom = 'assignee_1', db = 'db')
ip.detach()

##From class: class
ip.attach('class_1.sqlite3')
ip.merge(key = [['Class', 'ClassSub']], on = ['Patent'], tableFrom = 'class_1', db = 'db')
ip.detach()
ip.commit()

##Generate invnum
ip.c.execute("UPDATE invpat SET invnum = patent || '-' || invseq")
ip.c.execute("UPDATE invpat SET Invnum_N = Invnum")
ip.c.execute("UPDATE invpat SET Unique_Record_ID = Invnum")
ip.c.execute("UPDATE invpat SET Middlename = Firstname")
ip.c.execute("UPDATE invpat SET ApplyYear = AppYear")
ip.commit()

##Index invpat
ip.c.execute("CREATE INDEX idx_invpat_assignee on invpat (Assignee);")
ip.c.execute("CREATE INDEX idx_invpat_asgnum on invpat (AsgNum);")
ip.c.execute("CREATE INDEX idx_invpat_gyear on invpat (Gyear);")
ip.c.execute("CREATE INDEX idx_invpat_invnum_n  ON invpat (Invnum_N);")
ip.c.execute("CREATE INDEX idx_invpat_city on invpat (City);")
ip.c.execute("CREATE INDEX idx_invpat_city_state on invpat (City, State);")
ip.c.execute("CREATE INDEX idx_invpat_state on invpat (State);")
ip.c.execute("CREATE INDEX idx_invpat_patent ON invpat (Patent);")
ip.c.execute("CREATE INDEX idx_invpat_patent_invseq ON invpat (Patent, InvSeq);")

ip.commit()

ip.close()

print "Finish", datetime.datetime.now()-t1


#tables = ["assignee", "citation", "class", "inventor", "patent", "patdesc", "lawyer", "sciref", "usreldoc"]
#for table in tables:
#    filename = table + ".sqlite3"
#    shutil.move(filename,flder)
