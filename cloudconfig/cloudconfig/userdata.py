#!/bin/env python
#
# Retrieve all EC2/Cloud User data and dump to provided root. 
#
# By default, ths is the file tree: 
# /etc/cloudconfig/dynammic
#                 /meta-data    
#                 /user-data
#

from urllib2 import Request, urlopen, URLError
from socket import timeout, error
from ssl import SSLError
import os
import socket
import sys

import traceback

UDTOP="http://169.254.169.254/latest"
LOCAL="http://dev.racf.bnl.gov/dist/"
MDROOT="/etc/cloudconfig/"
DEFAULT_TIMEOUT=3

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError: 
        pass

'''
 Recursive method to retrieve and create directory/files from metadata server. 

 base is relative root on remote site, e.g.  http://169.254.169.254/latest/
 path is sub-path on both remote and local tree, e.g. meta-data/ami-launch-index
 root is local relative root, into which $path should be copied, e.g. /etc/cloudconfig

'''
def get_urltree(base, path, root="/etc/cloudconfig/config"):
    req = Request("%s%s" % (base, path))
    try:
        response = urlopen(req, timeout=DEFAULT_TIMEOUT)
        #thepage = response.read()
        for line in response.readlines():
            line = line.strip()
            print("%s%s%s" % (root, path, line))
            if line.endswith("/"):
                get_urltree(base, "%s%s" % (path,line))
            else:
                get_urlleaf(base, "%s%s" % (path,line))
    
    except URLError, e:
        if hasattr(e, 'reason'):
            sys.stderr.write( 'We failed to reach a server.')
            sys.stderr.write( 'Reason: %s'% e.reason )
        elif hasattr(e, 'code'):
            sys.stderr.write( 'The server couldn\'t fulfill the request.' )
            sys.stderr.write( 'Error code: %s ' % e.code )

def get_urlleaf(base, path, root="/etc/cloudconfig/config"):
    req = Request("%s%s" % (base, path))
    try:
        response = urlopen(req, timeout=DEFAULT_TIMEOUT)
        #thepage = response.read()
        for line in response.readlines():
            line = line.strip()
            print("%s%s value=%s" % (root, path, line))
                 
    except URLError, e:
        if hasattr(e, 'reason'):
            sys.stderr.write( 'We failed to reach a server.')
            sys.stderr.write( 'Reason: %s'% e.reason )
        elif hasattr(e, 'code'):
            sys.stderr.write( 'The server couldn\'t fulfill the request.' )
            sys.stderr.write( 'Error code: %s ' % e.code )

    

def get_metadata():
    print("Getting metadata...")

    #get_urltree(UDTOP, "/dynamic/")
    try:
        get_urltree(UDTOP, "/meta-data/")
        get_urltree(UDTOP, "/user-data/")            
    except socket.timeout, e:
        print("socket.timeout: %s" % str(e))
        #print(traceback.format_exc(None))
    except urllib2.URLError, e:
        print("URLError: %s" % str(e))
        #print(traceback.format_exc(None))
    except Exception, e:
        print("Exception: %s" % str(e))
        print(traceback.format_exc(None))            


if __name__ == "__main__":
    get_metadata()

    