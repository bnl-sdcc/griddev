#!/usr/bin/env python
#
# Author: John R. Hover <jhover@bnl.gov>
#
# Merges the contents of /usr/doc/tomcat-glite-trustmanager-<version>/server.xml.txt 
# into the proper place in /etc/tomcat5/server.xml
#
# Called with post or preun as arguments from the RPM.
#

debug=0

if debug: print "This is the tomcat5-glite-trustmanager RPM script..."

import sys
from xml.dom import minidom

server_xml="/etc/tomcat5/server.xml"
connector_xml="/usr/share/doc/tomcat5-glite-trustmanager-1.6.3/server.xml.txt" 

#
# When called as RPM postinstall script...
#
def post():

    if debug: print "rpmscript.post()..."
    try:
        server_doc=minidom.parse(server_xml)
    except:
        print "Error opening or parsing %s\nDon't know what to do. Exitting..."
        sys.exit()
        
    stringlist= open(connector_xml).readlines()
    connect_str = ''.join(stringlist)
    if debug: print "Fragment string = %s" % connect_str
    
    services = server_doc.getElementsByTagName("Service")
    if debug: print "There are %d Services in document" % len(services)
    
    #
    # Parse XML fragment to be inserted. Parser returns Document, so we 
    # grab the single Connector child.
    egee_connector=minidom.parseString(connect_str).getElementsByTagName("Connector")[0]

#
# Search for Catalina service, then look for Connector on port 8443. Replace it with our
# definition, or insert our definition.
#
    for service in services:
        servicename = service.getAttribute("name")
        if debug: print "  Service with name %s" % servicename
        if servicename == "Catalina":
            connectors = service.getElementsByTagName("Connector")
            if debug: print "There are %d Connectors in Service" % len(connectors)    
            connectorhash={}
            # Find all connectors, save by port
            for connector in connectors:
                connectorport = connector.getAttribute("port") 
                if debug: print "    Connector found for port %s" % connectorport
                connectorhash[connectorport] = connector
            try:
                c = connectorhash["8443"]
                service.replaceChild(egee_connector, c)
            except KeyError:
                service.appendChild(egee_connector)
    
    outfile = open(server_xml, 'w')
    server_doc.writexml(outfile)

#
# When called as an RPM preuninstall script...
# Remove egee Connector if found
#
def preun():
    if debug: print "rpmscript.preun()..."
    try:
        server_doc=minidom.parse(server_xml)
    except:
        print "Error opening or parsing %s\nDon't know what to do. Exitting..."
        sys.exit()
    services = server_doc.getElementsByTagName("Service")
    if debug: print "There are %d Services in document" % len(services)
     
    for service in services:
        servicename = service.getAttribute("name")
        if debug: print "  Service with name %s" % servicename
        if servicename == "Catalina":
            connectors = service.getElementsByTagName("Connector")
            if debug: print "There are %d Connectors in Service" % len(connectors)    
            # Find egee connector
            for connector in connectors:
                connectorport = connector.getAttribute("port") 
                if debug: print "    Connector found for port %s" % connectorport
                if connectorport == "8443":
                    try:
                        k = connector.getAttribute("sSLImplementation")
                        if debug: print "k is %s" % k
                        if k and k == "org.glite.security.trustmanager.tomcat.TMSSLImplementation": 
                            if debug: print "8443 EGEE connector found, removing..."    
                            service.removeChild(connector)
                        else:
                            if debug: print "sSLImplementation is None. 8443 connector found, but not for EGEE trustmanager. Done."
                    except KeyError:
                        if debug: print "8443 connector found, but not for EGEE trustmanager. Bailing."    
    outfile = open(server_xml, 'w')
    server_doc.writexml(outfile)


if __name__ == "__main__":
    
    argv = sys.argv[1:]
    
    if len(argv) > 0:
        if argv[0] == "post":
            if debug: print "Called as post."
            post()
        elif argv[0] == "preun":
            if debug: print "Called as preun"
            preun()
        else:
            print "Called incorrectly."
            sys.exit()
    else:
        print "Called incorrectly."
        sys.exit()





