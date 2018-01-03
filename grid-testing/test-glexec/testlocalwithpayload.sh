#!/bin/bash
VDT_LOCATION=/usr/local/OSG_WN_Client

GLEXEC=`find $VDT_LOCATION -name glexec`
WHOAMI=`which whoami`
IDEXE=`which id`
PAYLOAD=$PWD/payload.sh

echo "HOME is $HOME"
echo "PWD is $PWD"
echo "GLEXEC is $GLEXEC"
echo "VDT_LOCATION is $VDT_LOCATION"
echo "WHOAMI is $WHOAMI"
echo "IDEXE is $IDEXE"


. $VDT_LOCATION/setup.sh


voms-proxy-init -userconf ~/.glite/vomses -voms atlas:/atlas/usatlas
voms-proxy-info -all

PROXYFILE=`voms-proxy-info -path` 
echo "PROXYFILE is $PROXYFILE"

echo "Copying payload proxy to other file..."
NEWFILE=`mktemp`

cp -p $PROXYFILE $NEWFILE

FILEBASE=`basename $NEWFILE`

export GLEXEC_CLIENT_CERT=$NEWFILE
echo "GLEXEC_CLIENT_CERT is $GLEXEC_CLIENT_CERT"

CMDTORUN="$GLEXEC $PAYLOAD"

$CMDTORUN
