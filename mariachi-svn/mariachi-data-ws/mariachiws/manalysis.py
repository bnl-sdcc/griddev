#!/usr/bin/env python
# 
# Python interface to Dima Vavliov's manalysis.R
# 
import sys
import os
import getopt
from ConfigParser import ConfigParser
from tempfile import mkstemp


# Read in config file
config=ConfigParser()
config.read(['/etc/mariachi/mariachi-ws.conf','/home/jhover/devel/mariachi-data-ws/config/mariachi-ws.conf' ])


# Set up logging...
import logging
logfilename= config.get('analysis','logfile') 
# Check python version 
major, minor, release, st, num = sys.version_info
# Set up logging, handle differences between Python versions... 
# In Python 2.3, logging.basicConfig takes no args
#
FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
if major == 2 and minor ==3:
    logging.basicConfig()
    log = logging.getLogger()
    hdlr = logging.FileHandler(logfilename)
    formatter = logging.Formatter(FORMAT)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr) 
else:
    logging.basicConfig(filename='%s' % logfilename, format=FORMAT)
    log = logging.getLogger()
       
loglev = config.get('analysis','loglevel').lower()
if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)

log.debug("Logging initialized with logfile %s" % logfilename)

# Global variable to hold R
robj = None


#################################################################
#
# Python interface to manalysis script.
#
#################################################################

def mavgcounts(file="data.dat",outfile=None,interval=30):
    log = logging.getLogger()
    #(infd, inpath) = mkstemp()
    if not outfile:
        (ofd, outfile) = mkstemp()
    log.debug("manalysis.mavgcounts(): file=%s outfile=%s interval=%d" %(file, outfile, interval))
    if os.path.getsize(file) > 0:
        robj = getRobject()
        robj.mavgcounts(file=file, ofile=outfile,interval=interval)
        log.debug("manalysis.mavgcounts(): Done. Wrote output to %s" % outfile)
        retstring = open(outfile).read()
    else:
        retstring = "No input data."
    return retstring

def mavgweather(file="wdata.dat",outfile=None,interval=30):
    log = logging.getLogger()
    if not outfile:
        (ofd, outfile) = mkstemp()
    log.debug("manalysis.mavgweather(): file=%s outfile=%s interval=%d" %(file, outfile, interval))
    if os.path.getsize(file) > 0:
        robj = getRobject()
        robj.mavgweather(file=file, ofile=outfile,interval=interval)
        log.debug("manalysis.mavgweather(): Done. Wrote output to %s" % outfile)
        retstring = open(outfile).read()
    else:
        retstring = "No input data."    
    return retstring

def mavgboth( cfile, wfile, outfile=None, interval=30):
    log = logging.getLogger()
    if not outfile:
        (ofd, outfile) = mkstemp()
    log.debug("manalysis.mavgboth(): cfile=%s wfile=%s outfile=%s interval=%d" %(cfile, wfile, outfile, interval))
    if os.path.getsize(cfile) > 0 or os.path.getsize(wfile) > 0:
        robj = getRobject()
        robj.mavgboth(cfile=cfile, wfile=wfile, ofile=outfile,td=interval)
        log.debug("manalysis.mavgboth(): Done. Wrote output to %s" % outfile)
        retstring = open(outfile).read()
    else:
        retstring = "No input data." 
    return retstring


def mtbcomb(tab,td=30):
    '''
    Takes a single table and averages entries over interval <td> (in minutes). 
    
    '''
    log = logging.getLogger()
    robj = getRobject()


'''
tb1 <-mreadcounts(counts_file)
tb2 <-mreadweather(weather_file)
tbres -< mtbcomb2(tb1, tb2, interval)

'''


def mtbcomb2(tab,wtb,td=30):
    '''
    Extends <tab> with matching weather from <wtab> and returns the combined table. 
    Contract: Weather table must cover more time than initial table. 
    
    
    '''
    log = logging.getLogger()
    robj = getRobject()

def getRobject():
    global robj
    if robj:
        log.debug("manalysis.getRobject(): R already imported.")
        return robj
    else:
        log.debug("manalysis.getRobject(): R not found. Importing.")
        from rpy import r as robj
        # Set up R interface...
        manalysis_file=config.get('analysis','manalysis_file')
        robj.source(manalysis_file)
        log.debug("R interface to manalysis set up via file %s" % manalysis_file)
        return robj



if __name__ == "__main__": 
    usage = '''Usage: manalysis.py [OPTION] -c <countsfile> -w <weatherfile> -o <outfile> -i <interval> FUNCTION
manalysis.py -- Python interface to Dima Vavilov's manalysis.R 
Gather information on system processes 
   -h | --help          print this message
   -d | --debug         debug logging
   -v | --verbose       verbose logging 
   -c | --countsfile    counts file
   -w | --weatherfile   weather file
   -o | --outfile       output file
   -i | --interval      interval in seconds.
   
Report problems to <jhover@bnl.gov>'''
  
    # Command line arg defaults       
    outfile = None
    countsfile = None
    weatherfile = None
    interval = None
    
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hdvc:w:i:o:", ["help", 
                                                       "debug", 
                                                       "verbose",
                                                       "countsfile", 
                                                       "weatherfile",
                                                       "interval",
                                                       "outfile"])
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
        elif opt in ("-c", "--countsfile"):
            countsfile = arg
        elif opt in ("-w", "--weatherfile"):
            weatherfile = arg
        elif opt in ("-i","--interval"):
            interval = int(arg)
        elif opt in ("-o", "--outfile"):
            outfile = arg        

    if countsfile and weatherfile:
        log.debug("manalysis.main(): countsfile and weatherfile defined.")
        if interval:
            log.debug("manalysis.main(): interval also defind.")
        else:
            log.debug("manalysis.main(): interval also defind.")
            
    elif countsfile:
        log.debug("manalysis.main(): countsfile but not weatherfile defined.")
        if interval:
            print( mavgcounts(file=countsfile, interval=interval))
        else:
            print( mavgcounts(file=countsfile ))
    elif weatherfile:
        log.debug("manalysis.main(): weatherfile but not countsfile defined.")
        if interval:
            print( mavgweather(file=weatherfile, interval=interval))
        else:
            print( mavgweather(file=weatherfile ))
        
    
    