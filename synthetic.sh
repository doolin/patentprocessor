#!/bin/sh

# WARNING: this script is almost certainly, positively
# out of date. However, the sqlite3 syntax from the command
# is almost certainly, positively still useful.

# The notion here is that we have some spreadsheet
# somewhere, say Google Docs. It could be MS Excel.
# Doesn't matter.

# What matters is we can export a csv file from that
# spreadsheet. Say, "synthetic.csv".

# schema.sql is a CREATE TABLE <tablename>
# statement in valid sql. The fields should
# correspond exactly to the column labels
# in the spreadsheet.

# Lastly, it's a known issue in SQLite that the header
# rows are not handled very nicely. If you have header
# rows in your .csv file, they are going to inserted as
# the first row of data. Thus, the statement leveraging
# SQLite's (usually) invisible and autoincrement "rowid".
# We simply delete that first row.

# TODO: replace "mybd" with $1 or something more useful.
# TODO: add argument handling to support $0, $1, etc.
# TODO: Add automatic downloading of Google Doc spreadsheet.
# TODO: Add automatic default invpat.csv export.

sqlite3 mydb.sqlite3 < schema.sql
sqlite3 -separator , mydb.sqlite3 '.import synthetic.csv invpat'
sqlite3 mydb 'delete from invpat where rowid = 1'
