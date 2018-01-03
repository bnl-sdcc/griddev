#!/usr/bin/env python
#
# Utility that wraps the vomsadmin client and also provides access to other utility 
# functionality, e.g. synchronization and DN processing (e.g. looking for duplicate registations). 
#

import os
import sys
import logging
import getpass
import getopt
import time
import threading 
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError

### remove this after RPM install to system paths...
#sys.path.('/home/jhover/devel/python-vomsadmin/')
# Use the following when on a system with the RPM for this project installed.
#sys.path = ['/home/jhover/devel/python-vomsadmin/'] + sys.path

from VOMSAdminUtils.VOMSAdminAPI import VOMSServer, VOMSMember, CachingVOMSWrapper, VOMSException

#
# Having HTTP/S proxies set in the environment will mess things up. 
# Remove them during execution.
#
for k in  os.environ.keys():
    kl = k.lower()
    if kl == "http_proxy" or kl == "https_proxy":
        del os.environ[k]

usage = """Usage: vomsadmin-util.py [OPTIONS] [API COMMANDS] 
OPTIONS: 
BASIC OPTIONS
    -h --help                Print this message
    -c --config              Config file [/etc/grid-security/vomsadmin.conf]
    -d --debug               Debug messages
    -v --verbose             Verbose information

MISC OPTIONS    
    -l --list                List available/configured VOMS servers
    -T --test                Run diagnostic tests.
    -A --cache               Use caching.
    -y --yes                 Do not prompt for dangerous operations.

SYNC AND API OPTIONS
    -Y --synchronize         Do a synchronization. Implies -f and -t.
    -f --from   S1           Server to synchronize FROM 
    -t --target S2           Server to synchronize TO
    -s --server <V1> <ARGS>  Perform a VOMSAdmin API command on server V1

OPTIONS FROM GLITE
    -C --usercert FILE       Extract DN parameters from FILE.
    -K --userkey  FILE       Use this keyfile.
    -V --vo NAME             Connect to the NAME VO.  (No default.)
    -H --host HOSTNAME       Use the VOMS Admin service running on HOSTNAME.
                                (Default is localhost.)
    -P --port PORT           Use the VOMS Admin service running on PORT.
                                (Default is 8080 or 8443 depending on --nossl.)
    -U --url URL             Connect to the admin service runnig on URL.
                                Example: https://localhost:8443/voms/voname
                                (Overrides --nossl, --host, --port, and --vo.)
    --help-commands          Print a list of available commands, then exit.    
    --nousercert             Don't extract DNs from supplied certificates.
    --nossl                  Don't use SSL to connect
        
API COMMANDS:
    getVOName                                  Prints VO name.
    getVersion                                 Prints VOMSAdmin version.
    listMembers                                Prints DN,CA of all members. 
    listMembers /vogroup/group                 Lists DN,CA of group members.
    listSubGroups /vogroup/group               Lists subgroups.
    listUsersWithRole /vogroup/group/Role=role Lists DNs of members with role.
    createUser DN CN CA [ certUri mail]        Creates new user. 


Additional commands available through package API.
    listMembersEmail                           Prints members DN and Email (CSV)
    listAttributeDuplicates <attribute>        Prints info about members w/ duplicate attributes. 
    """ 

# Default constants & flags
default_config='/etc/grid-security/vomsadmin.conf'
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
vo = None
cert = None
key = None
host = None
port = None
url = None


testinterval=5 # seconds

# Handle command line options
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "hdvc:s:f:t:lTAC:K:V:H:P:U:", 
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
                                "usercert",
                                "userkey",
                                "vo",
                                "host",
                                "port",
                                "url",
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
    elif opt in ("-C","--usercert"):
        cert = arg
    elif opt in ("-K","--userkey"):
        key = arg
    elif opt in ("-V", "--vo"):
        vo = arg
    elif opt in ("-H", "--host"):
        host = arg
    elif opt in ("-P", "--port"):
        port = arg
    elif opt in ("-U", "--url"):
        url = arg


# Read in config file
config=ConfigParser()

try:
    config.read( configfile )
except NoSectionError:
    print("ERROR: Config file %s doesn't exist. Try specifying one with '-c <file>' switch. Or '-h' for help." % configfile)
    sys.exit(1)


# Check python version 
major, minor, release, st, num = sys.version_info


# Set up logging, handle differences between Python versions... 
# In Python 2.3, logging.basicConfig takes no args
#
FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
if major == 2 and minor ==3:
    logging.basicConfig()
else:
    logging.basicConfig(format=FORMAT)

log = logging.getLogger()

try:
    loglev = config.get('main','loglevel').lower()
except NoSectionError:
    print("ERROR: Config file %s invalid. Try specifying one with '-c <file>' switch. Or '-h' for help." % configfile)
    sys.exit(1)


if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)
elif loglev == 'error':
    log.setLevel(logging.ERROR)

# Override with command line switches
if debug: 
    log.setLevel(logging.DEBUG)
if info:
    log.setLevel(logging.INFO)

#
# Now that loglevel is set, print out python version...
log.debug('vomsadmin-util.py: Found python %d.%d' % (major, minor) )  
log.debug("vomsadmin-util.py: Using config file: %s" % configfile)
log.debug("vomsadmin-util.py: Left over command line args are %s" % args)

vomses = config.get('main', 'vomses').split(',')
log.debug('vomsadmin-util.py: Setting up VOMS servers for: %s' % vomses)

#
# Handle what user credential to use
#
log.debug("vomsadmin-util.py: Cert specified in config is  %s" % config.get('main','cert_file'))
log.debug("vomsadmin-util.py: Key specified in config is  %s" % config.get('main','key_file')) 


user_id = os.geteuid()
if user_id == 0:
    ## we are running as root, use host certificate
    log.debug("vomsadmin-util.py: Running as root")
    options['user_cert'] = "/etc/grid-security/hostcert.pem"
    options['user_key'] = "/etc/grid-security/hostkey.pem"

elif os.path.exists(config.get('main','cert_file')) and os.path.exists(config.get('main','key_file')):
    log.debug("vomsadmin-util.py: Cert and Key specified in config OK.")
    
else:
    #
    # Config is bad. Try to be smart...
    ## look for a proxy
    proxy_fname = "/tmp/x509up_u%d" % user_id
    if os.path.exists(proxy_fname):
        log.debug("vomsadmin-util.py: Using proxy file found in %s" % proxy_fname )
        config.set('main', 'cert_file', proxy_fname)
        config.set('main', 'key_file', proxy_fname)

    ## look for a proxy in X509_USER_PROXY env variable
    elif os.environ.has_key("X509_USER_PROXY"):
        log.debug("vomsadmin-util.py: Using proxy file found in X509_USER_PROXY %s" % os.environ['X509_USER_PROXY'] )
        config.set('main', 'cert_file', os.environ['X509_USER_PROXY'])
        config.set('main', 'key_file', os.environ['X509_USER_PROXY'] )
        #        options['user_cert'] = os.environ['X509_USER_PROXY']
        #options['user_key'] = os.environ['X509_USER_PROXY']
    
    ## use common certificate    
    elif os.environ.has_key("X509_USER_CERT"):
        log.debug("vomsadmin-util.py: Using proxy file found in X509_USER_CERT %s" % os.environ['X509_USER_CERT'] )
        config.set('main', 'cert_file', os.environ['X509_USER_CERT'])
        config.set('main', 'key_file', os.environ['X509_USER_KEY'] )
                        
    ## look in the .globus directory
    elif not os.path.exists(config.get('main','cert_file')) or not os.path.exists(config.get('main','key_file')):
        log.debug("vomsadmin-util.py: Using credentials found in %s/.globus" % os.environ['HOME'] )
        config.set('main', 'cert_file', os.path.join(os.environ['HOME'],".globus", "usercert.pem"))
        config.set('main', 'key_file', os.path.join(os.environ['HOME'],".globus", "userkey.pem") )
        #vlog("using credentials found in $HOME/.globus...")
        #options['user_cert'] = os.path.join(os.environ['HOME'],".globus", "usercert.pem")
        #options['user_key'] = os.path.join(os.environ['HOME'],".globus", "userkey.pem")


# Override if explicitly specified on the command line.
if cert and key:       
    log.debug("vomsadmin-util.py: User cert specified on command line: %s" % cert )
    config.set('main', 'cert_file', cert)  
    log.debug("vomsadmin-util.py: User key specified on command line: %s" % key )
    config.set('main', 'key_file', key)  

#
#  Set up VOMSServer objects...
#
servers = {}
for v in vomses:
    try:
        log.debug("vomsadmin-util.py: Setting up server [%s]" % v)
        if cache:
            vs = CachingVOMSWrapper(config, v )
        else:
            vs = VOMSServer(config, v)
        
        servers[v] = vs
        log.debug("%s" % vs)
    except VOMSException, ve:
        log.warning(ve)

# Catch KeyboardInterrupt for interactive use...
try:
    if test:
        log.debug("vomsadmin-util.py: Tests requested...")
        sys.exit(0)
        
    # List servers that successfully were set up.
    if list:
       klist = servers.keys()
       for k in klist:
           print servers[k].section
    
    # If server and command is specified, run it and exit...  
    if serv and args:
        log.debug("vomsutil.py: Received command to run on server %s" % serv)
        vs = servers[serv]
        vs.doCommand(args)
        sys.exit(0)
    
    # if specified, sychronize one VOMS to another.        
    if syncfrom and syncto:
        log.info("vomsutil.py: Sync requested from %s to %s" % (syncfrom, syncto) )
        fromserver = servers[syncfrom]
        toserver = servers[syncto]
        toserver.synchronize(fromserver)
        sys.exit(0)

# Gracefully exit on Ctrl-C
except (KeyboardInterrupt):
    sys.exit(0) 
