#!/usr/bin/env python
#
# Script to invoke the VOMS web service to get a list of members in a group or role, and
# write them to a simple text file. 
#
#

import os
import sys
import logging
import getpass
import getopt
import time
import threading 
from ConfigParser import ConfigParser

### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/python-vomsadmin/')
from vomsadmin.vomsapi import VOMSServer, VOMSMember, CachingVOMSWrapper

# Check python version 
major, minor, release, st, num = sys.version_info
logging.debug('vomsadmin.vomsutil : Found python %d.%d' % (major, minor) )  
if major ==  2 and minor >= 4:
    pass
else:
    logging.fatal('vomsadmin.vomsutil : This module requires Python 2.4')
    sys.exit(0)




# Default constants & flags
default_config='/etc/grid-security/python-vomsadmin.conf'
configfile=default_config
debug = 0
info = 0
warn = 0
test = 0
list = 0
cache = 0
serv = None
syncfrom = None
syncto = None

usage = """Usage: vomsutil.py [OPTIONS] [COMMANDS] 
OPTIONS: 
    -h --help                    Print this message
    -d --debug                   Debug messages
    -v --verbose                 Verbose information
    -c --config                  Config file [/etc/grid-security/python-vomsadmin.conf]
    -f --from   S1               Server to synchronize FROM 
    -t --target S2               Server to synchronize TO
    -s --server <V1> <ARGS>      Perform a VOMSAdmin API command on server V1
    -l --list                    List available/configured VOMS servers
    -T --test                    Run diagnostic tests
    -C --cache                   Use cacheing.   
COMMANDS:
    getVOName
    getVersion                               Prints VOMSAdmin version.
    listMembers                              Prints DNs of all members. 
    listMembers /vo/group                    Lists DNs of group members.
    listSubGroups /voname                    Lists subgroups.
    listUsersWithRole /vo/group Role=role    Lists DNs of members with role.""" 


# Handle command line options
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "hdvc:s:f:t:lTC", 
                               ["help", 
                                "debug", 
                                "verbose", 
                                "config=",
                                "server=",
                                "from=",
                                "target=",
                                "list",
                                "test",
                                "cache",
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
    elif opt in ("-s", "--server"):
        serv = arg  
    elif opt in ("-f", "--from"):
        syncfrom = arg
    elif opt in ("-t", "--target"):
        syncto = arg    
    elif opt in ("-T","--test"):
        test = 1    
    elif opt in ("-l","--list"):
        list = 1
    elif opt in ("-C","--cache"):
        cache = 1


# Read in config file
config=ConfigParser()
config.read(['config/python-vomsadmin.conf', default_config , configfile ])

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

log.debug("Left over command line args are %s" % args)


vomses = config.get('main', 'vomses').split(',')
log.debug('Setting up VOMS servers for: %s' % vomses)

servers = {}

for v in vomses:
    if cache:
        vs = CachingVOMSWrapper(config, v )
    else:
        vs = VOMSServer(config, v)
    
    servers[v] = vs
    log.debug("%s" % vs)

if list:
    for v in vomses:
        print v

if serv and not args:
    print 'You need to provide a command. Try "%s --help"' % sys.argv[0]

if serv and args:
    log.debug("vomsutil.py: Received command to run on server %s" % serv)
    vs = servers[serv]
    try:
        vs.doCommand(' '.join(args))
    except Exception, e:
        log.error("vomsutil.py: %s" % e)
    
        
if syncfrom and syncto:
    log.info("vomsutil.py: Sync requested from %s to %s" % (syncfrom, syncto) )
    fromserver = servers[syncfrom]
    toserver = servers[syncto]
    toserver.synchronize(fromserver)

    
if test:
    for v in vomses:     
        # Get VO Name
        n=vs.getVOName()
        print "VO Name: %s" % n
        
        # Get and print VOMSMember objects
        members = vs.listMembers()
        for m in members:
            print m
        
        #
        # Check version numbers
        #
        print vs.getVersion()
                
        # List CAs
        #cas=vs.listCAs()
        #for ca in cas:
        #    print ca
        
    
    if cache:
        # Test cache update...
        for k in servers.keys():
            s = servers[k]
            print s.printGroups()
        
        import time
        time.sleep(15)
        # Test for cache hit...
        for k in servers.keys():
            s = servers[k]
            print s.printGroups() 
        
    
    testadds=0
    testdels=0

    newuser="/DC=org/DC=doegrids/OU=People/CN=John Q. User 123456"
    newuserca="/DC=org/DC=DOEGrids/OU=Certificate Authorities/CN=DOEGrids CA 1"
    newcn="John Q. User 123456"
    newmail="jqu@bnl.gov"
    newcerturi=""
    
    if testadds:
        # create user
        log.debug("vomsutil.py: Creating new user for VOMS server %s..." % vo)
        
        nvm=VOMSMember(newuser, newcn, newuserca)    
        print nvm
        try:
            log.info("Creating new user...")
            vs.createUser(nvm)
  
            log.info("Creating new group...")
            # create group
            vs.createGroup('/mariachi', '/mariachi/test')

            # create role
            log.info("Creating new Role...")
            vs.createRole('Role=testrole')
    
            # add user to group
            log.info("Adding user to group...")
            vs.addMember( '/mariachi/test' , newuser, newuserca)
        
            # assign user to role
            log.info("Assigning Role to user...")
            vs.assignRole('/mariachi/test', 'Role=testrole', newuser, newuserca)
            
        except Exception, e:
            print e
            
            
    if testdels:
        log.info("Deleting user...")
        vs.deleteUser(newuser, newuserca)
        log.info("Deleting group...")
        vs.deleteGroup('/mariachi/test')
        log.info("Deleting role...")
        vs.deleteRole('Role=testrole')
        
        
        
        
        