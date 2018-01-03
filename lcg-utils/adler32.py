#!/bin/env python2.4
#
#

import zlib
import os, sys, logging, getopt


def calcAdler32(filename,chunksize):

    log.debug("Initial checksum is %d" % zlib.adler32(""))
    checksum = zlib.adler32("")
    
    try:
        f = open(filename)    
    except IOError:
        log.error("Problem opening %s" % filename)
    
    try:
        while (1):
            fstring = f.read(chunksize)
            if len(fstring) == 0:
                break
            log.debug("Chunk length is %d" % len(fstring))
            checksum = zlib.adler32(fstring,checksum)
    finally:
        f.close()
        log.debug('Closed the file.')
    return checksum



usage = """Usage: adler32.py [OPTIONS] FILE [FILE...] 
OPTIONS: 
    -h --help      print this message
    -d --debug     print debug messages
    -c --chunksize read() size in bytes [1024]
    """ 
# Handle command line options
debug = 0
batch = 0
chunksize = 1024
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "hdc:", 
                               ["help", 
                                "debug",
                                "chunksize", 
                                ])
except getopt.GetoptError:
    print "Unknown option..."
    print usage                          
    sys.exit(1)        
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print usage                     
        sys.exit()            
    elif opt in ("-d", "--debug"):
        debug = 1
    elif opt in ("-c", "--chunksize"):
        chunksize = int(arg)

# Set up logging. 
FORMAT="%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.WARN)

if debug: 
    log.setLevel(logging.DEBUG)

# Need at least one file
if len(args) < 1:
    log.error("Need at least one filename.")
    print usage                          
    sys.exit(1) 

if len(args) > 1:
    batch = 1

for fn in args:
    csum = calcAdler32(fn,chunksize)
    if batch:
        print "%s " % os.path.basename(fn),
    print csum

