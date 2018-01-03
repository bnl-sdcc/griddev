#!/bin/env python
#
#
#


class SSLSocketClient(object):
    # setting socket types
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
 
    def __init__(self, server_address, cert, certkey, ca):
        self.server_address = server_address
        self.connected = False
        self.cert = cert
        self.certkey = certkey
        self.ca = ca
        
    def connect(self):
        global ca
        cert = self.cert
        certkey = self.certkey
        ca = self.ca
        
        def verify_cb(ok, store) :
            global ca
            cert = store.get_current_cert()
            mecert = M2Crypto.X509.load_cert(ca)
            if mecert.get_fingerprint(md="sha1") == cert.get_fingerprint(md="sha1"):
                return 1
            else:
                return ok
        # setup an SSL context.
        context = SSL.Context("sslv23")
        context.load_verify_locations(ca, "./")
        # setting verifying level
        context.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, 1,verify_cb )
        # load up certificate stuff.
        context.load_cert(cert, certkey)
        # setting callback so we can monitor our SSL
        context.set_info_callback()
        # create real socket
        real_sock = socket.socket(self.address_family, self.socket_type)
        connection = SSL.Connection(context, real_sock)
        self.socket = connection
        self.socket.connect(self.server_address)
        self.connected = True


#
# Code above from 
# http://michalmazurek.pl/2007/05/16/ssl-sockets-and-certificate-authentication-in-python/
#
#


certf="/home/jhover/.globus/usercert.pem"
keyf="/home/jhover/.globus/userkeynopw.pem"
capath="/etc/grid-security/certificates/"
cafile="/etc/grid-security/certificates/1c3f2ca8.0"
h="vo.racf.bnl.gov"
p=8443
wsdlurl="https://vo.racf.bnl.gov:8443/voms/atlas/services/VOMSAdmin?wsdl"


print "M2Crypto test..."
import os
import M2Crypto
from M2Crypto import SSL

import urllib


# Get rid of proxies...
print "Removing proxies from env..."
for k in  os.environ.keys():
    kl = k.lower()
    if kl == "http_proxy" or kl == "https_proxy":
        del os.environ[k]

# Create 

#c = SSL.Context('sslv3')
sc = SSL.Context('sslv3')
ret = sc.load_cert(certfile=certf, keyfile=keyf)
print "load_cert ret is %s" % ret
ret = sc.load_verify_locations(cafile=cafile)
print "load_verify_locations via dir + file ret is %s" % ret
#ret = sc.load_verify_locations(cafile=cafile)
#ret = sc.load_verify_locations(cafile, '')
#print "load_verify_locations via file ret is %s" % ret
ret = sc.set_verify(SSL.verify_peer, 1 )
print "set_verify ret %s" % ret

#ret = sc.load_verify_depth(cafile=cafile)

#ret = sc.set_allow_unknown_ca(ok=True)
#print "set_allow_unknown_ca ret is %s" % ret
#ret = sc.set_verify(SSL.verify_peer, 0)

print "sc.get_verify_depth is %s" % sc.get_verify_depth()

s={}
s['cert_file'] = certf
s['key_file'] = keyf
s['ssl_context'] = sc


opener=urllib.FancyURLopener(cert_file=certf , key_file=keyf, ssl_context=sc)
r=opener.open(wsdlurl)
wsdlstr=r.read()
print wsdlstr
