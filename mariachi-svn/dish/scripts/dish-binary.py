#!/usr/bin/python
#
# dish.py
#
# Distributed Interactive Shell --
# Run shell commands simultaneously over multiple hosts.
# Author: John Hover <jhover@bnl.gov>
# 
# Similar to dsh (in C) at 
#  http://www.netfort.gr.jp/~dancer/software/downloads/list.cgi
# 
# This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 

import os, sys, logging, getpass, getopt, time, threading
from ConfigParser import ConfigParser
import pexpect


### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/dish/')
from dish.core import *



# Default constants
default_config='/etc/dish/dish.conf'
configfile=default_config

#Flag defaults
allhosts=0
command=None
debug = 0
info = 0
warn = 0
filelist=None    # List of hosts given by file. One per line. 
grouplist=None   # List of groups to run on.
hophost=None     # Intermediate host to connect through
listgroups = 0   # Please list groups of hosts
listmembers=None # Group(s) to list host members of
onlyping=0
ping=1           # Ping hosts by default before attempting connection.
script=None
timeout=10       # seconds
useuser=os.getlogin()
wordprompt=0

usage = """Usage: dish.py [OPTIONS]
DISH: Distributed Interactive SHell. Provides a parallel shell to multiple 
hosts, executing command lines on all and collating output. 
 
OPTIONS:
    -a --all                  Run on ALL hostgroups defined in config. 
    -c --command              Run command and exit. 
    -C --config <path>        Path to config file [/etc/dish/dish.conf].
    -d --debug                Print debug messages.
    -f --filelist <file>      Run on hosts in file list (one per line).       
    -g --grouplist <a,b,c>    List of hostgroups to run on.
    -h --help                 Print this message.
    -H --hop <host>           Hop to <host> then to the node.
    -l --list                 List available hostgroups.
    -m --memberlist <group>   List members of specified hostgroup. 
    -p --ping-only            Only ping the nodes (do NOT invoke shell or execute command).
    -P --no-ping              Do NOT ping the nodes before invoking shell/executing.
    -s --script <file>        Run the provided script on hosts and exit.
    -t --timeout <seconds>    Timeout commands after # seconds.
    -u --user                 Connect as this user (override config).
    -v --verbose              Print verbose information.
    -w --word                 Prompt once for password. 
""" 

# Handle command line options
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, 
                               "ac:C:df:g:hH:lm:pPst:u:vw", 
                               ["all",
                                "command",
                                "config",
                                "debug", 
                                "filelist",
                                "grouplist",                                
                                "help",
                                "hop", 
                                "list",
                                "memberlist",
                                "ping-only"
                                "no-ping",
                                "script",
                                "timeout",
                                "user",
                                "verbose",
                                "word",
                                ])
except getopt.GetoptError:
    print "Unknown option..."
    print usage                          
    sys.exit(1)        
for opt, arg in opts:
    if opt in ("-a", "--all"):
        allhosts = 1
    
    elif opt in ("-c","--command"):
        command = arg
    
    elif opt in ("-C","--config"):
        configfile = arg
            
    elif opt in ("-d", "--debug"):
        debug = 1
    
    elif opt in ("-f","--filelist"):
        filelist = arg

    elif opt in ("-g","--grouplist"):
        grouplist = arg    
        
    elif opt in ("-h", "--help"):
        print usage                     
        sys.exit()
                    
    elif opt in ("-H", "--hop"):
        hophost = arg

    elif opt in ("-l","--list"):
        listgroups = 1
        
    elif opt in ("-m","--memberlist"):
        listmembers = arg

    elif opt in ("-s","--script"):
        script = arg
        
    elif opt in ("-t","--timeout"):
        timeout = int(arg)

    elif opt in ("-u","--user"):
        useuser = arg

    elif opt in ("-v", "--verbose"):
        info = 1
        
    elif opt in ("-w","--word"):
        wordprompt=1
# Read in config files
config=ConfigParser()
config.read(['config/dish.conf', default_config , configfile ])

# Set up logging. 
FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
loglev = config.get('global','loglevel').lower()

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

log.debug("dish-binary.py: Logging level set...")



# add in command line flags to global config...
config.add_section('args')
config.set('args','allhosts',allhosts)
config.set('args','command',command)
config.set('args','grouplist', grouplist)

if filelist:
    try:
        filehosts = []
        hoststring = ""
        f = open(filelist).readlines()
        for line in f:
            filehosts.append(line.strip())
        hoststring=','.join(filehosts)
        config.set('args','filelist',filehosts)
        hgs = config.get('global','hostgroups')
        hgs = "%s,_filegroup" % hgs
        config.set('global','hostgroups', hgs)
        config.add_section('_filegroup')
        config.set('_filegroup','hosts',hoststring)
        if grouplist:
            config.set('args','grouplist',"%s,_filegroup" % grouplist)
        else:
            config.set('args','grouplist',"_filegroup")
        
    except IOError:
        log.error("dish-binary.py: Problem with filelist file: %s" % filelist)
        sys.exit(1) 

if grouplist and not filelist:
    config.set('args','grouplist',grouplist)
    
    


    
if listgroups:
    config.set('args','listgroups',1)

if listmembers:
    config.set('args','listmembers',listmembers)

config.set('args','user',useuser)


#
# Handle informational actions...
#
if listgroups:
    grps = config.get('global','hostgroups').split(',')
    for g in grps:
        print g 
    sys.exit(0)

if listmembers:
    hsts = config.get(listmembers, 'hosts').split(',')
    for h in hsts:
        print h
    sys.exit(0)

#
# Sanity checks...
#
#if not allhosts:
#    if not grouplist: 
#        if not filelist:
#            print "You must specify group(s), all hosts (--all), or a file (--filelist <file>)."
#            print usage
#            sys.exit(1)


#
# Create objects...
#

console = DishConsole(config)

if debug:
    print "DEBUG!!"
    sects = config.sections()
    for s in sects:
        items = config.items(s, raw=True)
        for (key,val) in items:
            print "sect: %s key: %s val: %s" % (s,key,val)
        
#
# Perform actual actions...
#
console = DishConsole(config)

if script:
    try:
        f = open(script)
        lines = f.readlines()
        for line in lines:
            console.doCommand(line)
    except IOError:
        log.error("dish-binary.py: Problem with script file %s" % script)

else:
    while 1:
        try:
            print ">",
            line = sys.stdin.readline()
            result = console.doCommand(line)
            for a in result:
                print a
        except (KeyboardInterrupt): 
            logging.info("Shutdown via Ctrl-C or -INT signal.")
            log.debug('dish-binary.py: Done.')
            sys.exit(1)
            
            
    
    






    
