#!/bin/bash
#
#
# Find, partition, format, and mount the first available ephemeral storage device.  
# Record it in /etc/fstab in case of instance reboot.
#
#
#

# pull in sysconfig settings
[ -f /etc/sysconfig/cloudconfig.sysconfig ] && . /etc/sysconfig/cloudconfig.sysconfig
[ -f /etc/cloudconfig/conf.d/ephemeral.conf ] && . /etc/cloudconfig/conf.d/ephemeral.conf

# If an ephemeral disk is provided, make it /home and 
# preserve existing content. 
for VD in $VIRTUAL_DISKS ; do
		echo "Checking /dev/$VD ..." >> $LOGFILE
	fdisk -l /dev/$VD 2>/dev/null | grep Disk >> $LOGFILE
	if [ $? -eq 0 ]; then
		d=`date`
		echo "Virtual disk seen at /dev/$VD: $d"
		echo "Virtual disk seen at /dev/$VD: $d" >> $LOGFILE
		echo "Creating filesystem..."
		echo "Creating filesystem..." >> $LOGFILE
		mkfs.ext3 -F -L home /dev/$VD | tee $LOGFILE
		echo "Mounting and mirroring /home..."
		echo "Mounting and mirroring /home..." >> $LOGFILE  2>&1
		mv -v /home /home.orig >> $LOGFILE  2>&1
		mkdir -v /home >> $LOGFILE  2>&1
		mount -t ext3 /dev/$VD /home >> $LOGFILE  2>&1
		cp -avr /home.orig/* /home   >> $LOGFILE  2>&1
		d=`date`
		echo "Done with /dev/$VD: $d"
		echo "Done with /dev/$VD: $d" >> $LOGFILE 
		break
	else
	    echo "No virtual disk seen at /dev/$VD: $d"
	fi
	echo "For disk /dev/$VD, nope..." >> $LOGFILE
done
d=`date`
echo "Done: $d" >> $LOGFILE 

