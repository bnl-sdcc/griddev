#!/bin/bash
#
# start|restart|graceful|stop|graceful-stop
#
#

HTTPDROOT=/home/jhover/devel/interdash/config/httpd
HTTPD=/usr/sbin/httpd
CONFFILE=$HTTPDROOT/conf/httpd.conf

if [ ! -d $HTTPDROOT/logs ]; then
	echo "Creating logs directory..."
	mkdir $HTTPDROOT/logs
fi

if [ ! -d $HTTPDROOT/run ]; then
	echo "Creating run directory..."
	mkdir $HTTPDROOT/run
fi

if [ ! -h $HTTPDROOT/modules ]; then
	echo "Linking to system modules directory..."
	cd $HTTPDROOT
	ln -s /usr/lib/httpd/modules
	cd -
fi

case "$1" in
  start)
        $HTTPD -f $CONFFILE -k start
        ;;
  stop)
          $HTTPD -f $CONFFILE -k stop
        ;;
  restart)
		  $HTTPD -f $CONFFILE -k restart
        ;;

  *)
        echo $"Usage: init.sh {start|stop|restart|}"
        exit 1
      
esac