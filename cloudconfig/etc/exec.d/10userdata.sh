#!/bin/bash
# 
# If a metadata server exists, pull in data, overriding 
# defaults in /etc/cloudconfig/userdata
#
LOGFILE=/var/log/cloudconfig.log

[ -f /etc/sysconfig/cloudconfig ] && . /etc/sysconfig/cloudconfig
[ -f /etc/cloudconfig/conf.d/userdata.conf ] && . /etc/cloudconfig/conf.d/userdata.conf

d=`date`
echo "Handling userdata..." >> $LOGFILE 

PYVER=`python -V 2>&1  | awk '{ print $2 }'  |  grep -o "[[:digit:]+]\.[[:digit:]]" `
#echo $PYVER
RPMEXE=/usr/lib/python$PYVER/site-packages/cloudconfig/userdata.py

if [ -f $RPMEXE ]; then
	python $RPMEXE $UDROOT >> $LOGFILE
else
	echo "No suitable userdata executable found."
fi

d=`date`
echo "Done: $d"
echo "Done: $d" >> $LOGFILE 