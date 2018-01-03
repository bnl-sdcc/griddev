#
#
# mod_python data web service for the MARIACHI project
# http://www.mariachi.stonybrook.edu
#
# Author: John R. Hover <jhover@bnl.gov>
#
#
#########################################################################
from ConfigParser import ConfigParser
from mariachiws.data import SiteFileHandler,DataHandler
import sys
import os
import logging
import time
import tempfile
import datetime

# Read in config file
config=ConfigParser()
config.read(['/etc/mariachi/mariachi-ws.conf','/home/jhover/devel/mariachi-data-ws/config/mariachi-ws.conf' ])
logfilename= config.get('global','logfile')


MIMEHTML="text/html"
MIMETXT="text/plain"
MIMEJPG="image/jpeg"
MIMESGML="text/sgml"
MIMEPNG="image/png"
MIMEBMP="image/bmp"
MIMEPDF="appplication/pdf"

# Check python version 
major, minor, release, st, num = sys.version_info

# Set up logging, handle differences between Python versions... 
# In Python 2.3, logging.basicConfig takes no args
#
FORMAT="%(asctime)s [ %(levelname)s ] %(message)s"
if major == 2 and minor ==3:
    logging.basicConfig()
else:
    logging.basicConfig(filename='%s' % logfilename, format=FORMAT)

log = logging.getLogger()
loglev = config.get('global','loglevel').lower()

if loglev == 'debug':
    log.setLevel(logging.DEBUG)
elif loglev == 'info':
    log.setLevel(logging.INFO)
elif loglev == 'warn':
    log.setLevel(logging.WARN)

log.debug("Logging initialized with logfile %s" % logfilename)

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



def graphAllSites(req, hours=48, width=640):
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    from time import strptime


    datadir="%s" % config.get('global','sites_root')
    sites = os.listdir(datadir)
    sitestodisplay = []
    for s in sites:
        if not s[0] == ".":
            sitestodisplay.append(s)
        
    req.add_common_vars()
    req.content_type=MIMEHTML
    req.add_common_vars()
    req.write('''
              <html>
                  <head>
                      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                      <title>Mariachi Live Data</title>
               ''')
    
    sitestodisplay.sort()
    for s in sitestodisplay:
        req.write("<br>")
        req.write(' <img src="/mariachi-ws/dataquery/query?site=%s&hours=%d&graph=1&width=%d" alt="Graph for site %s" />' % ( s, int(hours),int(width), s ))
        req.write("<br>")
               
    req.write('''
                </html>
    
                ''')       


def query(req,site="testsite",start="2008-01-01T12:01:30",end="now",datatype="all",hours=0,graph=0,width=648):
    '''
    Arguments:
    site:     official site name, e.g. testsite, smithtown, rockypoint, etc. [testsite]
    start:    a standard datetime string: "2005-12-06T12:13:14"
    end:     "now" is OK, or a standard datetime string: 
    type:    "all", or one or more of [ counts events errors], comma-separated
    graph:   0=false, 1=true  Return either tabulated data (txt) or graph
    
    '''
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    from time import strptime

    req.add_common_vars()
    #
    # Handle time parameters...
    #
    (y,m,d,h,mn,s) = time.strptime(start, "%Y-%m-%dT%H:%M:%S")[0:6] 
    #starttime= datetime.datetime(y,m,d,h,mn,s,tzinfo=utc)
    starttime= datetime.datetime(y,m,d,h,mn,s,tzinfo=None)      
    now = datetime.datetime.utcnow()
    
    if end == "now":
        endtime = now
    else:
        #try:
        (y,m,d,h,mn,s) = time.strptime(end, "%Y-%m-%dT%H:%M:%S")[0:6] 
        #endtime= datetime.datetime(y,m,d,h,mn,s,tzinfo=utc) 
        endtime= datetime.datetime(y,m,d,h,mn,s,tzinfo=None)      
        #except:
    
    if hours:
        seconds = int(hours) * 60 * 60
        tdelta = datetime.timedelta(seconds=seconds)
        starttime = now - tdelta
                       
    log.info("Site %s selected.\n" % site )
    log.info("Type %s selected.\n" % datatype)
   
    dir = "%s/%s" % (config.get("global","sites_root"), site )
    datatypes=[]
    
    if datatype=="all":
        #datatypes = [ 'counts','events','errors']
        datatypes = [ 'counts','events']
    else:
        datatypes = datatype.split(',')
    log.debug("Datatypes is %s" % datatypes)
    
    if graph:
        datatypes = ['counts']
        
    sfh = SiteFileHandler(dir)
    dh = DataHandler(config)
       
    # Dict to hold lists of objects, indexed by type 'counts','events','errors'
    dataobjs = {}  
    
    for d in datatypes:
        dataobjs[d] = sfh.getData(d, starttime, endtime)
    
    if graph:
        # Right now we only create graphs of counts.   
        f = dh.generateCountsGraph(widthpx=width , 
                                   counts=dataobjs['counts'], 
                                   sitename=site
                                   )
        req.content_type=MIMEPNG
        req.add_common_vars()
        data = f.read()
        req.write(data)
        
    else:
        req.content_type=MIMETXT
        #
        # For now, just grab everything
        #
        #(events, counts, gpserrors) = sfh.getAll()
        if "events" in datatypes:
            for e in dataobjs['events']:
                req.write("%s" % e)
        if "counts" in datatypes:    
            for c in dataobjs['counts']:
                req.write("%s\n" % c)        
        if "errors" in datatypes:
            for g in dataobjs['errors']:
                req.write("%s\n" % g )
    return  

#def django_query(req,site="testsite",datatype="all",startyear,startmonth,startday,starthour,startminute,endyear,endmonth,endday,endhour,endminute ):
#    pass


def django_query(starttime, endtime, sitename, format, datatype ):
    '''
    Non-request-based method for use by Django
    starttime, endtime are Python DateTime objects.
    sitename, datatype, format are strings
    format=['txt'|'graph']
    datatype=['counts'|'events'|'errors']

    Returns string or PNG graph file object

    '''
    
    
    log.debug("dataquery.django_query(): Begin...")
    dir = "%s/%s" % (config.get("global","sites_root"), sitename )
    sfh = SiteFileHandler(dir)
    dh = DataHandler(config)
    dataobjs = sfh.getData(datatype, starttime, endtime)

    if format == "graph":
        log.debug("dataquery.django_query(): Graph requested...")
        width=900
    # Right now we only create graphs of counts.   
        pngfile = dh.generateCountsGraph(widthpx=width , 
                                   counts=dataobjs, 
                                   sitename=sitename
                                   )
        return pngfile
    elif format == "txt":
        log.debug("dataquery.django_query(): Text requested...")
        answerstr = ""
        for item in dataobjs:
            answerstr += "%s\n" % item
        return answerstr
                
        

def test(req):
    return "OK"

def status(req):
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    from mariachi import modpystatus 

    req.content_type=MIMEHTML 
    req.add_common_vars() 
    r=modpystatus.modPyStats() 
    r.status(req) 
    req.write(r.page) 
    return apache.OK 