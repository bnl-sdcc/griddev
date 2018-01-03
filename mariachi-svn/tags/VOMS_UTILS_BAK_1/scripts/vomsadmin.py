#!/usr/bin/env python2.4
#
# Full SOAPpy/WSDL implementation of the VOMSAdmin client. 
#
#
#
import sys
sys.path.append('/home/jhover/devel/vomsutils/')

import SOAPpy
from SOAPpy import SOAPConfig

wsdlfile="/home/jhover/devel/vomsutils/config/VOMSAdmin.wsdl"
mariachiws="https://www-mariachi.physics.sunysb.edu:8443/voms/mariachi/services/VOMSAdmin"
mycertfile="/home/jhover/.globus/usercert.pem"
mykeyfile="/home/jhover/.globus/userkeynopw.pem"

cfg=SOAPConfig( cert_file=mycertfile,key_file=mykeyfile )
#cfg.cert_file="/home/jhover/.globus/usercert.pem"]
#cfg.key_file="/home/jhover/.globus/userkeynopw.pem"]


server = SOAPpy.SOAPProxy("https://www-mariachi.physics.sunysb.edu:8443/voms/mariachi/services/VOMSAdmin",config=cfg)

print server.getVOName()
print server.getMajorVersionNumber()
print server.getMinorVersionNumber()
print server.getPatchVersionNumber()

#import the WSDL module, this does all the work for you.
from SOAPpy import WSDL

#specify the wsdl file. This file contains everything an application needs to know
#to call the service with the right arguments, with the right protocol at the right
#location etc.

#Create a proxy. You can call methods that are on a distant machine as if they were
#on your local machine, as if they were implemented in the proxy object.

proxy      = WSDL.Proxy(wsdlfile, config=cfg)
#uncomment thoses lines to see outgoing and incoming soap envelops
#proxy.soapserver.config.cert_file="/home/jhover/.globus/usercert.pem"
#proxy.soapserver.config.key_file="/home/jhover/.globus/userkeynopw.pem"
#proxy.soapserver.config.dumpSOAPIn=1
#proxy.soapserver.config.dumpSOAPOut=1

voname = proxy.getVOName()
print voname


