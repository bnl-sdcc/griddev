#!/usr/bin/env python
#
# Script to invoke the VOMS web service to get a list of members in a group or role, and
# write them to a simple text file. 
#
#

import urllib2 
 
print "mkdnlist.py -- grab dnlists!"

f = urllib2.urlopen('https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?method=listMembers')
print f.read(100)