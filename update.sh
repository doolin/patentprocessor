#!/bin/bash

# PATENT_CSVFILE: location of CSV file for maintaining state
# PATENT_DOWNLOADDIR: destination of downloaded data
# PATENT_LOGFILE: destination of log file


printf "\e[31m" ;
# check that all requisite variables are set
csvfile=${PATENT_CSVFILE:?"Need to set PATENT_CSVFILE to destination of state file."}
datadir=${PATENT_DATADIR:?"Need to set PATENT_DATADIR to desired destination of downloaded files"}
logfile=${PATENT_LOGFILE:?"Need to set PATENT_LOGFILE to location of log file"}

##################################################
#
#   Function Definitions
#
##################################################
function have_file() {
  while IFS=, read col1 col2 ; do
    if [[ "$col1" == "$1" ]] ; then
      return 1
    fi
  done < $csvfile
  return 0
}

##################################################
#
#   Create state files if necessary
#
##################################################
printf "\e[34m" ;
echo "Data directory location: ${datadir}"
if [[ ! -d $datadir ]] ; then
  # create the data directory
  printf "\e[32m" ;
  echo "=> Creating ${datadir}"
  printf "\e[0m"
  mkdir -p $datadir
fi

printf "\e[34m" ;
echo "CSV file location: ${csvfile}"
if [[ ! -f $csvfile ]] ; then
  # create the CSV file
  printf "\e[32m" ;
  echo "=> Creating ${csvfile}"
  printf "\e[0m"
  touch $csvfile
fi

printf "\e[34m" ;
echo "Logfile location: ${logfile}"
if [[ ! -f $logfile ]] ; then
  # create the logfile
  printf "\e[32m" ;
  echo "=> Creating ${logfile}"
  printf "\e[0m"
  touch $logfile
fi

##################################################
#
#   Populate CSV file
#
##################################################
printf "\e[32m" ;
for file in `ls "$datadir"/*.zip`; do
  found=`ls $file | rev | cut -d'/' -f1 | rev`
  if have_file $found ; then
    echo "=> Found $found"
    echo $found,`date +"%T@%m-%d-%Y"` >> $csvfile
  fi
done
