#!/usr/bin/env python
#
# Client to use webdav to copy files to/from a server.
# Uses federated identities for auth.  
# Supports Apache Basic Auth and Shibboleth via ECP
#
#
import os
import sys
import getopt
import commands
import getpass
import stat
import re
import datetime
import logging
import time

from ConfigParser import ConfigParser

# Since script is in package "icutils" we can know what to add to path
(libpath,tail) = os.path.split(sys.path[0])
sys.path.append(libpath)

debug = 0
info = 0
warn = 0
list = 0
config_file = None
default_configfile = os.path.expanduser("~/.icutils/fedcopy.conf")
logfile = None
version="0.8.0"

usage = """Usage: fedcopy [OPTIONS] <source> <dest> 
VALID SOURCE/DEST 
   https://internet.host.com/path/to/file.txt
   username@http://host.edu/path/to/file.2.txt
   file://local/path/to/file.txt
   /path/to/file.txt
   
OPTIONS: 
    -h --help                   Print this message
    -i --idptag                 What identity provider to use for auth.  
    -l --list                   Print list of configured auth sources.
    -d --debug                  Debug messages
    -v --verbose                Verbose information
    -c --config                 Config file [~/.icutils/fedcopy.conf]
    -V --version                Print program version and exit.
    -L --logfile                Log output to logfile as well as stdout.
 """

# Handle command line options
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "c:hldvVL:", 
                               ["config=",
                                "help", 
                                "list", 
                                "debug", 
                                "verbose",
                                "version",
                                "logfile="
                                ])
except getopt.GetoptError, error:
    print( str(error))
    print( usage )                          
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(usage)                     
        sys.exit()            
    elif opt in ("-c", "--config"):
        config_file = arg
    elif opt in ("-l", "--list"):
        list = 1
    elif opt in ("-d", "--debug"):
        debug = 1
    elif opt in ("-v", "--verbose"):
        info = 1
    elif opt in ("-V","--version"):
        print(version)
        sys.exit()
    elif opt in ("-L","--logfile"):
        logfile = arg
 
log = logging.getLogger()

# Read in config file
cp=ConfigParser()
if not config_file:
    config_file = default_configfile
got_config = cp.read(config_file)

# Set up logging. 
# Check python version 
major, minor, release, st, num = sys.version_info

# Set up logging, handle differences between Python versions... 
# In Python 2.3, logging.basicConfig takes no args
#
FORMAT23="[ %(levelname)s ] %(asctime)s %(filename)s (Line %(lineno)d): %(message)s"
FORMAT24=FORMAT23
FORMAT25="[%(levelname)s] %(asctime)s %(module)s.%(funcName)s(): %(message)s"

if major == 2:
    if minor ==3:
        formatstr = FORMAT23
    elif minor == 4:
        formatstr = FORMAT24
    elif minor == 5:
        formatstr = FORMAT25
    elif minor == 6:
        formatstr = FORMAT25
    elif minor == 7:
        formatstr = FORMAT25


log = logging.getLogger()
hdlr = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(FORMAT23)
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
# Handle file-based logging.
if logfile:
    hdlr = logging.FileHandler(logfile)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)

logLev = cp.get('global','logLevel').lower()
if logLev == 'debug':
    log.setLevel(logging.DEBUG)
elif logLev == 'info':
    log.setLevel(logging.INFO)
elif logLev == 'warn':
    log.setLevel(logging.WARN)
if debug: 
    log.setLevel(logging.DEBUG) # Override with command line switches
if info:
    log.setLevel(logging.INFO) # Override with command line switches

start = time.time()

end = time.time()
elapsed = end - start

m, s = divmod(elapsed, 60)
h, m = divmod(m, 60)
elapsedstr="%dh%02dm%02ds" % (h, m, s)

log.info("Process took %s" % elapsedstr )

