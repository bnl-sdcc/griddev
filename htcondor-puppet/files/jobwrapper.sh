#!/bin/bash -l
#
# Condor startd jobwrapper
# Executes using bash -l, so that all /etc/profile.d/*.sh scripts are sourced. 
#
THISUSER=`/usr/bin/whoami`
export HOME=`getent passwd $THISUSER | awk -F : '{print $6}'`
exec "$@"
