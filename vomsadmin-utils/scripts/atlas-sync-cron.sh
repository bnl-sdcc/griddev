#!/bin/bash
LOGFILE=~/var/log/voms-update.log
BINPATH=~/bin
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
echo "******************************" >> $LOGFILE 2>&1
date >> $LOGFILE
$BINPATH/vomsadmin-util -c ~/etc/vomsadmin.conf -d -f atlas-voms.cern.ch -t atlas-vo.racf.bnl.gov >> $LOGFILE 2>&1
d=`date`
echo "Synchronization ran at $d" >> $LOGFILE 2>&1
