#!/bin/env python
#
# Simple script to generate a userlist for LCG/gLite
# jhover@bnl.gov
# 2006-07-06
#
#

import math


####################### Script Variables (edit these) ###########


# Groups hash, <VO/group name> : <number of accounts in group>
groups={ 'dteam' : 50 , 'atlas': 200 }

# Extra user suffixes to be created for all VOs
extras=[ "prd", "sgm" ]

# Format digits -- how wide should the number be? e.g. atlas002
fmt_digits=3


######################## Functions #############################

def maxval( grdict):
    max = 0
    for key in grdict.keys():
        if grdict[key] > max:
            max = grdict[key]
    return max

def format_id( num, digits ):
    strnum = str(num)
    for j in range(1,digits):
        #print "    j is %d" % j
        thresh = math.pow(10,j)
        #print "    threshold is %d" % thresh
        if num < thresh:
            #print "    %d is less than %d" % (num, thresh)
            strnum = "0%s" % strnum
        #elif num > thresh:
            #print "    %d not less than %d" % (num, thresh)
    return strnum

####################### Script  ###############################

maxid=maxval(groups)
#print "makelist"
#print "maxuid will be %d" % maxid

for uid in range(1,maxid):
    #print "UID is %d" % uid
    for vo in groups.keys():
        fmtuid=format_id(uid,fmt_digits)
        #print "formatted uid is " , fmtuid
        if uid < groups[vo]:
            print "%s%s" % (vo,fmtuid) ,

for vo in groups.keys():
    for suffix in extras:
    #print "formatted uid is " , fmtuid
        print "%s%s" % (vo,suffix) ,


