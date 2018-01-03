#!/bin/bash
TUN_CMD="ssh -f mariachi-with-tunnel"
ALIVE_CMD="ping -i 15 127.0.0.1"
TUNNEL_COMMAND="$TUN_CMD \"$ALIVE_CMD\" > /dev/null"
PROFILE_NAME=mariachi-with-tunnel

n=`ps aux | grep $PROFILE_NAME | grep -v grep`
D=`date`
if [ "x$n" == "x" ]; then
        echo "[$D] No tunnel running. Executing $TUNNEL_COMMAND"
        eval $TUNNEL_COMMAND
else
        echo "[$D] Tunnel running. Exitting."
fi
