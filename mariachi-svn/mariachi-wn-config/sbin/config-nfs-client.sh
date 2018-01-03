#!/bin/bash
FSTAB_TEMPLATE=/usr/share/mariachi-wn-config/fstab.template
FSTAB=/etc/fstab
IDMAPD_TEMPLATE=/usr/share/mariachi-wn-config/idmapd.conf.template
IFS=;
SIGNAL=mariachi.stonybrook.edu
DEBUG=0

ensure_fstab_line() {
	local LINE
	LINE=$1	
	LGREP=`grep $SIGNAL $FSTAB`
	if [ $DEBUG = 1 ]; then
		echo "Guaranteeing line..."
		echo "$LINE"
		echo "... in /etc/fstab"
		echo "grep $SIGNAL $FSTAB"
		echo "LGREP is $LGREP"
	fi
	if [ "${LGREP}X" == "X" ]; then
		#echo "Adding line..."
		cat $FSTAB_TEMPLATE >> $FSTAB
	#else
		#echo "Line already there..."
	fi	 	
}


remove_fstab_line() {
	local LINE
	LINE=$1
	LGREP=`grep $SIGNAL $FSTAB`
	if [ $DEBUG = 1 ]; then	
		echo "Guaranteeing line..."
		echo "$LINE"
		echo "...not in /etc/fstab"
		echo "grep $SIGNAL $FSTAB"
		echo "LGREP is $LGREP"
	fi
	if [ ! "${LGREP}X" == "X" ]; then
		#echo "Line present. Removing..."
		cp $FSTAB /etc/fstab.bak
		cat $FSTAB | grep -v $SIGNAL > /etc/fstab.new
		mv /etc/fstab.new /etc/fstab
	fi
}


case $1 in
		--on)
		chkconfig --level 0123456 portmap off
		chkconfig --level 345 portmap on
		chkconfig --level 0123456 rpcidmapd off
		chkconfig --level 345 rpcidmapd on
		chkconfig --level 0123456 nfslock off
		chkconfig --level 0123456 nfs off
		chkconfig --level 0123456 rpcgssd off
		chkconfig --level 0123456 rpcsvcgssd off
		/etc/init.d/nfslock stop
		/etc/init.d/nfs stop
		/etc/init.d/rpcgssd stop
		/etc/init.d/rpcsvcgssd stop
		/etc/init.d/portmap restart
		/etc/init.d/rpcidmapd restart
		;;

		--off)
		chkconfig  portmap off
		chkconfig rpcidmapd off
		/etc/init.d/portmap stop
		/etc/init.d/rpcidmapd stop
		;;

		--fstabadd)
		if [ -r $FSTAB_TEMPLATE ]; then
			read ENTRY < $FSTAB_TEMPLATE
			#echo "ENTRY is $ENTRY"
			ensure_fstab_line "$ENTRY"
		fi
		
		;;
		
		--fstabremove)
		if [ -r $FSTAB_TEMPLATE ]; then
			read ENTRY < $FSTAB_TEMPLATE
			#echo "ENTRY is $ENTRY"
			remove_fstab_line "$ENTRY"
		fi		
		;;

		--setidmapd)
		if [ -r $IDMAPD_TEMPLATE ]; then
			cp /etc/idmapd.conf /etc/idmapd.orig
			cp $IDMAPD_TEMPLATE /etc/idmapd.conf
		fi		
		;;

		--unsetidmapd)
		if [ -r /etc/idmapd.orig ]; then
			cp /etc/idmapd.orig /etc/idmapd.conf
		fi		
		;;

		*)
		echo "Configures Mariachi NFS client."
		echo "Usage: $0 [--on|--off |--fstabadd|--fstabremove]."
		exit 0
		;;
	esac

