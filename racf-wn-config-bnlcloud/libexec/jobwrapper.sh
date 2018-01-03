#!/bin/bash -l
#
# Invoke Condor jobs with bash -l to get normal environment
#
THISUSER=`/usr/bin/whoami`
export HOME=`getent passwd $THISUSER | awk -F : '{print $6}'`
exec "$@" 
