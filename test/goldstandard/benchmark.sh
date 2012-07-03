#!/bin/sh


gawk -F, '{print $1",", $2",",$3",",$4}' < benchmark.csv > dt5.csv

#gawk -F, '{print $2}' < benchmark.csv > patentlist.txt

