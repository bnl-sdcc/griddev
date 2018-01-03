#!/bin/bash
#
# Bootstrap VM configuration script.
#
# Author: John Hover <jhover@bnl.gov>
#

################################ CONSTANTS ####################################

DISABLE_SERVICES="anacron apmd atd auditd avahi-daemon bluetooth cpuspeed cups firstboot gpm haldaemon hidd iptables ip6tables iscsi iscsid kudzu lvm2-monitor mcstrans mdmonitor messagebus microcode_ctl netfs nfslock pcscd  portmap rawdevices readahead_early readahead_later restorecond rpcgssd rpcidmapd sendmail smartd xfs yum"

ENSURE_SERVICES="acpid"


################################ FUNCTIONS ####################################


disable_selinux(){
#echo "  Disabling selinux.."
   TARGET_KEY=SELINUX
   REPLACE_VAL=disabled
   CONFIG_FILE=/etc/sysconfig/selinux
   sed -c -i "s/\($TARGET_KEY *= *\).*/\1$REPLACE_VAL/" $CONFIG_FILE
#echo "  Done."
}


yum_update(){
#  echo " Performing yum update..."
   yum -y update
#  echo "  Done."
}

disable_services(){
#  echo " Disabling unneeded services..."
   for s in $DISABLE_SERVICES; do
    #     echo "Disabling $s..."
      service $s stop
      chkconfig $s off
   done

#echo "  Done."
}

enable_random_hostname(){
 echo 'hostname $RANDOM.localdomain' >> /etc/rc.local		
}

################################ MAIN SCRIPT ###################################

#echo "Performing config..."

disable_selinux
disable_services
enable_random_hostname
