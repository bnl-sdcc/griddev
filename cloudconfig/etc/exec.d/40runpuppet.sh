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
[ -f /etc/cloudconfig/conf.d/runpuppet.conf ] && . /etc/cloudconfig/conf.d/runpuppet.conf

puppet apply --modulepath ./modules manifests/site.pp >> $PUPPET_LOG

