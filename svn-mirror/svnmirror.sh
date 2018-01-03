#!/bin/bash
SVNURL=http://www.usatlas.bnl.gov/svn/panda
LOCALROOT=/home/jhover/tmp
WEBROOT=/home/jhover/tmp/pandaroot

echo "cd $LOCALROOT"
cd $LOCALROOT

TMPDIR=mktemp -d $LOCALROOT/panda.XXX



SVNCMD="svn co $SVNURL $TMPDIR"

echo "Executing command: $SVNCMD"
svn co $SVNURL

RETVAL=$?
echo "Return value is $RETVAL"

if [ $RETVAL -eq 0 ] ; then
    	
else

fi