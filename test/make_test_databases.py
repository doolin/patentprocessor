#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import sqlite3
import csv

def make_assignee_db():
    conn = sqlite3.connect("assignee.sqlite3")
    f = open('../schemas/assignee.sql', 'r')
    schema = f.read()
    c = conn.cursor()
    c.executescript(schema)
    csvfile = open("./integration/parse/ipg120327.two/assignee.csv", 'r')
    assignees = csv.reader(csvfile)
    for a in assignees:
        c.execute('INSERT INTO assignee VALUES (?,?,?,?,?,?,?,?,?)', a )
    csvfile.close()
    conn.commit()
    conn.close()

def make_inventor_db():
    conn = sqlite3.connect("inventor.sqlite3")
    f = open('../schemas/inventor.sql', 'r')
    schema = f.read()
    c = conn.cursor()
    c.executescript(schema)
    csvfile = open("./integration/parse/ipg120327.two/inventor.csv", 'r')
    inventors = csv.reader(csvfile)
    for i in inventors:
        c.execute('INSERT INTO inventor VALUES (?,?,?,?,?,?,?,?,?,?)', i )
    csvfile.close()
    conn.commit()
    conn.close()
