#!/usr/bin/env python
#
# Data file interface library for MARIACHI Project.
# http://www.mariachi.stonybrook.edu
# 
# This module/package focusses on the internals, file formats, and abstract representation
# of mariachi data. 
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

SDTYPES=['counts','events','errors']
SDSUBDIR="/sd"
RADIOSUBDIR="/radio"

COUNTSGLOB="counts-\d*.txt"
EVENTGLOB="timestamps-\d*.txt"
ERRGLOB="gps_error-\d*.txt"
WTHRGLOB="weather-\d*.csv"

# this works in bash:  '[[:alpha:]]\+[[:digit:]]\+U\.wav'
RADIOGLOB="[A-Za-z]+\d+U.wav"

DATEGLOB="\d+"

WTHRTYPES=['weather',]
WTHRSUBDIR="/weather"

DATERE= re.compile(DATEGLOB, re.IGNORECASE)

FILENAMERES = { 'counts' : re.compile(COUNTSGLOB, re.IGNORECASE),
                'events' : re.compile(EVENTGLOB, re.IGNORECASE),
                'errors' :  re.compile(ERRGLOB, re.IGNORECASE),
                'weather' : re.compile(WTHRGLOB, re.IGNORECASE),
                'radio' : re.compile(RADIOGLOB, re.IGNORECASE),               
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
        log = logging.getLogger()
        linestr = linestr.strip()  # get rid of null chars
        log.debug('Using line %s' % linestr)
        self.fields = []
        fieldlist = linestr.split(",")
        log.debug('Split line: %s' % fieldlist)
        for i in range(0, len(fieldlist)):
            self.fields.append(fieldlist[i])
        self.datetime = _parse_iso(self.fields[0], tzinfo)
        self.fields[0] = str(self.datetime)
        log.debug('Successfully set datetime: %s' % self.datetime)
    

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

class RadioFile(object):
    '''
    Object to contain all information about a radio/WAV file. 
    Source filenames are in the form: 
    
    CCCYYMMDDHHU.wav   where CCC is the sitecode and U just means UTC
    
    Other files will be in the form
    
    CCCYYMMDDHH
    
    
    sox WCU08042923U.wav -e stat
        Samples read:         155758592
        Length (seconds):   3531.940862
        Scaled by:         2147483647.0
        Maximum amplitude:     0.352844
        Minimum amplitude:    -0.353790
        Midline amplitude:    -0.000473
        Mean    norm:          0.007974
        Mean    amplitude:    -0.000010
        RMS     amplitude:     0.012974
        Maximum delta:         0.494507
        Minimum delta:         0.000000
        Mean    delta:         0.011009
        RMS     delta:         0.018289
        Rough   frequency:         4946
        Volume adjustment:        2.827

    3531.940862
    3531.847982
    3531.940862
    '''
    
    def __init__(self, path):
        self.path = path
        (head, self.filename) = os.path.split(path)
        # Calculate start time from the filename
        self.starttime = self._parseTime(self.filename)
        # Calculate end time using shntool/ shninfo 
        self.endtime = self.starttime +  datetime.timedelta(seconds = 3531.9)   
        self.sitecode = None
        
    
    def _parseTime(self, filename):
        '''
        Assumes specific filename convention. CCCYYMMDDHHU.wav 
        
        returns Python DateTime object set to proper time. 
        '''
        (base, ext) = os.path.splitext(filename)
        if len(base) == 12:
            self.sitecode = base[:3]
            self.year = 2000 + int(base[3:5])
            self.month = int(base[5:7])
            self.day = int(base[7:9])
            self.hour = int(base[9:11])
            self.zonecode = base[11]
            return datetime.datetime(self.year,self.month,self.day,self.hour,0,0,tzinfo=None) 
        else:
            raise Exception("Filename basename %s is wrong length." % base)
    

    def _calcWavDuration(self, filename):
        pass
 
    def _setStartTime(self):
        
        (head, ext) = os.path.splitext(self.path)
        fn = os.path.basename(head)
        
        (y,m,d,h,mn,s) = time.strptime(start, "%Y-%m-%dT%H:%M:%S")
        #starttime= datetime.datetime(y,m,d,h,mn,s,tzinfo=utc)
        starttime= datetime.datetime(y,m,d,h,mn,s,tzinfo=None)    
    
    def _setEndTime(self):
        pass
        
        


class SiteRadioHandler(object):
    '''
    Radio file-oriented version of SiteFileHandler
    
    
    '''
    
    def __init__(self, dir=None):
        self.rootdir=dir
        
    def getFile(self, datetimeobj):
        '''
        Takes a Python datetime and retrieves RadioFile *containing* that time. We are going to assume that if 
        a source file contains the start it will also contain the end. (big source files, desire for tiny durations 
        within them).   
 
        Returns a Radiofile containing provided datetime.
        Returns None if no corresponding file exists.
        
        '''
        log = logging.getLogger()
        allrfs = self._getWavFiles()
        answer = None
        for rf in allrfs:
            if rf.starttime < datetimeobj and rf.endtime > datetimeobj:
                answer = rf
        return answer
    
    
    def _getWavFiles(self):
        '''
        List directory and makes RadioFiles out of .wav files. 
        
        '''
        datadir="%s%s" % (self.rootdir, RADIOSUBDIR) 
        files = os.listdir(datadir)
        p = FILENAMERES['radio']
        radiofiles = []
        for f in os.listdir(datadir):
            if p.match(f): 
                fname = "%s/%s" % ( datadir, f)
                rf = RadioFile(fname)
                radiofiles.append(rf)
        return radiofiles
        
   
    
    
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
        log = logging.getLogger()
        #(counts, events, errors) = self._getAll()
        #log.debug("getData(): Prior to filtering: len(counts) = %d" % len(counts))
        #log.debug("getData(): Prior to filtering: len(events) = %d" % len(events))
        
        
        datalist = []
        returnlist = []
        
        filelist = self._getFilteredFileList(type, start, end)        
        datalist = self._parseFiles(filelist)
        for item in datalist:
            if item.datetime > start and item.datetime < end:
                returnlist.append(item)
                log.debug("Item %s between %s and %s. Keeping..." % (item.datetime, start, end) )
            else:
                log.debug("Item %s not between %s and %s. Skipping..." % (item.datetime, start, end) )
        log.info("Got data list of %d items, filtered to %d." % (len(datalist),len(returnlist) ))
        return returnlist
    
    def _getFilteredFileList(self, type, start, end ):
        '''
            Creates a list of *files* of the specified type that are from 
            the requested interval. 
            Returns a Python list of the filenames
        
        '''
        log = logging.getLogger()
        
        if type in SDTYPES:
            datadir="%s%s" % (self.rootdir, SDSUBDIR) 
        elif type in WTHRTYPES:
            datadir="%s%s" % (self.rootdir, WTHRSUBDIR) 
        else:
            log.error("Invalid type %s" % type)
            
        log.debug("Listing %s" % datadir)
        filestoread=[]    
        files = os.listdir(datadir)
        for fn in files:
            (head, bfn) = os.path.split(fn)
            log.debug("File base name is %s" % bfn)
            # Is it the right type?   Is it from the right time?
            if self._matchFile(type, bfn) and self._checkDate(bfn, start, end):
                filestoread.append("%s/%s" % (datadir,fn))
                log.debug("File %s kept in." % bfn)
            else:
                log.debug("File %s filtered out." % bfn)
        
        log.info("Got list of %d files." % len(filestoread))    
        filestoread.sort()
        log.debug("Sorted files: %s" % filestoread)
        return filestoread    

    def _checkDate(self, basename, start, end):
        '''
            Checks to see if a single file could contain data from the desired start->end period. 
            Returns boolean
            start and end are Python DateTime objects.
            
        '''
        log = logging.getLogger()
        # DATEGLOB="\d+"
        log.debug("Base name is %s" % basename)
        ret = False
        r = DATERE
        m = r.search(basename)
        if m:
            datestr = basename[m.start():m.end()]
        if len(datestr) == 8:
            log.debug("Date part is %s" % datestr)
            y = int(datestr[:4])
            m = int(datestr[4:6])
            d = int(datestr[6:])
            log.debug("Made datetimes for file X-%d%d%d " % (y,m,d))
            #dt = datetime.datetime(y,m,d,tzinfo=utc)
            dt_early = datetime.datetime(y,m,d, 0 , 0, 0 , tzinfo=None)
            oneday = datetime.timedelta(1)
            dt_early = dt_early - oneday
            log.debug("dt_early is %s" % dt_early)
            dt_late =  datetime.datetime(y,m,d, 23,59,59, tzinfo=None)
            dt_late = dt_late + oneday
            log.debug("dt_late is %s" % dt_late)

            # if the start of the desired period is *after* the last possible data contained in this file,
            # it shouldn't be used. 
            if start >= dt_late:
                log.debug("File %s is not in interval." % basename)
                return False
            # if the end of the desired preiod is *before* the earliest possible data contained in this 
            # file, it shouldn't be used. 
            if end <= dt_early:
                log.debug("File %s is not in interval." % basename)
                return False
            
            # If not removed, then it should be kept. 
            log.info("File %s is in interval." % basename )
            return True

       
    def _matchFile(self, type, basename):
        '''
        Determines if filename matches right data type. 
        
        '''
        log = logging.getLogger()
        # COUNTSGLOB="counts-*.txt"
        # EVENTGLOB="timestamps-*.txt"
        # ERRGLOB="gps_error-*.txt"
        log.debug("Checking base name is %s" % basename)
        ret = False
        p = FILENAMERES[type]
        m = p.match(basename)
        if m:
            log.debug("Basename %s matched!" % basename)
            ret = True
        else:
            log.debug("Basename %s didn't match." % basename)
        return ret


    def _parseFiles(self, filelist):
        '''
        Parses all data files in filelist, and returns list of objects therein.
        Contract: Assumes that all *files* passed in as argument represent a single type, 
        e.g. counts or events. 
        '''
        log = logging.getLogger()
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
                        log.warn("Bad timestamps line %s in file %s exception: %s" % (line, fn, e))

                elif t == "cts":
                    try:
                        cr = CountsRecord(line)
                        datalist.append(cr)
                    except Exception, e:
                        log.warn("Bad counts line: %s in file %s exception: %s" % (line, fn, e))
                
                elif bfn[0:3] == "gps" and line[0] == "#":
                    # probably a gps error
                    try:
                        ge = GPSError(line)
                        datalist.append(ge)
                    except Exception, e:
                        log.warn("Bad GPS line %s in file %s exception: %s" (line,fn, e))
                else:
                    try:
                        wr = WeatherRecord(line)
                        datalist.append(wr)
                    except Exception, e:
                        log.warn("Error %s, Coudn't parse %s in file %s" % (e,line, fn))
        return datalist

class RadioDataHandler(object):
    '''
        Radio counterpart to DataHandler. 
    '''
    
    
    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger()

    def slicewav(self, radiofile, start=60, duration=5):
        '''
        
        Uses sox
         
         sox <inputfile>  <outputfile> trim start duration
        
        
        radiofile=rf, start=0, duration=10
        Arguments:
        radiofile    File name of radiofile to slice
        start        Seconds into the file to begin
        duration     Seconds to slice out
        
        returns name? of properly named file containing sliced wav
        '''
        self.log.debug("Trying to slice wav file %s , start = %s , duration = %s" %(radiofile, start, duration))
        import commands
        (fd, tmpfilename) = mkstemp()
        
        cmd = "sox %s -t wav %s trim %s %s" % (radiofile.path, tmpfilename, start, duration)
        self.log.debug("Executing command %s" % cmd)
        (s,o) = commands.getstatusoutput(cmd)
        self.log.debug("Command status = %s, output = %s" % (s,o) )
        self.log.debug("Returning tempfile name %s" % tmpfilename)       
        return tmpfilename


class DataHandler(object):
    
    def __init__(self, config):
        self.config = config
    
    def generateCountsGraph(self, counts, sitename, widthpx=648, resol=72,  ):
        '''
            Static function to generate graph file via R.
            Graphs *all* of the counts records contained in counts List
        
    
        '''
        log = logging.getLogger()
        from rpy import r as robj
        
        log.info('Generating graph for %d counts from site %s' % (len(counts), sitename))
              
        # Calculate graph image information
        widthpx = int(widthpx)
        imgwidth = int( float(widthpx) / float(resol) )      
        ratio = float(self.config.get('data','graphratio'))
        imgheight =  int( (float(widthpx) * ratio) / float(resol) ), 
                
        counts_data = {"datetime":[],
                     "c1":[]}
        (fd, tmpgraphfile)= mkstemp()
        log.debug("Temp graph filename = %s" % tmpgraphfile)
    
        for cr in counts:
                #log.debug("%s" % c)
                epochsecs = time.mktime(cr.datetime.timetuple())
                counts_data["datetime"].append(  epochsecs  )
                #counts_data["datetime"].append( "%s" % c.datetime   )
                #log.debug("Datetime %s converted to epoch %d" % (c.datetime, epochsecs ))
                counts_data["c1"].append(cr.c1)

                # cr.datetime = "2008-02-11 12:07:08.112117"
       
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
            log.debug("DataHandler.generateCountsGraph(): OK: What is our tempfile? = %s" % tmpgraphfile )
            f = open(tmpgraphfile)
        else:
            log.debug("DataHandler.generateCountsGraph(): No data. Generating proper error image...")
            f = open(self.config.get('data','nodatapng'))
        return f

    def generateCountsGraph2(self, counts, sitename, widthpx=648, resol=72,  ):
            '''
                Static function to generate graph file via R.
                Graphs *all* of the counts records contained in counts List
                This one uses more in-R processing to handle dates/times (since
                Rpy doesn't do automatic conversions). 
            '''
            log = logging.getLogger()
            log.info('Generating graph for %d counts from site %s' % (len(counts), sitename))
            
            from rpy import r as robj
                 
            # Calculate graph image information
            ratio = float(self.config.get('data','graphratio'))
            widthpx = int(widthpx)
            imgwidth = int( float(widthpx) / float(resol) )      
            imgheight =  int( ( (float(widthpx) * ratio) / float(resol)) ) 
            resol = int(resol)

            # Get unused file/name to put image data into...
            (fd, tmpgraphfile)= mkstemp()
            log.debug("Temp graph filename = %s" % tmpgraphfile)        
            
            # Unpack CountsRecords into counts and timestamps. 
            cts = []
            ctm = []
            for cr in counts:
                    # cr.datetime = "2008-02-11 12:07:08.112117"
                    # cr.c1 = 5440
                    cts.append(cr.c1)
                    ctm.append(str(cr.datetime))
            
            log.debug("Got list of %d counts." % len(cts))
            
            # If there is data for a graph, import into R.
            if len(cts) > 0:
                robj.assign('rcts', cts)
                robj.assign('rctm', ctm)
                
                # Convert timestamps to POSIXct objects within R. 
                # datpt <- as.POSIXct(strptime(dat,format="%Y-%m-%d %H:%M:%S"))
                robj('''rctmpct <- as.POSIXct(strptime(rctm, format="%Y-%m-%d %H:%M:%S"))''')
                cmdstring = 'bitmap( "%s", type="png256", width=%s, height=%s, res=%s)' % (tmpgraphfile, imgwidth, imgheight,resol)
                log.debug("R cmdstring is %s" % cmdstring)
                robj(cmdstring )
                log.debug("Completed R command string %s" % cmdstring)
            
                ymin = int(self.config.get('data','counts.graph.ylim.min'))
                ymax = int(self.config.get('data','counts.graph.ylim.max'))
                #xlabel = " ctm[%s] -- ctm[%s] " % ("0",str( len(ctm)-1))
                xlabel = " %s -- %s " % (ctm[0], ctm[len(ctm)-1])
                cmdstring = 'plot( rctmpct, rcts, col="black",main="Counts: %s", xlab="Dates:  %s",ylab="Counts/min",type="l", ylim=c(%d,%d) )' % (sitename,xlabel,ymin, ymax )
                log.debug("R cmdstring is %s" % cmdstring)
                robj(cmdstring)
                log.debug("Completed R command string %s" % cmdstring)
                robj.dev_off()
                
                
                
                # Pull written image and return to caller
                import imghdr
                imgtype = imghdr.what(tmpgraphfile)
                log.debug("OK: What is our tempfile? = %s" % tmpgraphfile )
                f = open(tmpgraphfile)
            else:
                log.debug("No data. Generating proper error image...")
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
    log = logging.getLogger()
    log.debug('About to parse date into timestamp: %s' % timestring)
    (ymd,hms) = timestring.split(' ')
    (y,m,d) = ymd.split('-')
    (h,mn,s) = hms.split(':')
    log.debug('Extracted year=%s month=%s day=%s hour=%s min=%s sec=%s' % (y,m,d,h,mn,s) )
    dt = datetime.datetime(int(y),
                               int(m),
                               int(d),
                               int(h),
                               int(mn),
                               int(s),
                               0, 
                               tzinfo=tzinfo)    
    log.debug('Parsed date into datetime: %s' % dt )
    return dt
        


def _parse_datetime(ymd, hms):
    '''
    Takes information in the form easily extractable from Mariachi data files
    and creates Python datetime objects from it. 
    
    '''
    log = logging.getLogger()
    #log.debug("mariachi.data._parse_datetime(): YMD is %s" % ymd)
    year = int(ymd[0:4])
    #log.debug("mariachi.data._parse_datetime(): Year is %s" % year )
    
    month = int(ymd[4:6])
    #log.debug("mariachi.data._parse_datetime(): Month is %s" % month )
    
    day = int(ymd[6:8])
    #log.debug("mariachi.data._parse_datetime(): Day is %s" % day )
    
    #log.debug("mariachi.data._parse_datetime(): HMS is %s" % hms)
    hours = int(hms[0:2])
    #log.debug("mariachi.data._parse_datetime(): Hours is %s" % hours )
    
    mins = int(hms[2:4])
    #log.debug("mariachi.data._parse_datetime(): Minutes is %s" % mins )
    
    secs = int(hms[4:6])
    #log.debug("mariachi.data._parse_datetime(): Whole seconds is %s" % secs ) 
    
    decs = int(hms[7:])
    #log.debug("mariachi.data._parse_datetime(): Decimal seconds  is %s" % decs )
    
    microsecs = int(hms[7:-1])
    #log.debug("mariachi.data._parse_datetime(): Decimal seconds  is %s" % microsecs )
     
    dt = datetime.datetime( year, month, day , hours, mins, secs, microsecs, None)
    #log.debug("mariachi.data._parse_datetime(): Datetime object %s" % dt )
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
    import logging
    
    log = logging.getLogger()
    
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
        log.setLevel(logging.DEBUG)
    elif info:
        log.setLevel(logging.INFO)
    elif warn:
        log.setLevel(logging.WARN)
    
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
                    
    