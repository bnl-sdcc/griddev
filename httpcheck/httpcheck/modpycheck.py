import pprint
import sys
import os 
from mod_python import Session 
from mod_python import util 
from mod_python import psp 
from mod_python import apache 


def test(req):
    return "OK"

def status(req):

    req.content_type="text/html" 
    req.add_common_vars() 
    req.write(simplestatus())   

    
def simplestatus():
    ans = ""
    ans += "<html>"
    ans += "<title>httpcheck</title>"
    ans += "<body>If you see this, it is working.</body>"  
    ans += "</html>"
    return ans

def modpystatus(req):       
    req.content_type="text/html" 
    req.add_common_vars() 
    r=modPyStats() 
    r.status(req) 
    
class modPyStats:
    __doc__ = """
modpystatus is a quick and dirty way to figure out what your script is doing, like PHP's phpinfo() page. 
just import modpystatus and add it to your page's output variables, like this:

from mod_python import Session 
from mod_python import util 
from mod_python import psp 
from mod_python import apache 
import modpystatus 

req.content_type="text/html" 
req.add_common_vars() 
r=modpystatus.modPyStats() 
r.status(req) 
req.write(r.page) 
return apache.OK

"""
    def __init__(self):
        
        self.stats= (
        ('string','allowed_xmethods',"""Tuple. Allowed extension methods. RO"""),
        ('string','allowed_methods',"""Tuple. List of allowed methods. Used in relation with <tt class=constant>METHOD_NOT_ALLOWED</tt>. This member can be modified via <ttclass=method>req.allow_methods()</tt> described in section <A href=pyapi-mprequest-meth.html>4.5.3</A>. RO"""),
        ('string','server',"""A server object associate with this request. See Server Object below for details. RO"""),
        ('string','request_time',"""A long integer. When request started. RO"""),
        ('string','next',"""If this is an internal redirect, the request object we redirect to. RO"""),
        ('string','prev',"""If this is an internal redirect, the request object we redirect from. RO"""),
        ('string','main',"""If this is a sub-request, pointer to the main request. RO"""),
        ('string','the_request',"""String containing the first line of the request. RO"""),
        ('string','assbackwards',"""Indicates an HTTP/0.9 ``simple'' request. This means that the response will contain no headers, only the body. Although this exists forbackwards compatibility with obsolescent browsers, some people have figred out that setting assbackwards to 1 can be a useful technique when including part of theresponse from an internal redirect to avoid headers being sent."""),
        ('string','proxyreq',"""A proxy request: one of <tt class=constant>apache.PROXYREQ_*</tt> values. RO"""),
        ('string','header_only',"""A boolean value indicating HEAD request, as opposed to GET. RO"""),
        ('string','protocol',"""Protocol, as given by the client, or <tt class=samp>HTTP/0.9</tt>. Same as CGI <a class=envvar name=l2h-106>SERVER_PROTOCOL</a>. RO"""),
        ('string','proto_num',"""Integer. Number version of protocol; 1.1 = 1001 RO"""),
        ('string','hostname',"""String. Host, as set by full URI or Host: header. RO"""),
        ('string','status_line',"""Status line. E.g. <tt class=samp>200 OK</tt>. RO"""),
        ('string','sent_bodyct',"""Integer. Byte count in stream is for body. (?) RO"""),
        ('string','bytes_sent',"""Long integer. Number of bytes sent. RO"""),
        ('string','mtime',"""Long integer. Time the resource was last modified. RO"""),
        ('string','chunked',"""Boolean value indicating when sending chunked transfer-coding. RO"""),
        ('string','range',"""String. The <code>Range:</code> header. RO"""),
        ('string','clength',"""Long integer. The ``real'' content length. RO"""),
        ('string','remaining',"""Long integer. Bytes left to read. (Only makes sense inside a read operation.) RO"""),
        ('string','read_length',"""Long integer. Number of bytes read. RO"""),
        ('string','read_body',"""Integer. How the request body should be read. RO"""),
        ('string','read_chunked',"""Boolean. Read chunked transfer coding. RO"""),
        ('string','expecting_100',"""Boolean. Is client waiting for a 100 (<tt class=constant>HTTP_CONTINUE</tt>) response. RO"""),
        ('mp_table','headers_in',"""A table object containing headers sent by the client."""),
        ('mp_table','headers_out',"""A <code>table</code> object representing the headers to be sent to the client."""),
        ('string','err_headers_out',"""These headers get send with the error response, instead of headers_out."""),
        ('mp_table','subprocess_env',"""A <code>table</code> object containing environment information typically usable for CGI. You may have to call <tt class=member>req.add_common_vars()</tt> first to fillin the information you need."""),
        ('mp_table','notes',"""A <code>table</code> object that could be used to store miscellaneous generalpurpose info that lives for as long as the request lives. If youneed to pass data between handlers,it's better to simply add members to the request object than to use <tt class=member>notes</tt>."""),
        ('string','phase',"""The phase currently being being processed, e.g. <tt class=samp>PythonHandler</tt>. <i>(Read-Only)</i>"""),
        ('string','interpreter',"""The name of the subinterpreter under which we're running. <i>(Read-Only)</i>"""),
        ('string','content_type',"""String. The content type. Mod_python maintains an internal flag (<tt class=member>req._content_type_set</tt>) to keep track of whether<tt class=member>content_type</tt>was set manually from within Python. The publisher handler uses this flag in the following way: when<tt class=member>content_type</tt>isn't explicitly set, it attempts to guess the content type by examining the first few bytes of the output."""),
        ('string','handler',"""The name of the handler currently being processed. This is the handler set bymod_mime, not the mod_python handler. In most cases it will be""<tt class=samp>mod_python</tt>. RO"""),
        ('string','content_encoding',"""String. Content encoding. RO"""),
        ('string','vlist_validator',"""Integer. Variant list validator (if negotiated). RO"""),
        ('string','user',"""If an authentication check is made, this will hold the user name. Same as CGI <aclass=envvar name=l2h-108>REMOTE_USER</a>. RO <div class=note><bclass=label>Note:</b><tt class=method>req.get_basic_auth_pw()</tt> must be called prior to using this value. </div>"""),
        ('string','ap_auth_type',"""Authentication type. Same as CGI <a class=envvar name=l2h-109>AUTH_TYPE</a>. RO"""),
        ('string','no_cache',"""Boolean. No cache if true. RO"""),
        ('string','no_local_copy',"""Boolean. No local copy exists. RO"""),
        ('string','unparsed_uri',"""The URI without any parsing performed. RO"""),
        ('string','uri',"""The path portion of the URI. RO"""),
        ('string','filename',"""String. File name being requested."""),
        ('string','canonical_filename',"""String. The true filename (<tt class=member>req.filename</tt> iscanonicalized if they don't match).  <i>(Read-Only)</i>"""),
        ('string','path_info',"""String. What follows after the file name, but is before query args, if anything. Same as CGI <a class=envvar name=l2h-110>PATH_INFO</a>.RO"""),
        ('string','args',"""String. Same as CGI <a class=envvar name=l2h-111>QUERY_ARGS</a>. RO"""),
        ('string','finfo',"""Tuple. A file information structure, analogous to POSIX stat, describing the file pointed to by the URI.  <code>(mode, ino,   dev, nlink, uid,gid, size, atime, mtime, ctime, fname,   name)</code>. The <code>apache</code> module defines a set of <tt class=constant>FINFO_*</tt> constants that should be used toaccess elements of this tuple. Example: <dl><dd><pre class=verbatim>
    
        fname = req.finfo[apache.FINFO_FNAME]
        </pre></dl> RO"""),
        ('string','parsed_uri',"""Tuple. The URI broken down into pieces. <code>(scheme, hostinfo, user, password, hostname, port, path, query, fragment)</code>. The<code>apache</code> module defines a set of<tt class=constant>URI_*</tt> constants that should be used to access elements of this tuple. Example: <dl><dd><preclass=verbatim>
    
        fname = req.finfo[apache.FINFO_FNAME]
        </pre></dl> RO"""),
        ('string','parsed_uri',"""Tuple. The URI broken down into pieces. <code>(scheme, hostinfo, user, password, hostname, port, path, query, fragment)</code>. The<code>apache</code> module defines a set of<tt class=constant>URI_*</tt> constants that should be used to access elements of this tuple. Example: <dl><dd><preclass=verbatim>
    
        fname = req.parsed_uri[apache.URI_PATH]
        </pre></dl> RO"""),
        ('string','used_path_info',"""Flag to accept or reject path_info on current request. RO"""),
        ('string','eos_sent',"""Boolean. EOS bucket sent. RO"""),
        ('connection','base_server',"""A <code>server</code> object for the physical vhost that this connection came in
          through.
          RO"""),
        ('connection','local_addr',"""The (address, port) tuple for the server.
          RO"""),
        ('connection','remote_addr',"""The (address, port) tuple for the client.
          RO"""),
        ('connection','remote_ip',"""String with the IP of the client. Same as CGI <a class=envvar name=l2h-130>REMOTE_ADDR</a>.
          RO"""),
        ('connection','remote_host',"""String. The DNS name of the remote client. None if DNS has not been
          checked, <code>""</code> (empty string) if no name found. Same as CGI <a class=envvar name=l2h-131>REMOTE_HOST</a>.
          RO"""),
        ('connection','remote_logname',"""Remote name if using RFC1413 (ident). Same as CGI <a class=envvar name=l2h-132>REMOTE_IDENT</a>.
          RO"""),
        ('connection','aborted',"""Boolean. True is the connection is aborted.
          RO"""),
        ('connection','keepalive',"""Integer. 1 means the connection will be kept for the next request, 0 means
          ``undecided'', -1 means ``fatal error''.
          RO"""),
        ('connection','double_reverse',"""Integer. 1 means double reverse DNS lookup has been performed, 0 means
          not yet, -1 means yes and it failed.
          RO"""),
        ('connection','keepalives',"""The number of times this connection has been used. (?)
          RO"""),
        ('connection','local_ip',"""String with the IP of the server.
          RO"""),
        ('connection','local_host',"""DNS name of the server.
          RO"""),
        ('connection','id',"""Long. A unique connection id.
          RO"""),
        ('connection','notes',"""A <code>table</code> object containing miscellaneous general purpose info that lives for as long as the connection lives."""),
        )
        self.apstats = (
        ('string','APLOG_ALERT','APLOG_ALERT'),
        ('string','APLOG_CRIT','APLOG_CRIT'),
        ('string','APLOG_DEBUG','APLOG_DEBUG'),
        ('string','APLOG_EMERG','APLOG_EMERG'),
        ('string','APLOG_ERR','APLOG_ERR'),
        ('string','APLOG_INFO','APLOG_INFO'),
        ('string','APLOG_NOERRNO','APLOG_NOERRNO'),
        ('string','APLOG_NOTICE','APLOG_NOTICE'),
        ('string','APLOG_WARNING','APLOG_WARNING'),
        ('string','AP_MPMQ_DYNAMIC','AP_MPMQ_DYNAMIC'),
        ('string','AP_MPMQ_HARD_LIMIT_DAEMONS','AP_MPMQ_HARD_LIMIT_DAEMONS'),
        ('string','AP_MPMQ_HARD_LIMIT_THREADS','AP_MPMQ_HARD_LIMIT_THREADS'),
        ('string','AP_MPMQ_IS_FORKED','AP_MPMQ_IS_FORKED'),
        ('string','AP_MPMQ_IS_THREADED','AP_MPMQ_IS_THREADED'),
        ('string','AP_MPMQ_MAX_DAEMONS','AP_MPMQ_MAX_DAEMONS'),
        ('string','AP_MPMQ_MAX_DAEMON_USED','AP_MPMQ_MAX_DAEMON_USED'),
        ('string','AP_MPMQ_MAX_REQUESTS_DAEMON','AP_MPMQ_MAX_REQUESTS_DAEMON'),
        ('string','AP_MPMQ_MAX_SPARE_DAEMONS','AP_MPMQ_MAX_SPARE_DAEMONS'),
        ('string','AP_MPMQ_MAX_SPARE_THREADS','AP_MPMQ_MAX_SPARE_THREADS'),
        ('string','AP_MPMQ_MAX_THREADS','AP_MPMQ_MAX_THREADS'),
        ('string','AP_MPMQ_MIN_SPARE_DAEMONS','AP_MPMQ_MIN_SPARE_DAEMONS'),
        ('string','AP_MPMQ_MIN_SPARE_THREADS','AP_MPMQ_MIN_SPARE_THREADS'),
        ('string','AP_MPMQ_NOT_SUPPORTED','AP_MPMQ_NOT_SUPPORTED'),
        ('string','AP_MPMQ_STATIC','AP_MPMQ_STATIC'),
        ('string','AP_REQ_ACCEPT_PATH_INFO','AP_REQ_ACCEPT_PATH_INFO'),
        ('string','AP_REQ_DEFAULT_PATH_INFO','AP_REQ_DEFAULT_PATH_INFO'),
        ('string','AP_REQ_REJECT_PATH_INFO','AP_REQ_REJECT_PATH_INFO'),
        ('string','CGIStdin','CGIStdin'),
        ('string','CGIStdout','CGIStdout'),
        ('string','CallBack','CallBack'),
        ('string','DECLINED','DECLINED'),
        ('string','DONE','DONE'),
        ('string','FINFO_ATIME','FINFO_ATIME'),
       ('string','FINFO_CTIME','FINFO_CTIME'),
        ('string','FINFO_DEV','FINFO_DEV'),
        ('string','FINFO_FNAME','FINFO_FNAME'),
        ('string','FINFO_GID','FINFO_GID'),
        ('string','FINFO_INO','FINFO_INO'),
        ('string','FINFO_MODE','FINFO_MODE'),
        ('string','FINFO_MTIME','FINFO_MTIME'),
        ('string','FINFO_NAME','FINFO_NAME'),
        ('string','FINFO_NLINK','FINFO_NLINK'),
        ('string','FINFO_SIZE','FINFO_SIZE'),
        ('string','FINFO_UID','FINFO_UID'),
        ('string','HTTP_ACCEPTED','HTTP_ACCEPTED'),
        ('string','HTTP_BAD_GATEWAY','HTTP_BAD_GATEWAY'),
        ('string','HTTP_BAD_REQUEST','HTTP_BAD_REQUEST'),
        ('string','HTTP_CONFLICT','HTTP_CONFLICT'),
        ('string','HTTP_CONTINUE','HTTP_CONTINUE'),
        ('string','HTTP_CREATED','HTTP_CREATED'),
        ('string','HTTP_EXPECTATION_FAILED','HTTP_EXPECTATION_FAILED'),
        ('string','HTTP_FAILED_DEPENDENCY','HTTP_FAILED_DEPENDENCY'),
        ('string','HTTP_FORBIDDEN','HTTP_FORBIDDEN'),
        ('string','HTTP_GATEWAY_TIME_OUT','HTTP_GATEWAY_TIME_OUT'),
        ('string','HTTP_GONE','HTTP_GONE'),
        ('string','HTTP_INSUFFICIENT_STORAGE','HTTP_INSUFFICIENT_STORAGE'),
        ('string','HTTP_INTERNAL_SERVER_ERROR','HTTP_INTERNAL_SERVER_ERROR'),
        ('string','HTTP_LENGTH_REQUIRED','HTTP_LENGTH_REQUIRED'),
        ('string','HTTP_LOCKED','HTTP_LOCKED'),
        ('string','HTTP_METHOD_NOT_ALLOWED','HTTP_METHOD_NOT_ALLOWED'),
        ('string','HTTP_MOVED_PERMANENTLY','HTTP_MOVED_PERMANENTLY'),
        ('string','HTTP_MOVED_TEMPORARILY','HTTP_MOVED_TEMPORARILY'),
        ('string','HTTP_MULTIPLE_CHOICES','HTTP_MULTIPLE_CHOICES'),
        ('string','HTTP_MULTI_STATUS','HTTP_MULTI_STATUS'),
        ('string','HTTP_NON_AUTHORITATIVE','HTTP_NON_AUTHORITATIVE'),
        ('string','HTTP_NOT_ACCEPTABLE','HTTP_NOT_ACCEPTABLE'),
        ('string','HTTP_NOT_EXTENDED','HTTP_NOT_EXTENDED'),
        ('string','HTTP_NOT_FOUND','HTTP_NOT_FOUND'),
        ('string','HTTP_NOT_IMPLEMENTED','HTTP_NOT_IMPLEMENTED'),
        ('string','HTTP_NOT_MODIFIED','HTTP_NOT_MODIFIED'),
        ('string','HTTP_NO_CONTENT','HTTP_NO_CONTENT'),
        ('string','HTTP_OK','HTTP_OK'),
        ('string','HTTP_PARTIAL_CONTENT','HTTP_PARTIAL_CONTENT'),
        ('string','HTTP_PAYMENT_REQUIRED','HTTP_PAYMENT_REQUIRED'),
        ('string','HTTP_PRECONDITION_FAILED','HTTP_PRECONDITION_FAILED'),
        ('string','HTTP_PROCESSING','HTTP_PROCESSING'),
        ('string','HTTP_PROXY_AUTHENTICATION_REQUIRED','HTTP_PROXY_AUTHENTICATION_REQUIRED'),
        ('string','HTTP_RANGE_NOT_SATISFIABLE','HTTP_RANGE_NOT_SATISFIABLE'),
        ('string','HTTP_REQUEST_ENTITY_TOO_LARGE','HTTP_REQUEST_ENTITY_TOO_LARGE'),
        ('string','HTTP_REQUEST_TIME_OUT','HTTP_REQUEST_TIME_OUT'),
        ('string','HTTP_REQUEST_URI_TOO_LARGE','HTTP_REQUEST_URI_TOO_LARGE'),
        ('string','HTTP_RESET_CONTENT','HTTP_RESET_CONTENT'),
        ('string','HTTP_SEE_OTHER','HTTP_SEE_OTHER'),
        ('string','HTTP_SERVICE_UNAVAILABLE','HTTP_SERVICE_UNAVAILABLE'),
        ('string','HTTP_SWITCHING_PROTOCOLS','HTTP_SWITCHING_PROTOCOLS'),
        ('string','HTTP_TEMPORARY_REDIRECT','HTTP_TEMPORARY_REDIRECT'),
        ('string','HTTP_UNAUTHORIZED','HTTP_UNAUTHORIZED'),
        ('string','HTTP_UNPROCESSABLE_ENTITY','HTTP_UNPROCESSABLE_ENTITY'),
        ('string','HTTP_UNSUPPORTED_MEDIA_TYPE','HTTP_UNSUPPORTED_MEDIA_TYPE'),
        ('string','HTTP_USE_PROXY','HTTP_USE_PROXY'),
        ('string','HTTP_VARIANT_ALSO_VARIES','HTTP_VARIANT_ALSO_VARIES'),
        ('string','HTTP_VERSION_NOT_SUPPORTED','HTTP_VERSION_NOT_SUPPORTED'),
        ('string','M_BASELINE_CONTROL','M_BASELINE_CONTROL'),
        ('string','M_CHECKIN','M_CHECKIN'),
        ('string','M_CHECKOUT','M_CHECKOUT'),
        ('string','M_CONNECT','M_CONNECT'),
        ('string','M_COPY','M_COPY'),
        ('string','M_DELETE','M_DELETE'),
        ('string','M_GET','M_GET'),
        ('string','M_INVALID','M_INVALID'),
        ('string','M_LABEL','M_LABEL'),
        ('string','M_LOCK','M_LOCK'),
        ('string','M_MERGE','M_MERGE'),
        ('string','M_MKACTIVITY','M_MKACTIVITY'),
        ('string','M_MKCOL','M_MKCOL'),
        ('string','M_MKWORKSPACE','M_MKWORKSPACE'),
        ('string','M_MOVE','M_MOVE'),
        ('string','M_OPTIONS','M_OPTIONS'),
        ('string','M_PATCH','M_PATCH'),
        ('string','M_POST','M_POST'),
        ('string','M_PROPFIND','M_PROPFIND'),
        ('string','M_PROPPATCH','M_PROPPATCH'),
       ('string','M_PUT','M_PUT'),
        ('string','M_REPORT','M_REPORT'),
        ('string','M_TRACE','M_TRACE'),
        ('string','M_UNCHECKOUT','M_UNCHECKOUT'),
        ('string','M_UNLOCK','M_UNLOCK'),
        ('string','M_UPDATE','M_UPDATE'),
        ('string','M_VERSION_CONTROL','M_VERSION_CONTROL'),
        ('string','NullIO','NullIO'),
        ('string','OK','OK'),
        ('string','PROG_TRACEBACK','PROG_TRACEBACK'),
        ('string','PROXYREQ_NONE','PROXYREQ_NONE'),
        ('string','PROXYREQ_PROXY','PROXYREQ_PROXY'),
        ('string','PROXYREQ_REVERSE','PROXYREQ_REVERSE'),
        ('string','REMOTE_DOUBLE_REV','REMOTE_DOUBLE_REV'),
        ('string','REMOTE_HOST','REMOTE_HOST'),
        ('string','REMOTE_NAME','REMOTE_NAME'),
        ('string','REMOTE_NOLOOKUP','REMOTE_NOLOOKUP'),
        ('string','REQ_ABORTED','REQ_ABORTED'),
        ('string','REQ_EXIT','REQ_EXIT'),
        ('string','REQ_NOACTION','REQ_NOACTION'),
        ('string','REQ_PROCEED','REQ_PROCEED'),
        ('string','SERVER_RETURN','SERVER_RETURN'),
        ('string','URI_FRAGMENT','URI_FRAGMENT'),
        ('string','URI_HOSTINFO','URI_HOSTINFO'),
        ('string','URI_HOSTNAME','URI_HOSTNAME'),
        ('string','URI_PASSWORD','URI_PASSWORD'),
        ('string','URI_PATH','URI_PATH'),
        ('string','URI_PORT','URI_PORT'),
        ('string','URI_QUERY','URI_QUERY'),
        ('string','URI_SCHEME','URI_SCHEME'),
        ('string','URI_USER','URI_USER'),
        ('string','__builtins__','__builtins__'),
        ('string','__doc__','__doc__'),
        ('string','__file__','__file__'),
        ('string','__name__','__name__'),
        #('string','_apache','_apache'),
        #('string','_path','_path'),
        #('string','build_cgi_env','build_cgi_env'),
        #('string','config_tree','config_tree'),
        #('string','imp','imp'),
        #('string','import_module','import_module'),
        #('string','init','init'),
        #('string','log_error','log_error'),
        #('string','make_table','make_table'),
        #('string','module_mtime','module_mtime'),
        #('string','mpm_query','mpm_query'),
        #('string','os','os'),
        #('string','pdb','pdb'),
        #('string','resolve_object','resolve_object'),
        #('string','restore_nocgi','restore_nocgi'),
        #('string','server_root','server_root'),
        #('string','setup_cgi','setup_cgi'),
        #('string','stat','stat'),
        #('string','sys','sys'),
        #('string','syslog','syslog'),
        #('string','table','table'),
        #('string','time','time'),
        #('string','traceback','traceback'),
        #('string','types','types'),
        )

    def statusPp2str(self,o):
        return pprint.pformat(o)

    def statusHashPp2str(self,o):
        ans = ""
        keys = o.keys()
        keys.sort()
        for k in keys:
            ans +="%s = %s\n" % (k, o[k])
        return ans
        
        

    def statusMp2pp(self,o):
        return dict(o.iteritems())

    def statusRow(self,name,value,desc):
        return """<tr>
    <td bgcolor=#ffffcc width=120 align=left valign=top><i><font size=-2>"""+name+"""</font></i></td>
    <td bgcolor=#fefefe width=25 align=left valign=top><font size=-2><pre>= """+value+"""</pre></font></td>
    </tr>"""
  #   <td colspan=1 bgcolor=#ffffcc width=100% align=left valign=top><table width=100><tr><td width=100><font size=-3>"""+desc+"""</font></td></tr></table></td>

    def status(self,req):
        self.page=''

        # head
        self.page=self.page+"""<html>
        <head><title>mod_python status</title></head>
        <body bgcolor=#cccccc><center>
        <table width=100% cellspacing=2 cellpadding=2 border=0>
        <tr>
        <td colspan=2 width=100\% bgcolor=white><h4><font color=#006666>mod_python Status Page</font></h4></center></td>
        </tr>
        """
    
        # field storage
        y=util.FieldStorage(req,keep_blank_values=1)
        self.page=self.page+self.statusRow('FieldStorage',self.statusPp2str(y.list),'Field Storage: pass any fields that were included with the page')
    
        for i in self.stats:
            if i[0]=='mp_table': 
                value=self.statusPp2str(self.statusMp2pp(getattr(req,i[1])))
                self.page=self.page+self.statusRow(i[1],value,i[2])
            #elif i[0]=='mp_server': 
            #    value=self.statusPp2str(self.statusMp2pp(getattr(req,i[1])))
            #    self.page=self.page+self.statusRow(i[1],value,i[2])
            #elif i[0]=='connection': 
            #    value=self.statusPp2str(getattr(req.connection,i[1]))
            #    self.page=self.page+self.statusRow(i[1],value,i[2])
            #elif i[0]=='string': 
            #    value=self.statusPp2str(getattr(req,i[1]))
            #    self.page=self.page+self.statusRow(i[1],value,i[2])
            
    
        for i in self.apstats:
            if i[0]=='string': 
                value=self.statusPp2str(getattr(apache,i[1]))
                self.page=self.page+self.statusRow(i[1],value,i[2])
    
        self.page=self.page+self.statusRow('sys.path',self.statusPp2str(sys.path),'sys.path')
        self.page=self.page+self.statusRow('os.environ',self.statusHashPp2str(os.environ),'Environment Variables')
        # self.page=self.page+self.statusRow('x',self.statusPp2str(mod_python.mp_server.port),'Environment Variables')
        # self.page=self.page+self.statusRow('mod_python',self.statusPp2str(dir(mod_python)),'Mod_python dir()')
        self.page=self.page+self.statusRow("Config",self.statusPp2str(req.server.get_config()),'req.server.get_config()')
        self.page=self.page+self.statusRow("Hostname",self.statusPp2str(req.server.server_hostname),'req.server.server_hostname')
    
        self.page=self.page+"""</table></body><html>"""
        req.write(self.page)
        return "OK"
    