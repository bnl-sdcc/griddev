#!/usr/bin/env python2.4
#
# VOMS Utility Library
# 
# Author:
#   John Hover <jhover@bnl.gov>
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
# vomslib:   serves as a full Python interface to the VOMSAdmin API. All input
# and output is in the form of Python objects. Lib interaction with VOMS servers
# is done via SOAPpy. 
#
#

import urllib, sgmllib, logging, ConfigParser, exceptions
from xml.dom.minidom import parse, parseString 
import mySOAPpy as SOAPpy
from mySOAPpy import SOAPConfig, WSDL

log= logging.getLogger()


class VOMSServer(object):
    
    def __init__(self, config, section):
        log.debug('New VOMSServer created...')
        self.section=section
        self.vo=config.get(section, 'voname')
        self.certfile = config.get('main', 'cert_file')
        self.keyfile = config.get('main', 'key_file')
        self.strict = config.get('main' , 'strict')
        self.baseurl = config.get(section , 'base_url')
        self.serviceurl= "%s/services/VOMSAdmin?" % self.baseurl
        self.wsdlfile=config.get('main','wsdlfile')
        try:
            self.httpproxy= config.get('main', 'httpproxy')
        except ConfigParser.NoOptionError:
            self.httpproxy = None
        cfg=SOAPConfig( cert_file=self.certfile , key_file=self.keyfile )
        self.proxy= WSDL.Proxy(self.wsdlfile, config=cfg)


    def __repr__(self):
        s=""
        s+= "VOMSServer object\n"
        s+= "  Section: %s\n" % self.section
        s+= "  VO: %s\n" % self.vo
        s+= "  Certfile: %s\n" % self.certfile
        s+= "  Keyfile: %s\n" % self.keyfile
        s+= "  Base URL: %s\n" % self.baseurl
        return s 
       
    

    
    
    def _simpleReturn(self,methodname, **kwargs):
        """
        Private method used to handle calls without args that return a single item. 
             getMajorVersionNumber
             getMinorVersionNumber
             getPatchVersionNumber
             getVOName
        """
        log.debug("VOMSServer._simpleReturn(%s): Begin..." % methodname)
        keys = kwargs.keys()
        params=""
        for k in keys:
            log.debug("VOMSServer._simpleReturn(%s): Kwargs: key: %s val: %s" % (methodname, k, kwargs[k]))
            params+="&%s=%s" % (k, kwargs[k])
             
        openurl="%smethod=%s%s" % ( self.serviceurl, methodname, params)
        log.debug("VOMSServer._simpleReturn(%s): opening url %s" % (methodname, openurl))
                 
        opener = urllib.FancyURLopener( key_file=self.keyfile, cert_file=self.certfile   )
        log.debug('VOMSServer._simpleReturn(%s): Contacting VOMS server...' % methodname)
        r = opener.open(openurl)
        s = r.read()
        log.debug('VOMSServer._simpleReturn(%s): XML Response: \n%s' % (methodname,s))
        xmldoc = parseString(s)
        #
        # Handle response
        #
        
        methodreturn = xmldoc.getElementsByTagName("%sReturn" % methodname)
        if len(methodreturn) > 0:
            ans = methodreturn[0].childNodes[0].data
            log.debug("VOMSServer._simpleReturn(%s): Return is : %s" % (methodname, ans) )
            
        
        faultcode= xmldoc.getElementsByTagName("faultcode")
        if len(faultcode) > 0:
            fc = faultcode[0].childNodes[0].data
            fs = xmldoc.getElementsByTagName("faultstring")[0].childNodes[0].data
            ans = "SOAP Fault: faultcode: %s  faultstring: %s" % (fc, fs)
        
        return ans
    
    def _listReturn(self, methodname, **kwargs):
        """
        Private method used to handle calls that return a list of items. 
          
        """
        log.debug("VOMSServer._listReturn(%s): Begin..." % methodname)
        keys = kwargs.keys()
        params=""
        for k in keys:
            log.debug("VOMSServer._listReturn(%s): Kwargs: key: %s val: %s" % (methodname, k, kwargs[k]))
            params+="&%s=%s" % (k, kwargs[k])
        openurl="%smethod=%s%s" % ( self.serviceurl, methodname, params)
        log.debug("VOMSServer._listReturn(%s): opening url %s" % (methodname, openurl))
        opener = urllib.FancyURLopener( key_file=self.keyfile, cert_file=self.certfile   )
        log.debug('VOMSServer._listReturn(%s): Contacting VOMS server...' % methodname)
        r = opener.open(openurl)
        s = r.read()
        log.debug("VOMSServer._listReturn(%s): XML response: \n%s" % (methodname, s))
        xmldoc = parseString(s)
        items = xmldoc.getElementsByTagName("item")
        anslist = []
        for i in items:
            d = i.childNodes[0].data
            anslist.append(d)
        return anslist

    def listMembersSAX(self, group=None):
        """
        Returns (Python) list of DNs members of <group>, or all members ofthe VO 
        if group argument is omitted. Group must be given as path, e.g. /voname/group1
        This method doesn't use a generic template because is uses SAX rather than DOM, 
        for performance reasons.                
        """    
        log.debug("VOMSServer.listMembers(): Begin...")
        if not group:
            group="/%s" % self.vo

        openurl="%smethod=listMembers&groupname=%s" % ( self.serviceurl, group)
        log.debug("VOMSServer.listMembers: opening url %s" % openurl)
                 
        opener = urllib.FancyURLopener( key_file=self.keyfile, cert_file=self.certfile   )
        log.debug('VOMSServer.listMembers: Contacting VOMS server...')
        r = opener.open(openurl)
        s = r.read()
                       
        log.debug('VOMSServer.listMembers: XML response: \n%s' % s)
        vmp = VOMSMembersParser()
        log.debug('VOMSServer.listMembers: Parsing VOMS server response...')
        vmp.parse(s)
        members = vmp.get_members()
        return members



#################################################################################    
#
# VOMS Admin API Methods: Informational 
#
#################################################################################
   
    def getMajorVersionNumber(self):
        #return self._simpleReturn('getMajorVersionNumber')
        resp = self.proxy.getMajorVersionNumber()
        return resp
    
    def getMinorVersionNumber(self):    
        #return self._simpleReturn('getMinorVersionNumber')
        resp = self.proxy.getMinorVersionNumber()
        return resp
    
    def getPatchVersionNumber(self):    
        #return self._simpleReturn('getPatchVersionNumber')
        resp = self.proxy.getPatchVersionNumber()
        return resp
    
    
    def getVOName(self):
        #return self._simpleReturn('getVOName')         
        resp = self.proxy.getVOName()
        return resp

    def listSubGroups(self,group):
        '''
        listSubGroups-- parent group must be provided as "/voname/groupname" or just "/voname" to
        list all members. 
        Returns full paths for each group, e.g. /voname/group1
        '''
        #return self._listReturn('listSubGroups', groupname=group)
        resp = self.proxy.listSubGroups(group)
        return resp

    def listMembers(self, group=None):
        """
        Returns (Python) list of VOMSMember objects of members of <group>, or all 
        members ofthe VO if group argument is omitted. Group must be given as path, 
        e.g. /voname/group1. This method doesn't use a generic template because it 
        uses DOM, and each user item must be specially processed to create a Python 
        object.                
        """    
        if group:
            resp = self.proxy.listMembers(group)
        else:
            resp = self.proxy.listMembers(group)
        
        members=[]
        for r in resp:
            vm=VOMSMember.parseSOAPUser(r)
            members.append(vm)
        return members
        



    def listMembers2(self, group=None):
        """
        Returns (Python) list of VOMSMember objects of members of <group>, or all 
        members ofthe VO if group argument is omitted. Group must be given as path, 
        e.g. /voname/group1. This method doesn't use a generic template because it 
        uses DOM, and each user item must be specially processed to create a Python 
        object.                
        """    
        log.debug("VOMSServer.listMembers(): Begin...")
        if not group:
            group="/%s" % self.vo

        openurl="%smethod=listMembers&groupname=%s" % ( self.serviceurl, group)
        log.debug("VOMSServer.listMembers: opening url %s" % openurl)
                 
        opener = urllib.FancyURLopener( key_file=self.keyfile, cert_file=self.certfile   )
        log.debug('VOMSServer.listMembers: Contacting VOMS server...')
        r = opener.open(openurl)
        s = r.read()
                       
        log.debug('VOMSServer.listMembers: Server response XML is %s' % s)
        xmldoc = parseString(s)
        items = xmldoc.getElementsByTagName("item")
        members = []
        for i in items:
            dn = i.getElementsByTagName('DN')[0].childNodes[0].data
            ca = i.getElementsByTagName('CA')[0].childNodes[0].data
            cn = i.getElementsByTagName('CN')[0].childNodes[0].data
            email = i.getElementsByTagName('mail')[0].childNodes[0].data
            cui = ""
            try:
                cuielements = i.getElementsByTagName('certUri')[0].childNodes
                log.debug("VOMSServer.listMembers: certUri childnodes assigned.")
                if childNodes:
                    log.debug("VOMSServer.listMembers: certUri childnodes exist.")
                    cui = i.getElementsByTagName('certUri')[0].childNodes[0].data
            except:
                pass
            m = VOMSMember(dn, cn, ca, cui, email)
            log.debug("VOMSServer.listMembers: Member? dn: %s ca: %s" % (dn,ca))
            members.append(m)
        return members
            
   
   
    def listRoles(self, user=None, ca=None):
        if user and ca:
            return self._listReturn('listGroups', username=user, userca=ca)
        else:
            return self._listReturn('listRoles')
      
    def listCapabilities(self): 
        return self._listReturn('listCapabilities')
    
    def listCAs(self, user=None, ca=None):
        if user and ca: 
            return self._listReturn('listGroups', username=user, userca=ca)
        else:
            return self._listReturn('listCAs')

    def listUsersWithRole(self, group, role):
        return self._listReturn('listUserWithRole', groupname=group, rolename=role)
    
    def listUsersWithCapability(self, capablty):
        return self._listReturn('listUsersWithCapability', capability=capablty)
    
    def listGroups(self, user, ca):
        return self._listReturn('listGroups', username=user, userca=ca)

    def getACL(self, container):
        pass
    
    def getDefaultACL(self,groupname):
        pass

#################################################################################    
#
# VOMS Admin API Methods: Administrative (State-changing) 
#
#################################################################################
    def createUser(self, newmember):
        
        userobj={}
        userobj['DN']=newmember.dn
        userobj['CA']=newmember.ca
        userobj['CN']=newmember.cn
        userobj['certUri']=newmember.certuri
        userobj['mail']=newmember.mail
        
        resp = self.proxy.createUser(user=userobj)
        return resp
        
    
    
    def createGroup(self, parentname, groupname):
        pass
    
    def deleteUser(self, username, userca):
        pass
    
    def deleteGroup(self, groupname):
        pass
    
    def createRole(self, rolename):
        pass
    
    def deleteRole(self, rolename):
        pass
    
    def createCapability(self, capability):
        pass
    
    def deleteCapability(self, capability):
        pass
    
    def addMember(self, groupname , username, userca):
        pass
    
    def removeMember(self, groupname, username, userca):
        pass
    
    def assignRole(self, groupname, rolename, username, userca):
        pass
    
    def dismissRole(self,  parentname, rolename, username, userca):
        pass
    
    def assignCapability(self,  capability, username, userca):
        pass
    
    def dismissCapability(self, capability, username, userca):
        pass
    
    def setACL(self, container, acl):
        pass
     
    def addACLEntry(self, container, aclEntry):
        pass
    
    def removeACLEntry(self, container, aclEntry):
        pass
    
    def setDefaultACL(self, groupname, aclEntry):
        pass
    
    def addDefaultACL(self, groupname, aclEntry):
        pass
    
    def removeDefaultACLEntry(self, groupname, aclEntry):
        pass
    

###############################################################################
#
#  Convenience methods, beyond VOMSAdmin API
#
###############################################################################3

    def getMembers(self):
        """
        Get all members of VO and create full VOMSMember object for them, including CA etc. 
        This method uses DOM to make it easier to parse. 
         
        """
        log.debug("VOMSServer.getMembers(): Begin...")
        openurl="%smethod=listMembers&groupname=%s" % ( self.serviceurl, group)
        log.debug("VOMSServer.listMembers: opening url %s" % openurl)
                 
        opener = urllib.FancyURLopener( key_file=self.keyfile, cert_file=self.certfile   )
        log.debug('VOMSServer.listMembers: Contacting VOMS server...')
        r = opener.open(openurl)
        s = r.read()


    def getVersion(self):
        maj=self.getMajorVersionNumber()
        min=self.getMinorVersionNumber()
        pat=self.getPatchVersionNumber()
        return "%s.%s.%s" % (maj, min, pat)


class VOMSException(exceptions.Exception): pass
'''
    Exception class to represent an error in call to VOMS Admin interface. 

'''


class VOMSMember(object):
    "Represents a single user"
    
    @staticmethod
    def parseSOAPUser(struct):
        return VOMSMember( DN=struct['DN'],
                           CN=struct['CN'],
                           CA=struct['CA'],
                           certUri=struct['certUri'],
                           mail=struct['mail'],
                           )
    
    def __init__(self, DN, CN, CA, certUri=None, mail=None):
        "Initialize user."
        self.dn = DN
        self.cn = CN
        self.ca = CA
        self.certuri = certUri
        self.mail = mail
        
    def __repr__(self):
        s=""
        s+="DN: %s\n" % self.dn
        s+="CN: %s\n" % self.cn
        s+="CA: %s\n" % self.ca
        s+="CertUri: %s\n" % self.certuri
        s+="Mail: %s\n" % self.mail
        return s
    
    def getDn(self):
        return self.dn
    
    def getCa(self):
        return self.ca

    def getCn(self):
        return self.cn
   
    

class VOMSMembersParser(sgmllib.SGMLParser):
    """A simple parser class. Parses the members list from a VOMS call using SAX.
    More complex processing will have to use DOM."""
    
    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.members = []
        self.tags = []
        self.dnflag = 0
    
    def start_dn(self, attrs):
        self.dnflag = 1

    
    def end_dn(self):
        self.dnflag = 0
        
    def handle_data(self, data):
        if self.dnflag:
            self.members.append(data)
        self.dnflag=0
        
    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def get_members(self):
        "Return the list of DNs."
        return self.members



class MajorVersionNumberParser(sgmllib.SGMLParser):
    """A simple parser class. Parses the members list from a VOMS call using SAX.
    More complex processing will have to use DOM."""
    
    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.mvn=None
        self.dnflag = 0
    
    def start_getmajorversionnumberreturn(self, attrs):
        self.dnflag = 1

    
    def end_getmajorversionnumberreturn(self):
        self.dnflag = 0
        
    def handle_data(self, data):
        if self.dnflag:
            self.mvn=data
        
    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def get_version(self):
        "Get Major Version Number."
        return self.mvn    
    