#!/bin/bash
#############################################################################
# John Weigand (11/10/2008)
#
# This script attempts to determine when Gratia updates to the APEL-WLCG 
# accounting system have stabilized for a given month.
#
# This is for the purposes of the LCG Monthly Tier 1/2 accounting reports 
# and determining if all sites are current on previous months reporting.
#
# See the usage function for more details.
#############################################################################
# Changes:
#   6/10/09 (John Weigand)
#     Needed to make a change on the selection from the log files of
#     the update DML due to the updating of OSG_CN_DATA. 
#     Previous was 'INSERT INTO'.. now 'INSERT INTO OSG_DATA'.
#     This was to keep the deltas at the site level.
#############################################################################
function logerr {
  echo "ERROR: $1"
  if [ -d "$tmpdir" ];then
    rm -rf $tmpdir
  fi
  exit 1
}
#-----------------
function determine_previous_period {
  prev_year=$(echo $curr_period | cut -d'-' -f1)
  prev_month=$(echo $curr_period | cut -d'-' -f2 |sed -e's/^0//') 
  prev_month=$(($prev_month - 1))
  if [ $prev_month -eq 0 ];then
    prev_year=$(($curr_year -1))
    prev_month=12
  fi
  prev_month=$(printf "%02d" $prev_month)
  prev_period=$prev_year-$prev_month
}
#-----------------
function write_html {
  echo "$1" >> $html_file
}
#-----------------
function start_html {
  > $html_file
  write_html "<html>
<title>Gratia - APEL/LCG Interface (Late Accounting Updates for $prev_period)</title>
<head><h2><center><b>Gratia - APEL/LCG Interface<br/> (Late Accounting Updates for $prev_period)</b></center></h2></head><body>"
  write_hr
}
#-----------------
function write_hr {
  write_html "<hr width="75%" />"
}
#-----------------
function end_html {
  write_hr
  write_html "Last update $(date) </body></html>" 
}
#-----------------
function usage {
  echo "Usage: $PGM collector_instance  [time_period]

  collector_instance - Specify the full path of the Gratia tomcat
                       instance directory.  (e.g., /data/tomcat-gratia)
                       If 'NONE' is specified, then no attempt will be
                       made to copy the html file to the collector's webapps
                       directory ($path).
                       A copy will be made in the interface logs directory
                       ($logs)

  time_period - Month (YYYY-MM) in which accounting updates are being
                performed for the previous month. 
                Default: current month which is really a scan of the 
                         previous months log files.

This script is an adjunct to the Gratia-APEL/LCG interface script LCG.py.
It's purpose is to provide some insight into when the previous months 
accounting data is complete. 

It performs this task in a crude manner by scanning the logs files
generated by LCG.py and performing a 'diff' on the daily INSERT statements
in the log file.  It then generates an html file that can be viewed easily
in a browser.  This file is  created in the logs directory of the interface
and is also copied directly into the webapps directory for the collector 
instance specified.  

The create-apel-index.sh program has been changed to look for
this output file in the format YYYY-MM.late_updates.html as well. 

This directories are currently hard-coded so if the location of the interface
software and configuration files changed, this too must change.

This should be done better in the future should this information still be
required.  For now, it provides some insight into the information needed.
"
}
#### MAIN ##########################################
PGM=$(basename $0)
path=gratia-data/interfaces/apel-lcg
logs=/home/gratia/interfaces/apel-lcg/logs
tmpdir=$logs/tmp
TOMCAT_INSTANCE=""
curr_year=$(date '+%Y')
curr_month=$(date '+%m')

curr_period=$curr_year-$curr_month

#---------------------------------
# validate command line arguments
#---------------------------------
case $1 in
 "\?"               ) usage;exit 1;;
 "-h"    | "--h"    ) usage;exit 1;;
 "-help" | "--help" ) usage;exit 1;;
esac 
    
TOMCAT_INSTANCE=$1
if [ -z "$TOMCAT_INSTANCE" ];then
  usage;logerr "The collector_instance not specified"
fi

if [ "$TOMCAT_INSTANCE" != "NONE" ];then
  if [ ! -d "$TOMCAT_INSTANCE" ];then
    logerr "The collector_instance ($TOMCAT_INSTANCE) does not exist."
  fi
  datadir=$TOMCAT_INSTANCE/webapps/$path
  if [ ! -d "$datadir" ];then
    logerr "The Gratia-APEL interface directory does not exist:  
$datadir
"
  fi
  if [ ! -w "$datadir" ];then
    logerr "The Gratia-APEL interface directory does not have the correct permissions:
$(ls -ld $datadir)
"
  fi
fi 

#-----------------------------
# get the time period
#-----------------------------
prev_period=""
if [ $# -eq 2 ];then
  curr_period=$2
fi
curr_year=$(echo $curr_period | cut -d'-' -f1)
curr_month=$(echo $curr_period | cut -d'-' -f2)

determine_previous_period

html_file=$logs/$prev_period.late_updates.html

#-----------------------
# some validation 
#-----------------------
if [ ! -d "$logs" ];then
  logerr "APEL interface log dir ($logs) does not exist"
fi

if [ ! -f "$logs/$prev_period.log" ];then
  logerr "Log file for previous month does not exist ($logs/$prev_period.log)"
fi

if [ ! -d "$(dirname $tmpdir)" ];then
  logerr "Directory for tmp dir does not exist ($(dirname $tmpdir))"
fi

#-----------------------
# make a tmp directory
#-----------------------
if [ -d "$tmpdir" ];then
  rm -rf "$tmpdir"
fi
mkdir $tmpdir
if [ "$?" != "0" ];then
  logerr " Cannot create tmp directory ($tmpdir)"
fi

#--------------------------------------
# select the data from the logs files 
#--------------------------------------
cd $logs
if [ ! -f $prev_period.log ];then
  logerr "There is no log file ($prev_period.log) in the log directory ($logs)."
fi
days=1
while
  [ $days -lt 31 ]
do
  days=$((days+1))
  day=$(printf "%02d" $days)
  tmpfile=$tmpdir/$curr_period-$day
  egrep "INSERT INTO OSG_DATA" $prev_period.log |sed -e's/INSERT INTO OSG_DATA VALUES (//'  |grep $curr_period-$day|cut -d"," -f1,2,3,4,5,6,7,8,9,12 |sort -u >$tmpfile
  if [ ! -s "$tmpfile" ];then
    rm -f $tmpfile
  fi
done
file_first=$(ls $tmpdir|head -1)
file_all="$(ls $tmpdir |sort -r)"

#---------------------
# start the diffs 
#---------------------
found_one="no"
start_html
prev_file=""
for file in $file_all
do
  if [ -z "$prev_file" ];then
    prev_file=$file;continue
  fi
  if [ "$prev_file" = "$file_first" ];then
    break
  fi

  diff_files="$prev_file $file"
  cd $tmpdir
  diff -q $diff_files >/dev/null
  if [ "$?" != 0 ];then
    found_one="yes"
    write_html "<h3>Updates on $prev_file changed from those on $file</h3><pre>"
    diff  $diff_files >>$html_file
    write_html "</pre>"
  fi
  prev_file=$file
done

if [ "$found_one" = "no" ];then
  write_html "<p><font color="green"><b>No late updates detected for this period.</b></font></p>"
fi
end_html

chmod 664 $html_file
#-----------------------------------------------
# Copy the html file to the collector directory
#-----------------------------------------------
if [ "$TOMCAT_INSTANCE" != "NONE" ];then
  cp $html_file $datadir/.
  if [ "$?" != "0" ];then
    logerr "Unable to copy $html to $datadir"
  fi
fi  

rm -rf $tmpdir
exit 0

