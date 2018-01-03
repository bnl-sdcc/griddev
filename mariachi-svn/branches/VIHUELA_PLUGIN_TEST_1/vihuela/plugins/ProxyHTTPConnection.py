#!/usr/bin/env python2.4
#
# This code and recipies were found via 
#   http://www.hackorama.com/python/upload.shtml
#
# urllib2 opener to connection through a proxy using the CONNECT 
# method, (useful for SSL)
# tested with python 2.4
#
   

import httplib
import logging
import socket
import sys
import urllib


log = logging.getLogger()

# Check python version for urllib2 import
major, minor, release, st, num = sys.version_info
log.debug('webutils.py: Found python %d.%d' % (major, minor) )  
if major ==  2 and minor >= 4:
    import myurllib224 as urllib2
elif major == 2 and minor == 3:
    import myurllib223 as urllib2


class ProxyHTTPConnection(httplib.HTTPConnection):

    _ports = {'http' : 80, 'https' : 443}


    def request(self, method, url, body=None, headers={}):
        #request is called before connect, so can interpret url and get
        #real host/port to be used to make CONNECT request to proxy
        log.debug('ProxyHTTPConnection.request(): method = %s ' % method)
        proto, rest = urllib.splittype(url)
        if proto is None:
            raise ValueError, "unknown URL type: %s" % url
        #get host
        host, rest = urllib.splithost(rest)
        #try to get port
        host, port = urllib.splitport(host)
        #if port is not defined try to get from proto
        if port is None:
            try:
                port = self._ports[proto]
            except KeyError:
                raise ValueError, "unknown protocol for: %s" % url
        self._real_host = host
        self._real_port = port
        log.debug('ProxyHTTPConnection.request(): _real_host = %s _real_port = %s ' % 
                  ( self._real_host, self._real_port ) )
        httplib.HTTPConnection.request(self, method, url, body, headers)
        

    def connect(self):
        log.debug('ProxyHTTPConnection.connect(): Called...' )
        log.debug('ProxyHTTPConnection.connect(): Called superclass connect()' )
        httplib.HTTPConnection.connect(self)
        log.debug('ProxyHTTPConnection.connect(): Sending CONNECT...' )
        #send proxy CONNECT request
        self.send("CONNECT %s:%d HTTP/1.0\r\n\r\n" % (self._real_host, self._real_port))
        #expect a HTTP/1.0 200 Connection established
        response = self.response_class(self.sock, strict=self.strict, method=self._method)
        log.debug('ProxyHTTPConnection.connect(): Got response...' )
        (version, code, message) = response._read_status()
        #probably here we can handle auth requests...
        if code != 200:
            #proxy returned and error, abort connection, and raise exception
            self.close()
            raise socket.error, "Proxy connection failed: %d %s" % (code, message.strip())
        #eat up header block from proxy....
        while True:
            log.debug('ProxyHTTPConnection.connect(): In read loop.' )
            #should not use directly fp probablu
            line = response.fp.readline()
            if line == '\r\n': break
        log.debug('ProxyHTTPConnection.connect(): Done. Returning...' )


class ProxyHTTPSConnection(ProxyHTTPConnection):
    
    default_port = 443

    def __init__(self, host, port = None, key_file = None, cert_file = None, strict = None):
        log.debug('ProxyHTTPConnection.ProxyHTTPSConnection.__init__()' )
        ProxyHTTPConnection.__init__(self, host, port)
        #self.key_file = key_file
        #self.cert_file = cert_file
        #self.strict = strict
        
        self.key_file = urllib2.HTTPSHandler.keyfile
        self.cert_file = urllib2.HTTPSHandler.certfile
        self.strict = urllib2.HTTPSHandler.strict
        log.debug('ProxyHTTPSConnection.ProxyHTTPSConnection.__init__(): keyfile = %s , cert_file = %s , strict = %s' % 
                  (self.key_file, self.cert_file, self.strict ) )

    
    def connect(self):
        log.debug('ProxyHTTPSConnection.connectt():Called... ' )
        ProxyHTTPConnection.connect(self)
        #make the sock ssl-aware
        ssl = socket.ssl(self.sock, self.key_file, self.cert_file)
        self.sock = httplib.FakeSocket(self.sock, ssl)
        
                                       
class ConnectHTTPHandler(urllib2.HTTPHandler):

    def do_open(self, http_class, req):
        log.debug('ConnectHTTPHandler.do_open():Called... ' )
        return urllib2.HTTPHandler.do_open(self, ProxyHTTPConnection, req)


class ConnectHTTPSHandler(urllib2.HTTPSHandler):

    def do_open(self, http_class, req):
        log.debug('ConnectHTTPSHandler.do_open():Called... ' )
        return urllib2.HTTPSHandler.do_open(self, ProxyHTTPSConnection, req)


if __name__ == '__main__':
    
    import sys, logging
    # Set up logging. 
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    log.debug("Testing ConnectHTTPHandler")
    
    test_url = '<URL:https://www-mariachi.physics.sunysb.edu/gridsite/>'
    cert_file = '/home/jhover/.globus/usercert.pem'
    key_file = '/home/jhover/.globus/userkeynopw.pem'
    
    log.debug('Setting x509. cert=%s, key=%s'  % ( cert_file, key_file) )
    urllib2.HTTPSHandler.certfile = cert_file
    urllib2.HTTPSHandler.keyfile =  key_file
    urllib2.HTTPSHandler.strict = None
    
    log.debug('Building Opener...')
    opener = urllib2.build_opener(ConnectHTTPHandler, ConnectHTTPSHandler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url=test_url )
    req.set_proxy('192.168.1.130:3128', 'https')
    log.debug( "Opening url %s" % test_url)
    f = urllib2.urlopen(req)
    print f.read()

