#!/bin/sh

for f in test_*.py
do
echo "Processing $f file.."
python $f
done

rm -rf *.sqlite3 *.pyc
