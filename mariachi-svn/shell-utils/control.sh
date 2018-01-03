#!/bin/bash
echo "Top level program"
./proggie.sh &
sleep 30
proggiepid=`ps | grep proggie | grep -v grep | awk '{print $1}'`
echo "Proggie PID is $proggiepid"
kill -9 $proggiepid

