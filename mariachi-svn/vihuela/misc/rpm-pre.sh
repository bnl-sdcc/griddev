#!/bin/bash
if [ -f /etc/vihuela/vihuela.conf ] ; then
	cp -f /etc/vihuela/vihuela.conf /etc/vihuela/vihuela.conf.bak
fi