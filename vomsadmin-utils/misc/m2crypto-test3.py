#!/usr/bin/env python

#
#
# WORKS FOR CERN!!!!!!!!!!!!!!!!!!!!!!!!!1
#
#
#
#
cap="/etc/grid-security/certificates/"
# DOEGRIDS
#caf="/etc/grid-security/certificates/1c3f2ca8.0"
# CERN-TCA
#caf="/etc/grid-security/certificates/1d879c6c.0"
# All catted
caf="/etc/grid-security/certificates/allcas.pem"

certf="/home/jhover/.globus/usercert.pem"
keyf="/home/jhover/.globus/userkeynopw.pem"
myurl="https://vo.racf.bnl.gov:8443/voms/atlas/services/VOMSAdmin?wsdl"
urlpath="/voms/mariachi/services/VOMSAdmin?method=listMembers"
myhost="www-mariachi.physics.sunysb.edu"
#myhost="vo.racf.bnl.gov"
myport=8443

# Get rid of proxies...
import os
print "Removing proxies from env..."
for k in  os.environ.keys():
    kl = k.lower()
    if kl == "http_proxy" or kl == "https_proxy":
        del os.environ[k]

import M2Crypto

#ctx = M2Crypto.SSL.Context('sslv3')
ctx = M2Crypto.SSL.Context()
## what are the diff between these two??
#ctx.load_verify_info(cafile="/tmp/ca.crt")
ret = ctx.load_verify_locations(capath=cap, cafile=caf)
print "load_verify_locations ret is %s" % ret

# load client certificate (used to authenticate the client)
ctx.load_cert(certf, keyfile=keyf)

# stop if peer's certificate can't be verified
ctx.set_allow_unknown_ca(True)

# verify peer's certificate
#ctx.set_verify(M2Crypto.SSL.verify_peer, 3)
ctx.set_verify(M2Crypto.SSL.verify_peer, 3)

con = M2Crypto.httpslib.HTTPSConnection(host=myhost, port=myport, strict=0, ssl_context=ctx)

con.request("GET" , urlpath)


print con.getresponse().read()