#!/usr/bin/env python

import unittest
import os
import sqlite3
import sys
sys.path.append( '../lib/' )
import SQLite

class TestSQLite(unittest.TestCase):

    def removeFile(self, file):
        #delete a file if it exists
        if os.path.isfile(file):
            os.system("rm {file}".format(file=file))

    def createFile(self, file, type=None, data="1,2,3"):
        #create a file db, csv
        if file.split(".")[-1] == "db" or type == "db":
            conn = sqlite3.connect(file)
            c = conn.cursor()
            c.executescript(""" 
                CREATE TABLE test (a, B, c);
                CREATE TABLE main (d, E, f);
                INSERT INTO test VALUES ({data});
                INSERT INTO main VALUES ({data});
                CREATE INDEX idx ON test (a);
                CREATE INDEX idy ON test (a, b);
                """.format(data=data)) #"""
            conn.commit()
            c.close()
            conn = sqlite3.connect(file)
        elif file.split(".")[-1] == "csv" or type == "csv":
            os.system("echo '{data}' >> {file}".\
                format(data=data, file=file))

    def setUp(self):
        self.removeFile("test.db")
        self.removeFile("test.csv")
        self.removeFile("test2.db")
        self.removeFile("test2.csv")
        # create a really basic dataset
        self.createFile(file="test.db")
        self.s = SQLite.SQLite(db="test.db", tbl="test")
        self.createFile("test2.db")
        s = SQLite.SQLite("test2.db", tbl="test")
        self.s.attach(s)

    def tearDown(self):
        self.removeFile("test.db")
        self.removeFile("test.csv")
        self.removeFile("test2.db")
        self.removeFile("test2.csv")
        self.removeFile("errlog")

    def test_keyList(self):
        #key = self.s._keyList('foo', kwargs={'tbl': 'main'})
        #print "key from test: ", key
        #key = self.s._keyList('foo', kwargs={"keys": ['bar', 'baz'], 'tbl': 'main'})
        #print "key from test: ", key
        #key = self.s._keyList('foo', kwargs={"keys": 'bar', 'tbl': 'main'})
        #print "key from test: ", key
        #key = self.s._keyList('foo', keys={"bar": 'baz'})
        #print "key from test: ", key
        key = self.s._keyList('foo', keys={"bar",'baz'})
        print "key from test: ", key
        print "key[0] from test: ", key[0]

        self.assertEquals(1,1)


if __name__ == '__main__':
    unittest.main()

