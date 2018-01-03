#!/bin/bash
#
# userinit	Script to run user-level init scripts
#
# Author:       John R. Hover <jhover@bnl.gov>
#
#
# chkconfig: 345 26 74
# description: Starts and stops user init scripts.
# processname: userinit


if [ -f /etc/sysconfig/userinit ]; then
        . /etc/sysconfig/userinit
fi

# Source function library.
. /etc/rc.d/init.d/functions

RETVAL=0


#
# See how we were called.
#

doscript() {
    USERDIRS=`ls $USERINIT_HOMEROOT`
    for dir in $USERDIRS ; do
       initdir=$USERINIT_HOMEROOT/$dir$USERINIT_INITDIR
       if [ -d "$initdir" ] ; then
           echo "Running scripts in $initdir..."
           cd "$initdir"
           EXECUTABLES=`find . -maxdepth 1 -type f -perm /u=x,g=x,o=x`
           for exescript in $EXECUTABLES ; do
               echo "Executing $exescript in $initdir:"
               useruid=`ls -ln $exescript |  awk '{ print $3}'`
               #echo "sudo -u #$useruid $exescript $1"
               sudo -u \#$useruid $exescript $1
           done    
       fi
    done
}


start() {
	# Check that we're a privileged user
	[ `id -u` = 0 ] || exit 4

    echo "Starting user init scripts:  "	
	doscript start
    RETVAL=$?
	return $RETVAL
}

stop() {
	echo $"Stopping user init scripts: "
	doscript stop
	RETVAL=$?
	return $RETVAL
}


restart() {
	stop
	start
}	


case "$1" in
start)
	start
	;;
stop)
	stop
	;;
restart)
	restart
	;;
*)
	echo $"Usage: $0 {start|stop|restart}"
	RETVAL=2
esac

exit $RETVAL
