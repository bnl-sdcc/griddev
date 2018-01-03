#!/bin/bash
function clean_up {

	# Perform program exit housekeeping
	echo "In clean_up. Signalling subprocess."
	ps aux | grep wrapper.py | grep -v grep | awk {'print $2'} | xargs kill -s 10
	echo "Tried to send signal." 
	exit
}

trap clean_up SIGUSR1

echo "wrapper.sh: starting..."
while true; do
	sleep 5
	echo "wrapper.sh sleeping..."
	# Do nothing
done