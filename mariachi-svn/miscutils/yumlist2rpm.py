#!/usr/bin/env python
#
# Very simple script to convert output of 'yum list all' to
# RPM names. 

import os, sys
debug=0

lines = sys.stdin.readlines()
for line in lines:
    line= line.strip()
    if debug: print "line is: %s" % line
    (f1, release, f3) = line.split()
    if debug: print "f1: %s" % f1     
    (name, arch) = f1.split('.')
    if debug: print "name: %s arch: %s" % (name,arch)
    print "%s-%s.%s.rpm" % (name, release, arch)