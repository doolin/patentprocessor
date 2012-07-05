#!/bin/sh

for f in test_*.py
do
echo "Processing $f file.."
python $f
done
