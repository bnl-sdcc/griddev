#!/bin/env python
#
#
#
#
from ConfigParser import ConfigParser
import getopt
import os
import sys
import logging


class AnalysisBatch(object):
    
    def __init__(self, config):
        self.log = logging.getLogger()
        self.log.debug("Init...")
        self.config = config

    def execute(self):
        self.log.debug("Executing...")


if __name__=='__main__':

    debug = 0
    info = 0
    warn = 0
    config_file = None
    default_configfile = os.path.expanduser("~/share/analysis.conf")
    version="mariachi-data-analysis 0.7"
    
    usage = """Usage: analysis.py [OPTIONS]  
OPTIONS: 
    -h --help                   Print this message
    -d --debug                  Debug messages
    -v --verbose                Verbose information
    -c --config                 Config file [~/etc/analysis.conf]            
    -V --version                Print program version and exit.
 """

    # Handle command line options
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 
                                   "c:hdvV", 
                                   ["config=",
                                    "help", 
                                    "debug", 
                                    "verbose",
                                    "version",
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
        elif opt in ("-d", "--debug"):
            debug = 1
        elif opt in ("-v", "--verbose"):
            info = 1
        elif opt in ("-V","--version"):
            print(version)
            sys.exit()
     
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
    FORMAT26=FORMAT25
    
    if major == 2:
        if minor ==3:
            formatstr = FORMAT23
        elif minor == 4:
            formatstr = FORMAT24
        elif minor == 5:
            formatstr = FORMAT25
        elif minor == 6:
            formatstr = FORMAT26

    hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(FORMAT23)
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
    
    log.info("Starting Run...")
        
    log.debug("Creating AnalysisBatch().")
    batchobj = AnalysisBatch(cp)
    log.debug("Done creating AnalysisBatch().")
    log.debug("Executing AnalysisBatch.execute()")
    batchobj.execute()
    log.debug("Done.")    