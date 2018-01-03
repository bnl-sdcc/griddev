#
# WebDAV copy library
#
#  
#
#
#
import easywebdav
import urllib2
from urlparse import urlparse
from urlparse import urlsplit

class CopyEndpoint(object):
    
    def __init__(self, scheme, host, username, port, protocol, password, pathfile):
        self.scheme = scheme
        self.host = host
        self.username = username
        self.port =port
        self.password = password
        self.pathfile = pathfile
    

class WebdavCopy(object):

    def __init__(self, config, source, destination):
        self.log = logging.getlogger()
        self.config = config
        self.source = source
        self.dest = destinaton
        self.srcobj = self.parselocation(self, self.source)
        self.destobj = self.parselocation(self, self.destination)
        self.log.info("WebdavCopy Object initialized.")
        
    def parselocation(self, locstring):
        '''
        Returns a copyobject
          c.scheme [file|http|https]
          c.host   <host>|None
          c.port   <port>|None
          c.username 
          c.protocol
        
        '''
        self.log.debug("Parsing location %s" % locstring)
        if "@" in locstring:
            (username, locstring) = locstring.split('@')
                
        sr = urlparse.urlsplit(locstring)
        # scheme netloc path 
        scheme = sr.scheme
        if scheme =='':
            scheme = 'file'
        netloc = sr.netloc
        pathfile = sr.path

        host = None
        port = None
        if ':' in netloc:
            (host, port) = netloc.split(':')   
        else:
            host = netloc
            if scheme == 'https':
                port = 443
            elif scheme == 'http':
                port = 80
        
        if scheme != 'file':
            password = getpass.getpass(prompt='Password for %s:%s' % (username, host))

        ce = CopyEndpoint(scheme, host, username, port, password, pathfile)
        return ce
        
    def docopy(self):
        # verify_ssl=True
        if 'http' in self.srcobj.scheme:
            self.log.info("Downloading from web...")
            swd = easywebdav.connect( host=self.srcobj.host,
                                     username=self.srcobj.username,
                                     port=self.srcobj.port,
                                     protocol=self.srcobj.scheme,
                                     password=self.srcobj.password, 
                                     )        
            print(swd.exists(self.srcobj.pathfile))
            swd.download(self.srcobj.pathfile, self.dstobj.pathfile)
            
        elif 'http' in self.dstobj.scheme:
            self.log.info("Uploading to web...")
            dwd = easywebdav.connect( host=self.dstobj.host,
                                     username=self.dstobj.username,
                                     port=self.dstobj.port,
                                     protocol=self.dstobj.scheme,
                                     password=self.dstobj.password, 
                                     )        
            print(dwd.exists(self.dstobj.pathfile))
            dwd.upload(self.srcobj.pathfile, self.dstobj.pathfile)
    
            
            #print webdav.cd("/data/"
            #print webdav._get_url("")
            #print webdav.ls()
            # print webdav.exists("/dav/test.py")
            # print webdav.exists("ECS.zip")
            # print webdav.download(_file, "./"+_file)
            # print webdav.upload("./test.py", "test.py")