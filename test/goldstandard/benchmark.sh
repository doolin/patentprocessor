#!/bin/sh


# gawk -F, '{print $2",",$3",",$4}' < benchmark.csv
gawk -F, '{print $2}' < benchmark.csv > patentlist.txt

