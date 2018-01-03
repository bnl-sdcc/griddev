#!/usr/bin/env python2.4
#
#  Vihuela Data Acquisition Plugin
#  Created for the MARIACHI Project 
# http://www-mariachi.physics.sunysb.edu/
#
# Inspiration and recipes from 
#   http://www.hackorama.com/python/upload.shtml
#   http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
#
# MARIACHI Author:
#   John Hover <jhover@bnl.gov>
#
# Other code from:
#   Will Holcomb <wholcomb@gmail.com>
#   Fabien Seisen: <fabien@seisen.org>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
"""
Usage:
 Set of classes to manage data upload from remote collection 
 nodes. Data upload is recieved by a mod_gridsite protected 
 path on a main server. 
 
 
  
"""
import vihuela
import os, stat, sys, logging, threading, signal, time, sets
import mimetools, mimetypes, urllib, sgmllib

log = logging.getLogger()

# Check python version 
major, minor, release, st, num = sys.version_info
log.debug('vihuela.plugins.GridsitePlugin: Found python %d.%d' % (major, minor) )  
if major ==  2 and minor >= 4:
    import myurllib224 as urllib2
else:
    log.fatal('vihuela.plugins.GridsitePlugin: This module requires Python 2.4')
    sys.exit(0)


class GridsitePlugin(vihuela.core.Plugin):
    """
    Represents a single source root and destination root that is meant to be kept 
    in sync, ensuring that anything on the client is also present on the server 
    (but not vice versa). This syncronization includes all subdirectories of each 
    root. 

    Every <interval> seconds, this class will do a comparison of files present,
    and their sizes, and upload files that exist on the source but not the 
    destination AND re-upload files on the source which are larger than that on 
    the destination
    
    See grst_admin_main.c in org.grisite.core/src in the gridsite sources to see CGI 
    parameter handling. 
        
    
    """
    def __init__(self, config,section,cgiscript="gridsite-admin.cgi"):
        super(GridsitePlugin, self).__init__(config,section)
        self.log.debug("vihuela.daq.GridsiteUploader.__init__()..." )
        self.klassname="vihuela.plugins.GridsitePlugin"
        self.certfile = config.get(section,'cert_file')
        self.keyfile = config.get(section,'key_file')
        self.strict= config.get(section,'strict')
        self.upload_host = config.get(section,'upload_host')
        self.base_path = config.get(section,'upload_base')
        self.local_base = config.get(section,'local_base')

        self.cgi_exec = cgiscript
        self.httpproxy= '%s:%s' % ( config.get('daemon', 'httpproxy_host'), 
                       config.get('daemon','httpproxy_port')
                       )
       
    def run_action(self):
        self.run_upload()

    def run_upload(self):
        """
       Compares local files (and dirs) vs. remote files (and dirs) and sends only files 
       (and dirs) not already fully uploaded to remote location. Uses both file path+name
       and file size to determine unfinished/undone uploads.  
        
       """
        self.log.debug("vihuela.plugins.GridsiteUploader.run_upload(): Beginning run...")
        
        remotestat = 0
        try:
            remotefiles = self._getRemoteFileSet("/")
            remotestat = 1
        except IOError:
            self.log.error('vihuela.plugins.GridsiteUploader.run_upload(): Problem connecting to remote URL. Check network, proxies, config.')
        
        if remotestat:
            localfiles = self._getLocalFileSet()
            sendset = localfiles.difference(remotefiles)
    
            # debug assessment
            self.log.debug('vihuela.plugins.gridsiteUploader.run_upload(): Got remote set: %s ' % remotefiles)
            self.log.debug('vihuela.plugins.gridsiteUploader.run_upload(): Got local set: %s ' % localfiles)
            
            # We can't do sendset.sort(), so we have to make a list
            sendlist = []
            for i in sendset:
                sendlist.append(i)
            sendlist.sort()
            self.log.debug('vihuela.plugins.gridsiteUploader.run_upload(): Got send list: %s ' % sendlist)
            if len(sendlist) == 0:
                self.log.info('vihuela.plugins.gridsiteUploader.run_upload(): [%s] No files to send.' % self.section )
            try:
                for f in sendlist:
                    if f.type == 'dir':
                        self._mkDir(f.filename)
                        self.log.info('%s.run_upload(): [%s] Made directory: %s ' % (self.klassname, self.section, f.filename) )
                    else:
                        self._uploadFile(f.filename)
                        self.log.info('%s.run_upload(): [%s] Uploaded file %s' % (self.klassname, self.section, f.filename) )
            except IOError:
                self.log.debug('vihuela.plugins.gridsiteUploader.run_upload(): Problem uploading file. Check remote URL config, permissions.')
    
    
    def _strip_localbase(self, fullpath):
        '''Remove local base path from full path in order to make local and remote files comparable.'''
        return fullpath.replace(self.local_base, '')
    
          
    def _uploadFile(self, filename):
        """
        Uploads a single file from sourcedir to destdir as specified for this
        uploader.
        
        """
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): Setting x509...')
        urllib2.HTTPSHandler.certfile = self.certfile
        urllib2.HTTPSHandler.keyfile = self.keyfile
        urllib2.HTTPSHandler.strict = self.strict
        
        # build localfilename to open
        fullpath = "%s/%s" % ( self.local_base , filename )
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): Uploading %s' % fullpath)
 
        # filename e.g. "/subdir/newsubdir"
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): Uploading %s' % filename)
        (parents,newfile) = os.path.split(filename)
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): parents = %s tail=%s' % (parents,newfile))
        
        # build CGI URL
        url = "https://%s%s" % (self.upload_host, self.base_path)
                
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): URL step 1: %s' % url)
        if parents and len(parents) > 1:
            url = "%s%s/" % ( url, parents)
        else:
            url = "%s/" % url
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): URL step 2: %s' % url)
        url = "%s%s" % (url, self.cgi_exec)
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile(): URL step 3: %s' % url)
        
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile():  CGI upload URL:  %s'  % url )
        
         
        opener = urllib2.build_opener(MultipartPostHandler)
        urllib2.install_opener(opener)

        params = {'filename' : filename , 'uploadfile':open(fullpath, 'rb')}
        self.log.debug('vihuela.plugins.gridsiteUploader._uploadFile():  params:   %s'  %  params )
              
        response = opener.open(url, params)
        return response
    
    
    def _mkDir(self, newname):
        """
        Creates a new directory of newname.
        
        """
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): Setting x509.')
        urllib2.HTTPSHandler.certfile = self.certfile
        urllib2.HTTPSHandler.keyfile = self.keyfile
        urllib2.HTTPSHandler.strict = self.strict
        
        
        # newname e.g. "/subdir/newsubdir"
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): Creating %s' % newname)
        (parents,newdir) = os.path.split(newname)
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): parents = %s tail=%s' % (parents,newdir))
        
        # build CGI URL
        url = "https://%s%s" % (self.upload_host, self.base_path)
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): URL step 1: %s' % url)
        if parents and len(parents) > 1:
            url = "%s%s/" % ( url, parents)
        else:
            url = "%s/" % url
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): URL step 2: %s' % url)
        url = "%s%s" % (url, self.cgi_exec)
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir(): URL step 3: %s' % url)

        # debug info
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir():  CGI upload URL:  %s'  % url )
        params = { 'cmd' : 'edit' ,  'button' : 'Create', 'file' : newdir }
        self.log.debug('vihuela.plugins.gridsiteUploader._mkDir():  params:   %s'  %  params )
        
        #execute directory creation
        opener = urllib2.build_opener(MultipartPostHandler)
        urllib2.install_opener(opener)        
        response = opener.open(url, params)
        return response
    
        
    def _getRemoteFileSet(self, dirpath):
        """
        Returns a Set of files in remote directory. Calls itself recursively on subdirectories,
        and returns final result Set of UploadFile objects. 

        """
        self.log.debug('vihuela.plugins.gridsiteUploader._getRemoteFileSet():...')
        rfs = sets.Set()
        listing = self._listDir(dirpath)
        #self.log.debug('vihuela.plugins.gridsiteUploader._getRemoteFileSet(): Response %s' % listing )
        
        p = GridsiteParser()
        p.parse(listing)
        files = p.get_files()
        dirs = p.get_dirs()
        for f in files:
            filename = "%s%s" % (dirpath, f[0])
            ulf = UploadFile( filename, int(f[1]) )
            self.log.debug('vihuela.plugins.gridsiteUploader._getRemoteFileSet(): File: %s' % f )
            rfs.add(ulf)
        for d in dirs:
            dname = "%s%s" % (dirpath, d[0])
            uld = UploadFile( dname, int(d[1]), file_type="dir")
            rfs.add(uld)
            self.log.debug('vihuela.plugins.gridsiteUploader._getRemoteFileSet(): Dir: %s' % d )
            rfs.union_update(self._getRemoteFileSet("%s%s/" % (dirpath, d[0])))
        
        #self.log.debug('vihuela.plugins.gridsiteUploader._getRemoteFileSet(): Got set: %s' % rfs)
        return rfs


    def _listDir(self,dirpath):
        '''
        Parses a file/directory listing for a single gridsite path relative to this Uploaders base path
       
        '''
        self.log.debug('vihuela.plugins.gridsiteUploader._listDir(): Listing remote dir path: %s' % dirpath )
  
        fullpath="%s%s" % ( self.base_path , dirpath )
        self.log.debug('vihuela.plugins.gridsiteUploader._listDir(): Listing path:%s' % fullpath)
        
        opener= urllib.URLopener(key_file = self.keyfile, cert_file= self.certfile )
        url = "https://%s/%s" %(self.upload_host,fullpath )
        response = opener.open(url, data=None)
        log.debug('vihuela.plugins.gridsiteUploader._listDir(): returning response')
        return response.read()
       
         
        
       

    def _getLocalFileSet(self):
        """
        Returns a Set of files in remote directory. Throws exception for errors. 
        """
        self.log.debug('vihuela.plugins.gridsiteUploader._getLocalFileSet(): ...')
        lfs = sets.Set()
        self.log.debug('vihuela.plugins.gridsiteUploader._getLocalFileSet(): local_base is %s' % self.local_base)
        for root, dirs, files in os.walk(self.local_base):
            for d in dirs:
                fd = os.path.join(root,d)
                si = os.stat(fd)
                rd = self._strip_localbase(fd)
                ud = UploadFile(rd, si.st_size, file_type="dir") 
                lfs.add(ud)
                
            for f in files:
                self.log.debug('vihuela.plugins.gridsiteUploader._getLocalFileSet(): checking file %s' % f )
                ff = os.path.join(root,f)
                si = os.stat(ff)
                rf = self._strip_localbase(ff)
                uf = UploadFile(rf, si.st_size, file_type="file" )
                lfs.add(uf)
        #self.log.debug('vihuela.plugins.gridsiteUploader._getLocalFileSet(): Got local set %s' % lfs)
        return lfs

       
        
class GridsiteParser(sgmllib.SGMLParser):
    "A simple parser class. Parses the directory listings on a Gridsite URL."
    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.files = []
        self.directories = []
        
    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."
        link = None
        length = None
        for name, value in attributes:
            if name == "href":
                link = value
            elif name == "content-length":
                length = value
        if link and length:
            if link[-1] == "/" :
                fixedlink = link[:-1]
                self.directories.append([fixedlink , length])
            else:
                self.files.append([ link, length])        

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def get_files(self):
        "Return the list of files."
        return self.files

    def get_dirs(self):
        '''Return the list of directories.'''
        return self.directories
    
    

class UploadFile(object):
    """
    Represents a file or directory entry beneath an upload root, either locally or remotely 
    e.g. names like "/fileinroot", "/subdir", "/subdir/fileinsubdir".
    Comparison is meant to work with Sets, and should also sort() in such a way that all 
    directories come before files, and all no subdirectory will come before its parent. 
   
    """
    
    def __init__(self, file_name, file_size, file_type="file"):
        self.filename = file_name
        self.filesize = file_size
        self.type = file_type
    
    def __hash__(self):
        s = self.__repr__()
        return s.__hash__()
    
    def __eq__(self, other):
        if self.type != other.type:
            return 0
        namecmp = cmp(self.filename, other.filename)
        # directories are the same if they have the same name
        if self.type == 'dir' and namecmp == 0:
            return 1
        # files are the same if they share name and size
        if self.type == 'file':
            if namecmp == 0 and self.filesize == other.filesize:
                return 1
            else:
                return 0    
        
    def __cmp__(self, other):
        '''
        For sorting we want directories to always come first, sorted by path length (so no 
        directory can come before any of its parents. Otherwise, order is irrelevant. 
        
        '''
        #log.debug('UploadFile.__cmp__(): comparing %s  to %s ' % ( self, other) )
        
        
        # compare types
        #
        # self > other, return 1
        #
        if self.type != other.type:
            #log.debug('UploadFile.__cmp__(): self different type from other.')
            if self.type == "dir":
                retval = -1
                #log.debug('UploadFile.__cmp__(): retval = %d ' % retval )
                return retval
            else:
                retval = 1
                #log.debug('UploadFile.__cmp__(): retval = %d ' % retval )
                return retval
        # OK, dir vs. dir or file vs. file
        # compare names
        namecmp = cmp(self.filename, other.filename)
        
        #log.debug('UploadFile.__cmp__(): namecompare = %d ' % namecmp )
        
        if namecmp == 0:
            # if they have the same name, we only care about file size
            if self.type == 'file':
                retval =  cmp(self.filesize, other.filesize)
            elif self.type == 'dir':
                retval = 0
            #log.debug('UploadFile.__cmp__(): retval = %d ' % retval )
            return retval
        else:
            if self.type == "dir":
                # we care about path length
                retval =  len(self.filename) - len(other.filename)
                #log.debug('UploadFile.__cmp__(): retval = %d ' % retval )
                return retval
            else:
                # for files we don't really care. 
                retval = namecmp
                #log.debug('UploadFile.__cmp__(): retval = %d ' % retval )
                return retval

    def __repr__(self):
        if self.type == 'file':
            s = 'UploadFile: %s %d bytes' % ( self.filename, self.filesize) 
        elif self.type == 'dir':
            s = 'UploadDir: %s ' %  self.filename 
        return s


class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if request.has_header('Content-type'):
                    pass # print "Replacing %s with %s" % (request.get_header('content-type'), contenttype)
                request.add_unredirected_header('Content-type', contenttype)

            request.add_data(data)

        return request

        
    def multipart_encode(vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buffer is None:
            buffer = ''
        for(key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer += '\r\n' + fd.read() + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer
    multipart_encode = Callable(multipart_encode)

    https_request = http_request



        


#
# WORKS!
#
def urllibx509httpsGet(_cert_file,_key_file,url):

    log.debug('vihuela.plugins.urllibx509httpsGet(): making opener')
    opener= urllib.URLopener(key_file = _key_file, cert_file= _cert_file )
    log.debug('vihuela.plugins.urllibx509httpsGet(): opener keyfile is %s'% opener.key_file)
    log.debug('vihuela.plugins.urllibx509httpsGet(): opener certfile is %s' % opener.cert_file )
    log.debug('vihuela.plugins.urllibx509httpsGet(): opening url...')
    response = opener.open(url, data=None)
    log.debug('vihuela.plugins.urllibx509httpsGet(): returning response')
    return response.read()


def main():
    import tempfile, sys

    validatorURL = "http://validator.w3.org/check"
    opener = urllib2.build_opener(MultipartPostHandler)

    def validateFile(url):
        temp = tempfile.mkstemp(suffix=".html")
        os.write(temp[0], opener.open(url).read())
        params = { "ss" : "0",            # show source
                   "doctype" : "Inline",
                   "uploaded_file" : open(temp[1], "rb") }
        print opener.open(validatorURL, params).read()
        os.remove(temp[1])

    if len(sys.argv[1:]) > 0:
        for arg in sys.argv[1:]:
            validateFile(arg)
    else:
        validateFile("http://www.google.com")
        


if __name__=="__main__":
    pass
    #main()
