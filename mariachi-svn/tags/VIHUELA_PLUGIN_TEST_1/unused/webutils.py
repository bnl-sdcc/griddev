#
# various web upload/download utilities
# configured for easy use...
#
#
# This code and recipies were found via 
#   http://www.hackorama.com/python/upload.shtml
#

### remove this after RPM install to system paths...
import sys, logging
sys.path.append('/home/jhover/devel/mariachi-uploadd/')

"""
Client side authentication w/ SSL recipe:
  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117004

"""
log = logging.getLogger("root")

# Check python version 
major, minor, release, st, num = sys.version_info
log.debug('webutils.py: Found python %d.%d' % (major, minor) )  
if major ==  2 and minor >= 4:
    import myurllib224 as urllib2
elif major == 2 and minor == 3:
    import myurllib223 as urllib2


    
# HTTP example
def httpGet(url):
    
    response = urllib2.urlopen(url).read().strip()
    return response 

# HTTPS example
def httpsGet(url):

    response = urllib2.urlopen(url).read().strip()
    return response 

#
# WORKS!
#
def urllibx509httpsGet(_cert_file,_key_file,url):
    import urllib
    log.debug('webutils.urllibx509httpsGet(): making opener')
    opener= urllib.URLopener(key_file = _key_file, cert_file= _cert_file )
    log.debug('webutils.urllibx509httpsGet(): opener keyfile is %s'% opener.key_file)
    log.debug('webutils.urllibx509httpsGet(): opener certfile is %s' % opener.cert_file )
    log.debug('webutils.urllibx509httpsGet(): opening url...')
    response = opener.open(url, data=None)
    log.debug('webutils.urllibx509httpsGet(): returning response')
    return response.read()

#
# WORKS!
#
def httplibx509httpGet(_certfile,_keyfile,_hostname,_hostpath):
    import httplib
    conn = httplib.HTTPSConnection(host=_hostname, key_file = _keyfile, cert_file=_certfile)
    conn.putrequest('GET',_hostpath)    
    conn.endheaders()
    response = conn.getresponse()
    return response.read()

#
# Works with custom urllib2!
#
def urllib2x509httpsGet( url, _cert_file, _key_file):
    urllib2.HTTPSHandler.certfile = _cert_file
    urllib2.HTTPSHandler.keyfile = _key_file
    urllib2.HTTPSHandler.strict = None  
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    f = urllib2.urlopen(url)
    return f.read()
  
    
# HTTP + MULTIPART example
#def httpMultipartUpload(url, username, password, filename):
#    import urllib2
#    from mariachi import MultipartPostHandler
#
#    params = {userName : password ,'file':open( filename , 'rb')}
#    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
#    urllib2.install_opener(opener)
#    req = urllib2.Request( url , params)
#    response = urllib2.urlopen(req).read().strip()
#    return response 
#
#'''
#Form design for mod_gridsite directory. 
#
#<form 
#       method=post 
#       action="/gridsite/gridsite-admin.cgi" 
#       enctype="multipart/form-data">
#        <tr>
#                <td colspan=8><hr width="75%"></td>
#        </tr>
#        <tr>
#                <td rowspan=2>Upload file:</td>
#                <td colspan=2>New name:</td>
#                <td colspan=6>
#                        <input  type=text name=file size=25> 
#                        <input  type=submit value=Upload>
#                </td>
#        </tr>
#        <tr>
#                <td colspan=2>Local name:</td>
#                <td colspan=6>
#                        <input type=file name=uploadfile size=25>
#                </td>
#        </tr>
#</form>
#
#'''
#

def httpsMultipartUpload(url, filename, _cert_file, _key_file):
    # HTTPS + MULTIPART example
    # This is customized for mod_gridsite uploads...
    gridsite_cgi = "gridsite-admin.cgi"
    
    
    log.debug('webutils.httpsMultipartUpload(): \n    URL:  %s\n    filename: %s' % ( url, filename) )
    from mariachi import MultipartPostHandler
    
    log.debug('webutils.httpsMultipartUpload(): Setting x509. cert=%s, key=%s'  % ( _cert_file, _key_file) )
    urllib2.HTTPSHandler.certfile = _cert_file
    urllib2.HTTPSHandler.keyfile = _key_file
    urllib2.HTTPSHandler.strict = None
    
    params = {'filename' : filename , 'uploadfile':open(filename, 'rb')}
    log.debug('webutils.httpsMultipartUpload():  params:   %s'  %  params )
    
    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
    urllib2.install_opener(opener)
    
    url = url + gridsite_cgi
    log.debug('webutils.httpsMultipartUpload():  CGI upload URL:  %s'  % url )
    
    response = opener.open(url, params)
    #req = urllib2.Request(url, params)
    #response = urllib2.urlopen(req).read().strip()
    return response 
#
def httpProxyGet(url, _http_proxy ):
    # HTTP + PROXY example
    log.debug('webutils.httpProxyGet(): Begin fetching URL: %s' % url)
    
    urllib2.HTTPSHandler.certfile = "/home/jhover/.globus/usercert.pem"
    urllib2.HTTPSHandler.keyfile = "/home/jhover/.globus/userkeynopw.pem"
    urllib2.HTTPSHandler.strict = None  
    
    proxyurl = 'http://%s' % _http_proxy
    log.debug('webutils.httpProxyGet(): Adding proxy: %s' % proxyurl)
    proxy_support = urllib2.ProxyHandler({"http" : proxyurl })
    log.debug('webutils.httpProxyGet(): making opener')
    opener = urllib2.build_opener(proxy_support)
    log.debug('webutils.httpProxyGet(): installing opener...')
    urllib2.install_opener(opener)
    log.debug('webutils.httpProxyGet(): making Request...')

    req = urllib2.Request(url)
    response = urllib2.urlopen(req).read().strip()
    return response 
#
def httpsProxyGet(url, _cert_file, _key_file, _http_proxy ):
    # HTTPS + PROXY example
    #import urllib2
    log.debug('webutils.httpsProxyGet(): Begin fetching URL: %s' % url)
    from mariachi.ProxyHTTPConnection import ConnectHTTPSHandler,ConnectHTTPHandler
    
    urllib2.HTTPSHandler.certfile = _cert_file
    urllib2.HTTPSHandler.keyfile = _key_file
    urllib2.HTTPSHandler.strict = None  
    
    proxyurl = 'http://%s' % _http_proxy
    log.debug('webutils.httpsProxyGet(): Adding proxy: %s' % proxyurl)
    proxy_support = urllib2.ProxyHandler({"http" : proxyurl })
    log.debug('webutils.httpsProxyGet(): making opener')
    opener = urllib2.build_opener(proxy_support, ConnectHTTPHandler, ConnectHTTPSHandler)
    log.debug('webutils.httpsProxyGet(): installing opener...')
    urllib2.install_opener(opener)
    log.debug('webutils.httpsProxyGet(): making Request...')
    req = urllib2.Request(url)
    log.debug('webutils.httpsProxyGet(): calling urlopen(Request)')
    response = urllib2.urlopen(req).read().strip()
    return response 


#
#def httpsProxyMultipartUpload(url, username, password, filename):
#    # HTTPS + PROXY + MULTIPART example
#    import urllib2
#    from mariachi import MultipartPostHandler
#    from mariachi.ProxyHTTPConnection import ConnectHTTPSHandler
#    
#    params = {username:password,'file':open(filename, 'rb')}
#    opener = urllib2.build_opener(ConnectHTTPSHandler, 
#                MultipartPostHandler.MultipartPostHandler)
#    urllib2.install_opener(opener)
#    req = urllib2.Request(url, params)
#    req.set_proxy('proxyserver:8888', 'https')
#    response = urllib2.urlopen(req).read().strip()
#    return response     
    