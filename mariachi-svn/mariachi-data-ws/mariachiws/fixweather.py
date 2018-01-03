#!/usr/bin/env python
#
# Quick and dirty. Read in weather files and convert to UTC. 
#
from mariachiws.data import WeatherRecord
from pytz import timezone
import getopt
import os
import sys
import logging


if __name__ == '__main__':
    print "fixweather!"

    # Set up logging..
    loglev = 'warn'
    
    # Check python version 
    major, minor, release, st, num = sys.version_info
    # Set up logging, handle differences between Python versions... 
    # In Python 2.3, logging.basicConfig takes no args
    #
    FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
    if major == 2 and minor ==3:
        logging.basicConfig()
        log = logging.getLogger()
    else:
        logging.basicConfig(format=FORMAT)
           
    if loglev == 'debug':
        log.setLevel(logging.DEBUG)
    elif loglev == 'info':
        log.setLevel(logging.INFO)
    elif loglev == 'warn':
        log.setLevel(logging.WARN)
    log.debug("Logging initialized. ")
   
    usage = '''fixweather.py -- import weather files and change timezone.
     Outputs to <filepath>/fixed/<filename>
     Usage: fixweather.py     FILESTOFIX
    
    
    '''
   
    inzone='US/Eastern'  # default input zone
    
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hdvz:", ["help", 
                                                  "debug", 
                                                  "verbose",
                                                  "zone",
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
            log.setLevel(logging.DEBUG)
        elif opt in ("-v", "--verbose"):
            log.setLevel(logging.INFO)
            log.info("verbose logging enabled.")
    
    for f in args:
        log.info("processing file: %s" % f)
        absp = os.path.abspath(f)
        log.debug("absolute path is %s" % absp)
        (base,file) = os.path.split(absp)
        if os.path.exists("%s/fixed" % base):
            pass
        else:
            log.info("making output directory %s/fixed ..." % base)
            os.mkdir("%s/fixed" % base)
        
        outfile = "%s/fixed/%s" % (base, file )
        log.info("output file: %s" % outfile  )
        wf = open(f)
        recordlist = []
        tz = timezone(inzone)
        for line in wf.readlines():
            line = line.strip()
            wr = WeatherRecord(line, tzinfo=tz)
            recordlist.append(wr)
        log.info("created %d WeatherRecords" % len(recordlist))
        
        of = open(outfile, 'w')
        for wr in recordlist:
            of.write("%s\n" % wr.fullAsUTC())
        of.close()
        log.debug("wrote to output file %s" % outfile )    
        
        
        
                    