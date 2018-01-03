#!/bin/bash
#
# start|restart|graceful|stop|graceful-stop
#
#
HTTPD=/usr/sbin/httpd
CONFFILE=/home/jhover/devel/mod-python-template/config/httpd/conf/httpd.conf

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

