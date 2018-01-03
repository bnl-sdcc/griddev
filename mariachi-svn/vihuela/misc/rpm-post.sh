#!/bin/bash
if [ -f /etc/vihuela/vihuela.conf.bak ] ; then
	cp -f /etc/vihuela/vihuela.conf /etc/vihuela/vihuela.conf.rpmnew
	cp -f /etc/vihuela/vihuela.conf.bak /etc/vihuela/vihuela.conf
fi
chmod ugo+x /etc/init.d/vihuela
/sbin/chkconfig --add vihuela