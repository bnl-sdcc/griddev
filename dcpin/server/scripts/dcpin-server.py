#!/usr/bin/env python
'''
dcpin-server.py

dCache file pinning server daemon.

 John Hover <jhover@bnl.gov>
 

'''
try:
    import psyco
    psyco.full()
except ImportError:
    pass

import Pyro.core
import sys, logging, getpass, getopt 
from ConfigParser import ConfigParser

### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/dcpin/common')
from dcpin.core import *
from dcpin.server import DCPinServer

# Default constants
default_config='/etc/dcpin/server.conf'
configfile=default_config
pwstdin = 0

usage = """Usage: dcpin-server.py [OPTIONS] 
OPTIONS: 
    -h --help      print this message
    -d --debug     print debug messages
    -v --verbose   print verbose information
    -p --password  take admin console password on stdin
    -c --config    path to config file
    """ 

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdvpc:", ["help", "debug", "verbose", "password", "config"])
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

cp=ConfigParser()
cp.read(['config/server.conf', default_config , configfile ])

if (pwstdin):
    pw = getpass.getpass()
    cp.set('sshconsole', 'password', pw)

# Set up logging. 
logging.basicConfig()
log = logging.getLogger()
loglev = cp.get('server','loglevel')
if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)

#
# Initialize Pyro
#  
Pyro.core.initServer(banner=0)
daemon=Pyro.core.Daemon(port=int(cp.get('server','port')))
server=DCPinServer(config=cp)
uri=daemon.connect(server,"dcpinserver")

logging.debug("The daemon runs on port: %s" % daemon.port)
logging.debug("The object's uri is: %s" % uri)

try:
    daemon.requestLoop()
except (KeyboardInterrupt): # Exit gracefully when run from console...
    logging.debug('dcpin-server: Got Ctrl-C. Closing down server cleanly... ')
    server.shutDown()
    logging.debug('dcpin-server: Got Ctrl-C. Server shut down cleanly.')
    logging.info(" User cancel via Ctrl-C. Bye!")
    sys.exit(0)