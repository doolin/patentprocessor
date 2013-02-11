#!/bin/bash

# PATENT_CSVFILE: location of CSV file for maintaining state
# PATENT_DOWNLOADDIR: destination of downloaded data
# PATENT_LOGFILE: destination of log file


# check that all requisite variables are set
csvfile=${PATENT_CSVFILE:?"Need to set PATENT_CSVFILE to destination of state file."}
datadir=${PATENT_DATADIR:?"Need to set PATENT_DATADIR to desired destination of downloaded files"}
logfile=${PATENT_LOGFILE:?"Need to set PATENT_LOGFILE to location of log file"}

p1=`date +"%Y" | cut -c3-`
p2=`date +"%m"`
p3=`date +"%d"`
most_current=$p1$p2$p3

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

function next_filename() {
  last=`echo $1 | tail -c3`
  first=`echo $1 | head -c2`
  mid=`echo $1 | head -c4 | tail -c2`
  last=$(((10#$last+1)%32))
  if [[ "$last" -eq 0 ]] ; then
    mid=$(((10#$mid + 1)%12))
    if [[ $mid -lt 10 ]] ; then
      mid=0$mid
    fi
  fi
  if [[ $last -lt 10 ]] ; then
    last=0$last
  fi
  week_id=$first$mid$last
  return 0
}

function download_next() {
  printf "\e[0m"
  week_id=`echo $1 | cut -d. -f1 | cut -c4-`
  next_filename $week_id
  until [[ $week_id > $most_current ]] ; do
    next_filename $week_id
    wget -q -P "$datadir" "http://commondatastorage.googleapis.com/patents/grant_full_text/2012/ipg${week_id}.zip"
    echo "Attempted download of ipg${week_id}.zip, max of ${most_current}" >> $logfile
  done
  printf "\e[32m" ;
  echo "=> Downloaded ipg${week_id}.zip"
  printf "\e[0m"
  echo ipg${week_id}.zip,`date +"%T@%m-%d-%Y"` >> $csvfile
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

download_next `sort $csvfile | tail -n1`
