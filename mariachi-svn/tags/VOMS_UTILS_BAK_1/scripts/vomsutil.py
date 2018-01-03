#!/usr/bin/env python2.4
#
# Script to invoke the VOMS web service to get a list of members in a group or role, and
# write them to a simple text file. 
#
#

import os, sys, logging, getpass, getopt, time, threading 
from ConfigParser import ConfigParser

### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/vomsutils/')
import vomslib

# Default constants
default_config='/etc/grid-security/vomslib.conf'
configfile=default_config
debug = 0
info = 0
warn = 0

usage = """Usage: vomsutil.py [OPTIONS] 
OPTIONS: 
    -h --help      print this message
    -d --debug     print debug messages
    -v --verbose   print verbose information
    -C --config    path to config file [/etc/grid-security/vomsutils.conf]

    """ 
# Handle command line options
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "hdvc:", 
                               ["help", 
                                "debug", 
                                "verbose", 
                                "config",
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
    elif opt in ("-v", "--verbose"):
        info = 1
    elif opt in ("-c","--config"):
        configfile = arg


# Read in config file
config=ConfigParser()
config.read(['config/vomslib.conf', default_config , configfile ])

# Set up logging. 
FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
loglev = config.get('main','loglevel').lower()

if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)

# Override with command line switches
if debug: 
    log.setLevel(logging.DEBUG)
if info:
    log.setLevel(logging.INFO)


vos = config.get('main', 'vos').split(',')
log.debug('Setting up VOMS servers for: %s' % vos)


for vo in vos:
    vs = vomslib.VOMSServer(config, vo )
    log.debug("%s" % vs)
    members = vs.listMembers()
    for m in members:
        print m
    majv=vs.getMajorVersionNumber()
    print majv 
    minv=vs.getMinorVersionNumber()
    print minv
    pv=vs.getPatchVersionNumber()
    print pv
    v=vs.getVersion()
    print v
    n=vs.getVOName()
    print n
    subgroups = vs.listSubGroups(n)
    for s in subgroups:
        print s
        members=vs.listMembers(s)
        for m in members:
            print m
    log.debug("vomsutil.py: Creating new user for VOMS server %s..." % vo)
    newuser="/DC=org/DC=doegrids/OU=People/CN=John Q. User 123456"
    newuserca="/DC=org/DC=DOEGrids/OU=Certificate Authorities/CN=DOEGrids CA 1"
    newcn="John Q. User 123456"
    newmail="jqu@bnl.gov"
    newcerturi=""
    userobj={}
    userobj['DN']=newuser
    userobj['CA']=newuserca
    userobj['CN']=newcn
    userobj['certUri']=newcerturi
    userobj['mail']=newmail
    
    
    print 'Available methods:'
    methodnames= vs.proxy.methods.keys()
    methodnames.sort()
    for m in methodnames:
        print "   %s" % m
        

    
    