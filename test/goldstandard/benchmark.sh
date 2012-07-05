#!/bin/sh


<<<<<<< HEAD
gawk -F, '{print $2",",$3",",$4}' < benchmark.csv > patentlist.txt
=======
gawk -F, '{print $1",", $2",",$3",",$4}' < benchmark.csv > dt5.csv

>>>>>>> 39c819113636d5908622990fdaf38898ce2912d4
#gawk -F, '{print $2}' < benchmark.csv > patentlist.txt

