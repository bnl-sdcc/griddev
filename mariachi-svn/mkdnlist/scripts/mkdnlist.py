#!/usr/bin/python2.4
#
# Script to invoke the VOMS web service to get a list of members in a group or role, and
# write them to a simple text file. 
#
#
debug = 1

import sys

### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/mkdnlist/')

from xml.dom import minidom
import myurllib224 as urllib2 

certfile="/home/jhover/.globus/usercert.pem"
keyfile="/home/jhover/.globus/userkeynopw.pem"
vomsurl='https://vo.racf.bnl.gov:8443/voms/atlas/services/VOMSAdmin?method=listMembers' 
if debug: print "mkdnlist.py -- grab dnlists!"

# Uses custom urllib2
def urllib2x509httpsGet( url, _cert_file, _key_file):
    urllib2.HTTPSHandler.certfile = _cert_file
    urllib2.HTTPSHandler.keyfile = _key_file
    urllib2.HTTPSHandler.strict = None  
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    f = urllib2.urlopen(url)
    return f.read()

def extractDNs(soap_env):
    doc = minidom.parseString(soapenv)
    env = doc.getElementsByTagName("soapenv:Envelope")[0]
    bod = env.getElementsByTagName("soapenv:Body")[0]
    lmr = bod.getElementsByTagName("listMembersResponse")[0]
    lmrt = lmr.getElementsByTagName("listMembersReturn")[0]
    members = lmrt.getElementsByTagName("item")
    if debug: print "There are %d members in the list." % len(members)
    memberlist = []
    for member in members:
        memberlist.append( member.getElementsByTagName("DN")[0].childNodes[0].data)
    return memberlist


if __name__ == "__main__":
    soapenv = urllib2x509httpsGet(vomsurl, certfile, keyfile ) 
    mlist = extractDNs(soapenv)
    for m in mlist: 
        print m


