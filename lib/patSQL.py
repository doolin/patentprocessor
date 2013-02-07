#!/usr/bin/env python

import sqlite3

"""
The plan is to build up a queue of commands to be executed
on each sql table. This queue should be able to be constructed
concurrently among many processes. After all patents have been
added to the queue, we can just hit "commit" on each db 
connection.
"""

class SQLTableBuilder(object):
    pass

class AssigneeSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("assignee.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS assignee (
                Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqAsg ON assignee (Patent, AsgSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO assignee VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class CitationSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("citation.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS citation (
                Patent VARCHAR(8),      Cit_Date INTEGER,       Cit_Name VARCHAR(10),
                Cit_Kind VARCHAR(1),    Cit_Country VARCHAR(2), Citation VARCHAR(8),
                Category VARCHAR(15),   CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqCit ON citation (Patent, CitSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO citation VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class ClassSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("class.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS class (
                Patent VARCHAR(8),      Prim INTEGER,
                Class VARCHAR(3),       SubClass VARCHAR(3));
            CREATE UNIQUE INDEX IF NOT EXISTS uqClass ON class (Patent, Class, SubClass);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO class VALUES \
            (?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class InventorSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("inventor.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS inventor (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                Street VARCHAR(15),     City VARCHAR(10),
                State VARCHAR(2),       Country VARCHAR(12),
                Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqInv ON inventor (Patent, InvSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO inventor VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class PatentSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("patent.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS patent (
                Patent VARCHAR(8),      Kind VARCHAR(3),        Claims INTEGER,
                AppType INTEGER,        AppNum VARCHAR(8),
                GDate INTEGER,          GYear INTEGER,
                AppDate INTEGER,        AppYear INTEGER, PatType VARCHAR(15) );
            CREATE UNIQUE INDEX IF NOT EXISTS uqPat on patent (Patent);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO patent VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class PatdescSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("patdesc.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS patdesc (
                Patent VARCHAR(8),
                Abstract VARCHAR(50),   Title VARCHAR(20));
            CREATE UNIQUE INDEX IF NOT EXISTS uqPatDesc ON patdesc (Patent);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO patdesc VALUES \
            (?, ?, ?)""", self.inserts)
        self.conn.commit()

class LawyerSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("lawyer.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS lawyer (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                LawCountry VARCHAR(2),  OrgName VARCHAR(20),    LawSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqLawyer ON lawyer (Patent, LawSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO lawyer VALUES \
            (?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

class ScirefSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("sciref.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS sciref (
                Patent VARCHAR(8),      Descrip VARCHAR(20),    CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqSciref ON sciref (Patent, CitSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO sciref VALUES \
            (?, ?, ?)""", self.inserts)
        self.conn.commit()

class UsreldocSQL(SQLTableBuilder):
    def __init__(self):
        self.conn = sqlite3.connect("usreldoc.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS usreldoc (
                Patent VARCHAR(8),      DocType VARCHAR(10),    OrderSeq INTEGER,
                Country VARCHAR(2),     RelPatent VARCHAR(8),   Kind VARCHAR(2),
                RelDate INTEGER,        Status VARCHAR(10));
            CREATE UNIQUE INDEX IF NOT EXISTS uqUSRelDoc ON usreldoc (Patent, OrderSeq);
            """)
        self.inserts = []

    def commit(self):
        self.cursor.executemany("""INSERT OR IGNORE INTO usreldoc VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?)""", self.inserts)
        self.conn.commit()

assignee_table = AssigneeSQL()
citation_table = CitationSQL()
class_table = ClassSQL()
inventor_table = InventorSQL()
patent_table = PatentSQL()
patdesc_table = PatdescSQL()
lawyer_table = LawyerSQL()
sciref_table = ScirefSQL()
usreldoc_table = UsreldocSQL()
