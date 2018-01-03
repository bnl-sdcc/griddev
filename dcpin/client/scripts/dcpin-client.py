#!/usr/bin/env python
'''
dpin-client.py

dCache file pinning client program


 John Hover <jhover@bnl.gov>
 
'''

import Pyro.core
import sys, logging, getopt
from ConfigParser import ConfigParser

### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/dcpin/common')

#from dcpin.core import *

#
# Editable during develpment
# 
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

default_config='/etc/dcpin/client.conf'
configfile=default_config
docommand =  0

usage = """Usage: dcpin-client.py [OPTIONS] [ <command-and-args>] 
OPTIONS: 
    -h --help          print this message
    -d --debug         print debug messages
    -v --verbose       print verbose information
    -c --config        path to config file
    -x  --exec         execute given command + args and exit  
    """ 

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdvc:x", ["help", "debug", "verbose", "config", "execute"])
except getopt.GetoptError:
    print "Unknown option..."
    print usage                          
    sys.exit(1)        
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print usage                     
        sys.exit()            
    elif opt in ("-d", "--debug"):
        log.setLevel(logging.DEBUG)
    elif opt in ("-v", "--verbose"):
        log.setLevel(logging.INFO)
    elif opt in ("-p","--password"):
        pwstdin = 1
    elif opt in ("-c","--config"):
        configfile = arg
    elif opt in ("-x","--execute"):
        docommmand = 1

cp=ConfigParser()
cp.read(['config/client.conf', default_config , configfile])
host=cp.get('client','host')
port=int(cp.get('client','port'))

# Set up logging. 
logging.basicConfig()
log = logging.getLogger()
loglev = cp.get('client','loglevel')
if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)

Pyro.core.initClient(banner=0)
# you have to change the URI below to match your own host/port.
server = Pyro.core.getProxyForURI("PYROLOC://%s:%d/dcpinserver" % (host, port ) )

if len(args) > 0:
    logging.debug( "Command line args are %s" % args  )
    result = server.doCommand(' '.join(args) )
    print result
    sys.exit(0)

else:
    try: 
        while(1):
            sys.stdout.write('>')
            commandstr = sys.stdin.readline()
            if commandstr.strip() == 'quit' or commandstr.strip() == 'exit':
                sys.exit(0)
            elif commandstr.strip() == '':
                pass
            else:
                result = server.doCommand(commandstr)
                print result
    # Gracefully exit on Ctrl-C
    except (KeyboardInterrupt):
        sys.exit(0)
