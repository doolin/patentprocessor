#!/bin/bash

# First crack at building integration test framework for
# ensuring the preprocessing works correctly as we move
# forward fixing bugs, etc.

make spotless > /dev/null
mkdir -p /tmp/integration/ipg120327.one
./parse.py -d test/fixtures/xml/ -p. -x ipg120327.one.xml

for table in assignee citation class inventor lawyer patdesc patent sciref usreldoc
do
  sqlite3 -csv ${table}.sqlite3 "select * from ${table}"  > /tmp/integration/ipg120327.one/${table}.csv
  diff test/integration/parse/ipg120327.one/${table}.csv /tmp/integration/ipg120327.one/${table}.csv
done

# TODO: Refactor
make spotless > /dev/null
mkdir -p /tmp/integration/ipg120327.two
./parse.py -d test/fixtures/xml/ -p. -x ipg120327.two.xml

for table in assignee citation class inventor lawyer patdesc patent sciref usreldoc
do
  sqlite3 -csv ${table}.sqlite3 "select * from ${table}"  > /tmp/integration/ipg120327.two/${table}.csv
  diff test/integration/parse/ipg120327.two/${table}.csv /tmp/integration/ipg120327.two/${table}.csv
done


