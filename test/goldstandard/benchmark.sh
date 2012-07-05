#!/bin/sh


gawk -F, '{print $2",",$3",",$4}' < benchmark.csv > patentlist.txt
#gawk -F, '{print $2}' < benchmark.csv > patentlist.txt

