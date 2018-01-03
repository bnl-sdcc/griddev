#!/usr/bin/env python
#
# Data file interface library for MARIACHI Project.
# http://www.mariachi.stonybrook.edu
# 
#
############################################################
import os
import sys
import logging
import datetime
import re
from tempfile import mkstemp
import time
from xml.utils.iso8601 import parse as parseiso

logobject = logging.getLogger()

SDTYPES=['counts','events','errors']
SDSUBDIR="/sd"

COUNTSGLOB="counts-\d*.txt"
EVENTGLOB="timestamps-\d*.txt"
ERRGLOB="gps_error-\d*.txt"
WTHRGLOB="weather-\d*.csv"

DATEGLOB="\d+"

WTHRTYPES=['weather',]
WTHRSUBDIR="/weather"

DATERE= re.compile(DATEGLOB, re.IGNORECASE)

FILENAMERES = { 'counts' : re.compile(COUNTSGLOB, re.IGNORECASE),
                'events' : re.compile(EVENTGLOB, re.IGNORECASE),
                'errors' :  re.compile(ERRGLOB, re.IGNORECASE),
                'weather' : re.compile(WTHRGLOB, re.IGNORECASE)               
              }

############################################################
#
# Class definitions
#
############################################################
class Event(object):
    '''
    Class representing an event from the timestamps file.
    
    '''
    def __init__(self, linestr):
        linestr = linestr.strip()
        fields = linestr.split(",")
        #try:
        self.vers = fields[0]
        ymd = fields[1]            
        hms = fields[2]
        self.datetime = _parse_datetime(ymd,hms)
        self.foldness = int(fields[3])
        self.bitmap = fields[4]
        #except Exception, e:
        #    raise ParseException("%s" % e)
     
    def __repr__(self):
        s = "<mariachi.data.Event>"
        return s

    def __str__(self):
        #s = "Event: Version=%s Datetime=%s Foldness=%d Bitmap=%s" % (self.vers, 
        #                                                             self.datetime, 
        #                                                             self.foldness, 
        #                                                             self.bitmap)
        s = "%s,%d,%s" % (self.datetime, 
                          self.foldness, 
                          self.bitmap)
        return s


class CountsRecord(object):
    '''
    Class representing count information for one minute
    ''' 
    def __init__(self,linestr):
        linestr = linestr.strip()
        fields = linestr.split(",")
        #try:
        self.vers = fields[0]

        ymd = fields[1].strip()
  
        #<hours><minutes><secs>.<decimal fraction of seconds>
        hms = fields[2].strip()
        self.datetime = _parse_datetime(ymd,hms)
        #<s1>,<s2><s3>,<s4>,<s5>
        self.s1 = int( fields[3] )
        self.s2 = int( fields[4] )
        self.s3 = int( fields[5] )
        self.s4 = int( fields[6] )
        self.s5 = int( fields[7] )
        # couples 1 + 2
        self.c1 = int( fields[8] )
        # triples (1+2) + [3|4|5]
        self.t1 = int( fields[9] )
        self.t2 = int( fields[10] )
        self.t3 = int( fields[11] )
        # fourfolds 
        self.f1 = int( fields[12] )
        # fivefolds
        self.v1 = int( fields[13] )
        #except Exception, e:
        #    raise ParseException("%s" % e)

    def __repr__(self):
        s = "<mariachi.data.CountsRecord:>"
        return s
    
    def __str__(self):
        '''
          String representation of this object in CSV. Using full info after user request.    
        '''
        return self._fullStr()
    
    def _fullStr(self):
        '''
            Full, direct reporting of all information in counts record.
        
        '''
        s = "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % ( self.datetime,
                                    self.s1,
                                    self.s2,
                                    self.s3,
                                    self.s4,
                                    self.s5,
                                    self.c1,
                                    self.t1,
                                    self.t2,
                                    self.t3,
                                    self.f1,
                                    self.v1)                                                                                                       
        return s
    
    
    def _abbrStr(self):
        '''
            Abbreviated data, with minute aggregate totals for singles and Triples.
        '''
        s = "%s,%d,%d,%d,%d,%d" % ( self.datetime,
                                    self.s1 + self.s2 + self.s3 + self.s4 + self.s5,
                                    self.c1,
                                    self.t1 + self.t2 + self.t3,
                                    self.f1,
                                    self.v1)                                                                                                       
        return s


class GPSError(object):
    '''
    Class representing a GPS error from the gps_error file.
    '''
    def __init__(self, linestr):
        self.error = linestr.strip()

    def __repr__(self):
        s = "<mariachi.data.GPSError>" 
        return s
    
    def __str__(self):
        s = "GPSError: %s" % self.error
        return s


class WeatherRecord(object):
    '''
    Class representing weather from a single point in time.
    Generalized to handle arbitrary lengths of records.
    
    '''
    def __init__(self,linestr, tzinfo=None):
        linestr = linestr.strip()  # get rid of null chars
        logobject.debug('data.WeatherRecord(): Using line %s' % linestr)
        self.fields = []
        fieldlist = linestr.split(",")
        logobject.debug('data.WeatherRecord(): Split line: %s' % fieldlist)
        for i in range(0, len(fieldlist)):
            self.fields.append(fieldlist[i])
        self.datetime = _parse_iso(self.fields[0], tzinfo)
        self.fields[0] = str(self.datetime)
        logobject.debug('data.WeatherRecord(): Successfully set datetime: %s' % self.datetime)
    

    def __repr__(self):
        s = "<mariachi.data.WeatherRecord>" 
        return s

    def _abbrStr(self):
        s = "<mariachi.data.WeatherRecord>"
        return s

    def _fullStr(self):
        #s = "<mariachi.data.WeatherRecord>\n"
        s = ','.join(self.fields)
        #s = s[:-1] # chop off last comma 
        return s

    def __str__(self):
        '''
          String representation of this object in CSV. Using full info after user request.    
        '''
        return self._fullStr()

    def fullAsUTC(self):
        from pytz import timezone
        tz = timezone('UTC') 
        self.fields[0] = str(self.datetime.astimezone(tz))[:-6] # remove +00:00
        s = ','.join(self.fields)
        #s = s[:-1] # chop off last comma 
        return s
      
    
    
class ParseException(Exception):
    pass

class NanoTime(datetime.time):
    '''
    Time object with greater accuracy (x.x microseconds )
    year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]
    
    '''
    
    def __init__(self, year, month, day, hour=0, minute=0,second=0, microsecond=0, tzinfo=None ):
        pass

class NanoTimeDelta(datetime.timedelta):
    pass


# A UTC class.
ZERO = datetime.timedelta(0)
class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
utc = UTC()


class SiteFileHandler(object):
    '''
    Class which handles all the operations on a single site. 
    self.rootdir points to the site's data dir. 
    Selects relevant subsets of files, and parses them with 
      
    '''
    def __init__(self, directory=None):
        self.rootdir=directory
           
    def getData(self, type, start, end):
        '''
        Selective data retrieval. Gets the type requested and filters by date.
        Start and end dates/times must be Python datetime objects. 
                 
        '''
        #(counts, events, errors) = self._getAll()
        #logobject.debug("getData(): Prior to filtering: len(counts) = %d" % len(counts))
        #logobject.debug("getData(): Prior to filtering: len(events) = %d" % len(events))
        
        
        datalist = []
        returnlist = []
        
        filelist = self._getFilteredFileList(type, start, end)        
        datalist = self._parseFiles(filelist)
        for item in datalist:
            if item.datetime > start and item.datetime < end:
                returnlist.append(item)
                logobject.debug("data.getData(): Item %s between %s and %s. Keeping..." % (item.datetime, start, end) )
            else:
                logobject.debug("data.getData(): Item %s not between %s and %s. Skipping..." % (item.datetime, start, end) )
        logobject.info("data.getData(): Got data list of %d items, filtered to %d." % (len(datalist),len(returnlist) ))
        return returnlist
    
    def _getFilteredFileList(self, type, start, end ):
        '''
            Creates a list of *files* of the specified type that are from 
            the requested interval. 
            Returns a Python list of the filenames
        
        '''
        if type in SDTYPES:
            datadir="%s%s" % (self.rootdir, SDSUBDIR) 
        elif type in WTHRTYPES:
            datadir="%s%s" % (self.rootdir, WTHRSUBDIR) 
        else:
            logobject.error("SiteFileHandler._getFilteredFileList: Invalid type %s" % type)
            
        logobject.debug("SiteFileHandler._getFilteredFileList: Listing %s" % datadir)
        filestoread=[]    
        files = os.listdir(datadir)
        for fn in files:
            (head, bfn) = os.path.split(fn)
            logobject.debug("_getFilteredFileList(): File base name is %s" % bfn)
            # Is it the right type?   Is it from the right time?
            if self._matchFile(type, bfn) and self._checkDate(bfn, start, end):
                filestoread.append("%s/%s" % (datadir,fn))
                logobject.debug("_getFilteredFileList(): File %s kept in." % bfn)
            else:
                logobject.debug("_getFilteredFileList(): File %s filtered out." % bfn)
        
        logobject.info("data._getFilteredFileList(): Got list of %d files." % len(filestoread))    
        filestoread.sort()
        logobject.debug("data._getFilteredFileList(): Sorted files: %s" % filestoread)
        return filestoread    

    def _checkDate(self, basename, start, end):
        '''
            Checks to see if a single file could contain data from the desired start->end period. 
            Returns boolean
            start and end are Python DateTime objects.
            
        '''
        # DATEGLOB="\d+"
        logobject.debug("SiteFileHandler._checkDate(): Base name is %s" % basename)
        ret = False
        r = DATERE
        m = r.search(basename)
        if m:
            datestr = basename[m.start():m.end()]
        if len(datestr) == 8:
            logobject.debug("SiteFileHandler._checkDate(): Date part is %s" % datestr)
            y = int(datestr[:4])
            m = int(datestr[4:6])
            d = int(datestr[6:])
            logobject.debug("SiteFileHandler._checkDate(): Made datetimes for file X-%d%d%d " % (y,m,d))
            #dt = datetime.datetime(y,m,d,tzinfo=utc)
            dt_early = datetime.datetime(y,m,d, 0 , 0, 0 , tzinfo=None)
            oneday = datetime.timedelta(1)
            dt_early = dt_early - oneday
            logobject.debug("SiteFileHandler._checkDate(): dt_early is %s" % dt_early)
            dt_late =  datetime.datetime(y,m,d, 23,59,59, tzinfo=None)
            dt_late = dt_late + oneday
            logobject.debug("SiteFileHandler._checkDate(): dt_late is %s" % dt_late)

            # if the start of the desired period is *after* the last possible data contained in this file,
            # it shouldn't be used. 
            if start >= dt_late:
                logobject.debug("SiteFileHandler._checkDate(): File %s is not in interval." % basename)
                return False
            # if the end of the desired preiod is *before* the earliest possible data contained in this 
            # file, it shouldn't be used. 
            if end <= dt_early:
                logobject.debug("SiteFileHandler._checkDate(): File %s is not in interval." % basename)
                return False
            
            # If not removed, then it should be kept. 
            logobject.info("SiteFileHandler._checkDate(): File %s is in interval." % basename )
            return True

       
    def _matchFile(self, type, basename):
        '''
        Determines if filename matches right data type. 
        
        '''
        # COUNTSGLOB="counts-*.txt"
        # EVENTGLOB="timestamps-*.txt"
        # ERRGLOB="gps_error-*.txt"
        logobject.debug("SiteFileHandler._matchFiles(): checking base name is %s" % basename)
        ret = False
        p = FILENAMERES[type]
        m = p.match(basename)
        if m:
            logobject.debug("SiteFileHandler._matchFiles(): basename %s matched!" % basename)
            ret = True
        else:
            logobject.debug("SiteFileHandler._matchFiles(): basename %s didn't match." % basename)
        return ret


    def _parseFiles(self, filelist):
        '''
        Parses all data files in filelist, and returns list of objects therein.
        Contract: Assumes that all *files* passed in as argument represent a single type, 
        e.g. counts or events. 
        '''
        datalist = []
        
        for fn in filelist:
            f = open(fn)
            (head, bfn) = os.path.split(fn)
            lines = f.readlines()
            for line in lines:
                t = line[0:3]
                if t == "gts":
                    try:
                        ev = Event(line)
                        datalist.append(ev)
                    except Exception, e:
                        logobject.warn("SiteFileHandler._parseFiles(): Bad timestamps line %s in file %s exception: %s" % (line, fn, e))

                elif t == "cts":
                    try:
                        cr = CountsRecord(line)
                        datalist.append(cr)
                    except Exception, e:
                        logobject.warn("SiteFileHandler._parseFiles(): Bad counts line: %s in file %s exception: %s" % (line, fn, e))
                
                elif bfn[0:3] == "gps" and line[0] == "#":
                    # probably a gps error
                    try:
                        ge = GPSError(line)
                        datalist.append(ge)
                    except Exception, e:
                        logobject.warn("SiteFileHandler._parseFiles(): Bad GPS line %s in file %s exception: %s" (line,fn, e))
                else:
                    try:
                        wr = WeatherRecord(line)
                        datalist.append(wr)
                    except Exception, e:
                        logobject.warn("SiteFileHandler._parseFiles(): Error %s, Coudn't parse %s in file %s" % (e,line, fn))
        return datalist


class DataHandler(object):
    
    def __init__(self, config):
        self.config = config
    
    def generateCountsGraph(self, counts, sitename, widthpx=648, resol=72,  ):
        '''
            Static function to generate graph file via R.
            Graphs *all* of the counts records contained in counts List
        
    
        '''
        from rpy import r as robj
              
        # Calculate graph image information
        widthpx = int(widthpx)
        imgwidth = int( float(widthpx) / float(resol) )      
        ratio = float(self.config.get('data','graphratio'))
        imgheight =  int( (float(widthpx) * ratio) / float(resol) ), 
                
        counts_data = {"datetime":[],
                     "c1":[]}
        (fd, tmpgraphfile)= mkstemp()
        logobject.debug("DataHandler.generateCountsGraph(): Temp graph filename = %s" % tmpgraphfile)
    
        for cr in counts:
                #logobject.debug("%s" % c)
                epochsecs = time.mktime(cr.datetime.timetuple())
                counts_data["datetime"].append(  epochsecs  )
                #counts_data["datetime"].append( "%s" % c.datetime   )
                #logobject.debug("Datetime %s converted to epoch %d" % (c.datetime, epochsecs ))
                counts_data["c1"].append(cr.c1)

        
        cts = counts_data['c1']
        ctm = counts_data['datetime']
        if len(cts) > 0:
            robj.bitmap(tmpgraphfile, 
                     type = "png256", 
                     width = imgwidth , 
                     height = imgheight,
                     res = resol,
                     )
        
            ymin = int(self.config.get('data','counts.graph.ylim.min'))
            ymax = int(self.config.get('data','counts.graph.ylim.max'))
            robj.plot(ctm, cts, 
                       col="black", 
                       main="Counts: %s" % sitename ,
                       xlab="Time: (secs since 1970)", 
                       ylab="Counts/min",
                       type="l",
                       ylim=(ymin,ymax)
                       )
            robj.dev_off()
            import imghdr
            imgtype = imghdr.what(tmpgraphfile)
            logobject.debug("DataHandler.generateCountsGraph(): OK: What is our tempfile? = %s" % tmpgraphfile )
            f = open(tmpgraphfile)
        else:
            logobject.debug("DataHandler.generateCountsGraph(): No data. Generating proper error image...")
            #logobject.debug("DataHandler.generateCountsGraph(): Temp error image filename = %s" % tmpgraphfile)
            
            #import Image
            #import imghdr
            #imf = Image.open(self.config.get('data','nodatapng'))
            #imf.save(tmpgraphfile)
                        
            #imgtype = imghdr.what(tmpgraphfile)
            #logobject.debug("DataHandler.generateCountsGraph(): ERROR: What is our tempfile? = %s" % imgtype )
            f = open(self.config.get('data','nodatapng'))
        return f
            

##################################################################
#
# Private function definitions...
#
##################################################################

def _parse_iso(timestring, tzinfo ):
    '''
    Parses 2008-02-01 13:56:00 info Python datetime object in UTC (or as specified TZ).
    
    '''
    logobject.debug('data._parse_iso(): About to parse date into timestamp: %s' % timestring)
    (ymd,hms) = timestring.split(' ')
    (y,m,d) = ymd.split('-')
    (h,mn,s) = hms.split(':')
    logobject.debug('data._parse_iso(): Extracted year=%s month=%s day=%s hour=%s min=%s sec=%s' % (y,m,d,h,mn,s) )
    dt = datetime.datetime(int(y),
                               int(m),
                               int(d),
                               int(h),
                               int(mn),
                               int(s),
                               0, 
                               tzinfo=tzinfo)    
    logobject.debug('data._parse_iso(): Parsed date into datetime: %s' % dt )
    return dt
        


def _parse_datetime(ymd, hms):
    '''
    Takes information in the form easily extractable from Mariachi data files
    and creates Python datetime objects from it. 
    
    '''
    
    #logobject.debug("mariachi.data._parse_datetime(): YMD is %s" % ymd)
    year = int(ymd[0:4])
    #logobject.debug("mariachi.data._parse_datetime(): Year is %s" % year )
    
    month = int(ymd[4:6])
    #logobject.debug("mariachi.data._parse_datetime(): Month is %s" % month )
    
    day = int(ymd[6:8])
    #logobject.debug("mariachi.data._parse_datetime(): Day is %s" % day )
    
    #logobject.debug("mariachi.data._parse_datetime(): HMS is %s" % hms)
    hours = int(hms[0:2])
    #logobject.debug("mariachi.data._parse_datetime(): Hours is %s" % hours )
    
    mins = int(hms[2:4])
    #logobject.debug("mariachi.data._parse_datetime(): Minutes is %s" % mins )
    
    secs = int(hms[4:6])
    #logobject.debug("mariachi.data._parse_datetime(): Whole seconds is %s" % secs ) 
    
    decs = int(hms[7:])
    #logobject.debug("mariachi.data._parse_datetime(): Decimal seconds  is %s" % decs )
    
    microsecs = int(hms[7:-1])
    #logobject.debug("mariachi.data._parse_datetime(): Decimal seconds  is %s" % microsecs )
     
    dt = datetime.datetime( year, month, day , hours, mins, secs, microsecs, None)
    #logobject.debug("mariachi.data._parse_datetime(): Datetime object %s" % dt )
    return dt

#################################3
#
# Utility funcitons
#
##################################






################################################################
#
# Command line application/testing rig
#
################################################################
if __name__ == "__main__":
    print "Testing Mariachi Data Parser..." 
    import os
    import sys
    import getopt
    
    #defaults
    debug=0
    info=0
    warn=1
    directory="/home/jhover/devel/mariachi-data-ws/test/testsite"
    
    usage = """Usage: mariachi/data.py [OPTIONS] [COMMANDS] 
OPTIONS: 
    -h --help                    Print this message
    -d --debug                   Debug messages
    -v --verbose                 Verbose information
""" 

    # Handle command line options
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 
                                   "hdvD:", 
                                   ["help", 
                                    "debug", 
                                    "verbose",
                                    "directory", 
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
        elif opt in ("-D", "--directory"):
            directory = arg
        elif opt in ("-v", "--verbose"):
            info = 1
    
    if debug:
        logobject.setLevel(logging.DEBUG)
    elif info:
        logobject.setLevel(logging.INFO)
    elif warn:
        logobject.setLevel(logging.WARN)
    
    sfh = SiteFileHandler(directory)
       
    (events, counts, gpserrors) = sfh.getAll()
    for e in events:
        print e
    for c in counts:
        print c
    for g in gpserrors:
        print g
    
    print "%d Event objects" % len(events)
    print "%d CountsRecord objects" % len(counts)
    print "%d GPSError objects" % len(gpserrors)
                    
    