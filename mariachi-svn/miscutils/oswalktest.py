#!/usr/bin/env python

import os, sys

argv = sys.argv[1:]
print argv[0]

for dirpath, dirnames, filelist in os.walk(argv[0]):
    #print "%s/%s/%s" % (dirpath,dirnames,filelist)
    #for n in dirnames:
    for f in filelist:
        print "%s/%s" % (dirpath, f)
            
