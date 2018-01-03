#!/bin/bash
if [ -f /etc/mariachi/mariachi-ws.conf ]; then
	cp /usr/share/mariachi-data-ws/mariachi-ws.conf /etc/mariachi/mariachi-ws.conf.rpmnew
else
	mkdir -p /etc/mariachi
	cp /usr/share/mariachi-data-ws/mariachi-ws.conf /etc/mariachi/mariachi-ws.conf
fi
