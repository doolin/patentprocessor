#!/bin/bash

# Integration testing for the clean.py script

##### Two rows

make spotless > /dev/null
./parse.py -d test/fixtures/xml/ -p. -x ipg120327.two.xml
mkdir -p /tmp/integration/ipg120327.two


echo Starting clean...
python clean.py

echo Starting diffs...
for table in inventor inventor_1
do
  sqlite3 inventor.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.two/${table}.csv
  `diff test/integration/clean/ipg120327.two/${table}.csv /tmp/integration/ipg120327.two/${table}.csv`
done

for table in assignee assignee_1 grp wrd
do
  sqlite3 assignee.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.two/${table}.csv
  `diff test/integration/clean/ipg120327.two/${table}.csv /tmp/integration/ipg120327.two/${table}.csv`
done

for table in patent
do
  sqlite3 patent.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.two/${table}.csv
  `diff test/integration/clean/ipg120327.two/${table}.csv /tmp/integration/ipg120327.two/${table}.csv`
done


#### 18 rows

make spotless > /dev/null
./parse.py -d test/fixtures/xml/ -p. -x ipg120327.18.xml
mkdir -p /tmp/integration/ipg120327.18

echo Starting clean...
python clean.py

echo Starting diffs...
for table in inventor inventor_1
do
  sqlite3 inventor.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.18/${table}.csv
  `diff test/integration/clean/ipg120327.18/${table}.csv /tmp/integration/ipg120327.18/${table}.csv`
done

for table in assignee assignee_1 grp wrd
do
  sqlite3 assignee.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.18/${table}.csv
  `diff test/integration/clean/ipg120327.18/${table}.csv /tmp/integration/ipg120327.18/${table}.csv`
done

for table in patent
do
  sqlite3 patent.sqlite3 -csv "select * from ${table}"  > /tmp/integration/ipg120327.18/${table}.csv
  `diff test/integration/clean/ipg120327.18/${table}.csv /tmp/integration/ipg120327.18/${table}.csv`
done


