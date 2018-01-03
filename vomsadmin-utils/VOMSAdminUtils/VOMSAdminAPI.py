#!/usr/bin/env python
#
# VOMSAdmin Utility Library
# 
# vomsadmin.py:   Serves as a full Python interface to the VOMSAdmin API. All input
# and output is in the form of Python objects. Lib interaction with VOMS servers
# is done via SOAP. 
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
"""
 Classes to implement a pure Python VOMSAdmin API. 
 
 Usage:
 

"""

import sys
import os
import logging
import ConfigParser
import exceptions
import time
import tempfile
import re


import xml
from xml.dom.minidom import parse, parseString

from VOMSAdmin.VOMSAdminService import VOMSAdmin
from VOMSAdmin.VOMSAttributesService import VOMSAttributes


log=logging.getLogger()


class VOMSAdminZSIProxy:
    
    def __init__(self,*args, **kw):
        log.debug("VOMSAdminZSIProxy.__init__(): Initializing ZSI Proxy object...")
       
        
        self.base_url = "https://%s:%d/voms/%s/services" % (kw['host'],
                                                            int(kw['port']),
                                                            kw['vo'])
        transdict = {
                     "cert_file":kw['user_cert'], 
                     "key_file":kw['user_key']
                     }
        
        self.admin = VOMSAdmin(url=self.base_url+"/VOMSAdmin",
                               transdict=transdict)
        self.admin.port.binding.AddHeader("X-VOMS-CSRF-GUARD", "")
        
        self.attributes = VOMSAttributes(url=self.base_url+"/VOMSAttributes",
                                         transdict=transdict)
        self.attributes.port.binding.AddHeader("X-VOMS-CSRF-GUARD", "")
        
    
    def transname(self, method_name):
        def f(m):
            return m.group(2).upper()
        
        return re.sub("(-(.))",f,method_name)
    
    
    def call_method(self, method_name, *args, **kw):
        mn = self.transname(method_name)
        
        if self.__class__.__dict__.has_key(mn):
            return self.__class__.__dict__[mn](self,*args,**kw)
        
        else:
            if not self.admin.__class__.__dict__.has_key(mn):
                
                if not self.attributes.__class__.__dict__.has_key(mn):
                    raise RuntimeError, "Unknown method '%s'!" %mn
                else:
                    return self.attributes.__class__.__dict__[mn](self.attributes,*args,**kw)
            
            else:
                return self.admin.__class__.__dict__[mn](self.admin,*args,**kw)


class VOMSServer(object):
    """
    Represents a single VOMS Server.
    
    """ 
    def __init__(self, config, section):
        log.debug('VOMSServer.__init__(): New VOMSServer created...')
        self.section=section
        self.vo=config.get(section, 'voname')
        self.host=config.get(section, 'host')
        self.port=int( config.get(section, 'port') )
        self.serviceurl=config.get(section, 'service_location')
        self.servicepath=config.get(section, 'service_path')
        self.certfile = config.get('main', 'cert_file')
        self.keyfile = config.get('main', 'key_file')
        self.strict = config.get('main' , 'strict')
        self.ttl = config.get(section, 'ttl')

        try:
            self.httpproxy= config.get('main', 'httpproxy')
        except ConfigParser.NoOptionError:
            log.debug("VOMSServer.__init__(): No proxy set in config.")
            self.httpproxy = None
        # Create proxy object to call methods on server...
        self._make_soap_proxy()
        self.blacklist = []
        try:
            self.blacklist_file = config.get('main','blacklist_file')
            self._load_blacklist()
        except ConfigParser.NoOptionError:
            log.debug("VOMSServer.__init__(): No blacklist set in config. OK.")
                    
        log.debug('VOMSServer.__init__(): VOMSServer initialized fully.')

    def _load_blacklist(self):
        #try:
        f = open(self.blacklist_file)
        for line in f.readlines():
            line = line.strip()
            self.blacklist.append(line)
        log.debug("%d DNs loaded from blacklist file: %s." % (len(self.blacklist),self.blacklist_file))
        #except Exception:
        #    log.warning("Problem loading blacklist file: %s" % self.blacklist_file)

    def _make_soap_proxy(self):
        """
        Generate SOAP proxy using whatever is available.
        1) ZSI using Andrea Ceccanti's static classes
        """
        log.debug("VOMSServer._make_soap_proxy(): Begin...")
        
        # Check python version 
        major, minor, release, st, num = sys.version_info
        hasStaticZSI=False
        
        # Using Andrea Ceccanti's ZSI static setup
        try:
            from VOMSAdminUtils.VOMSAdminAPI import VOMSAdminZSIProxy
            hasStaticZSI = True
        except ImportError:
            pass

        if hasStaticZSI:
            log.debug("VOMSServer._make_soap_proxy(): Using VOMSAdmin static ZSI classes." )
            options={}
            options['host'] = self.host
            options['port'] = self.port
            options['vo'] = self.vo
            options['user_cert'] = self.certfile
            options['user_key'] = self.keyfile
            log.debug("VOMSServer._make_soap_proxy(): Creating ZSI proxy..." )
            self.adminproxy = VOMSAdminZSIProxy(host=self.host, 
                                        port=self.port,
                                        vo=self.vo,
                                        user_cert=self.certfile,
                                        user_key=self.keyfile
                                        )
            self.proxy = self.adminproxy.admin
            self.attributes = self.adminproxy.attributes
                                    
        else:
            raise VOMSException("VOMSServer._make_soap_proxy(): Unable to create ZSI Proxy.")
            
        log.debug("VOMSServer._get_soap_proxy(): Done.")

    def _remove_blacklist_dns(self, userlist):
        toremove = []
        for m in userlist:
            if m.dn in self.blacklist:
                log.debug("Found blacklisted DN: %s Removing..." % m.dn)
                toremove.append(m)
        for r in toremove:
            userlist.remove(r)
        log.debug("Removed %d blacklisted DNs." % len(toremove) )
        return userlist
            

    def _fix_soap_fault_in_wsdl(self):
        """
        This shouldn't be necessary, but it is. SOAPpy complains about invalid
        soap:fault elements from actual WSDL supplied by the VOMSAdmin service.
        This method takes the wsdl and adds in the 'name' attribute for all soap:faults
        so that SOAPpy doesn't complain.  
                
        """
        log.debug("VOMSServer._fix_soap_fault_in_wsdl(): Begin...")
        try:
            xmldoc=parseString(self.wsdl)
            #log.debug("VOMSServer._fix_soap_fault_in_wsdl(): XML doc is %s" % xmldoc)
            soapfaults = xmldoc.getElementsByTagName("wsdlsoap:fault")
            for sf in soapfaults:
                if not sf.hasAttribute('name'):
                    sf.setAttribute('name', 'VOMSException')
            self.wsdl=xmldoc.toprettyxml()
            xmldoc.unlink()
        except xml.parsers.expat.ExpatError, ee :
            log.critical("VOMSServer._fix_soap_fault_in_wsdl(): 'xml.parsers.expat.ExpatError: %s' : Malformed WSDL, URL unreachable, HTTPS_PROXY improperly set." % ee)

    def _download_wsdl_standard(self): 
        #
        # Grab WSDL from service, for fixing if necessary, for debug otherwise... 
        #
        # Using FancyURLopener ...
        #
        import urllib
        from urllib import FancyURLopener
        
        log.debug("VOMSServer._download_wsdl_standard(): Creating opener with cert %s and key %s" % (self.certfile, self.keyfile))
        opener=FancyURLopener(cert_file=self.certfile , key_file=self.keyfile)
        wsdlurl="%s?wsdl" % self.serviceurl
        log.debug("VOMSServer._download_wsdl_standard(): wsdl url is %s" % wsdlurl)
        try:
            log.debug("VOMSServer._download_wsdl_standard(): About to try opener... ")
            r=opener.open(wsdlurl)
            log.debug("VOMSServer._download_wsdl_standard(): Opener defined...")
            wsdlstr=r.read()
            #log.info("VOMSServer.__init__(): wsdl string is %s" % wsdlstr)
            if wsdlstr.find ("<?xml version=") == -1:
                raise VOMSException("Service unavailable: %s" % self.section)
            log.debug("VOMSServer._download_wsdl_standard(): wsdl string downloaded from %s" % wsdlurl)
            self.wsdl=wsdlstr
        
        except IOError, ioe:
            log.critical("VOMSServer._download_wsdl_standard(): IOError. '%s'. Do you have read access to private key? Network connectivity? Proxy?" % ioe)
            raise VOMSException("Service unavailable: %s" % self.section)


    def __repr__(self):
        s=""
        s+= "VOMSServer Object: [%s] VO: %s Service URL: %s" % ( self.section, self.vo, self.serviceurl)
        return s 
       

#################################################################################    
#
# VOMS Admin API Methods: Read-only/Informational 
#
#################################################################################
   
    def getMajorVersionNumber(self):
        """
        Returns major version as integer.
        """ 
        resp = self.proxy.getMajorVersionNumber()
        return resp
    
    def getMinorVersionNumber(self):    
        """
        Returns minor version as integer.
        """         
        resp = self.proxy.getMinorVersionNumber()
        return resp
    
    def getPatchVersionNumber(self):
        """
        Returns patch version as integer.
        """    
        
        resp = self.proxy.getPatchVersionNumber()
        return resp
    
    
    def getVOName(self):
        """
        Returns VOName as string in form "/voname"
        """
        resp = self.proxy.getVOName()
        return resp


    def listSubGroups(self, group):
        """
        Lists all subgroups of the given group.
        
        Arguments:
        
        group:  Group name in form of "/voname/groupname"
        
        Returns Python List of full path strings for each group, e.g. /voname/group1
        """
        log.debug('VOMSServer.listSubGroups(): Called on group %s' % group)
        #log.debug("VOMSServer.listSubGroups(): self.proxy.soapproxy.config.dumpSOAPOut is %d " % self.proxy.soapproxy.config.dumpSOAPOut ) 
        #self.proxy.soapproxy.config.dumpSOAPOut = 1
        #self.proxy.soapproxy.config.dumpSOAPIn = 1
        #sniff = Sniff()
        #sys.stdout = sniff
        
        #try:
        resp = self.proxy.listSubGroups(group)
            #resp = re.findall(c, sniff.buffer())
        log.debug("VOMSServer.listSubGroups(): resp is: %s" % resp)
        
        #log.debug("VOMSServer.listSubGroups(): Response = %s" % resp)
        
        if resp:
            return resp
        else:
            return [] 
        
        #return resp
        #except xml.sax.SAXParseException, e:
        #    log.error('XML error in the response (line %d, column %d): %s' %
        #         (e._linenum, e._colnum, e.getMessage()))
        #sys.stdout = sys.__stdout__       
        #self.proxy.soapproxy.config.dumpSOAPOut = 0
        #self.proxy.soapproxy.config.dumpSOAPIn = 0
        
        #c = re.compile(r">([a-z0-9]+):([^,:< ]+),([^:<]+):([^<]+)<")
        #log.debug("VOMSServer.listSubGroups(): Buffer contents is: %s" % sniff.buffer())
        

        


    def listMembers(self, group=None):
        """
        Lists all the members of the VO or specified group. 
        
        Arguments:
        
        group:  Group name in form of "/voname/groupname"
        
        Returns (Python) list of VOMSMember objects of members of <group>, or all 
        members ofthe VO if group argument is omitted.              
        """
        basegroup = "/%s" % self.vo
            
        if group:
            resp = self.proxy.listMembers(group)
        else:
            resp = self.proxy.listMembers(basegroup)
                
        #print resp
        members=[]
        
        #for r in resp:
        #    vm=VOMSMember.parseSOAPUser(r)
        #    members.append(vm)
        
        #
        # if resp seems to be necessary, since some SOAP implementations return python None
        # instead of an empty list
        if resp:
            while len(resp) > 0:
                user_holder = resp.pop()
                
                dn = user_holder._DN
                cn = user_holder._CN
                ca = user_holder._CA
                em = user_holder._mail
                vm = VOMSMember(DN=dn, CN=cn, CA=ca, mail=em)
                members.append(vm)
            
            if len(members) == 0:
                log.debug("VOMSServer.listMembers(): Group %s had no members." % group )
            else:
                log.debug("VOMSServer.listMembers(): Created list of %d members." % len(members) )

        members = self._remove_blacklist_dns(members)
        return members   
        
   
    def listRoles(self, user=None, ca=None):
        '''
            Returns Python List of Role strings, e.g.  Role=VO-Admin
        '''
        if user and ca:
            return self.proxy.listRoles( username=user, userca=ca)
        else:
            return self.proxy.listRoles()
      
    def listCapabilities(self): 
        return self.proxy.listCapabilities()
   
    
    def listCAs(self, user=None, ca=None):
        if user and ca:
            return self.proxy.listCAs( username=user, userca=ca )
        else:
            return self.proxy.listCAs()

    def listUsersWithRole(self, group, role):
        """
        Lists all the members of the group approved for specified role 
        
        Arguments:
        
        group:  Group name in form of "/voname/groupname"
        role: Role in form "Role=rolename"
        
        Returns (Python) list, possibly empty, of VOMSMember objects.               
        """ 
        log.debug("VOMSServer.listUsersWithRole(): Called on group %s and role %s" % (group,role))   
        resp = self.proxy.listUsersWithRole( group , role)
        members=[]
        
        #for r in resp:
        #    vm=VOMSMember.parseSOAPUser(r)
        #    members.append(vm)
        if resp:
            while len(resp) > 0:
                user_holder = resp.pop()
                dn = user_holder._DN
                cn = user_holder._CN
                ca = user_holder._CA
                vm = VOMSMember(DN=dn, CN=cn, CA=ca)
                members.append(vm)

            if len(members) == 0:
                log.debug("VOMSServer.listUsersWithRole(): Server %s group %s has no members with %s." % (self.section, group, role) )
            else:
                log.debug("VOMSServer.listUsersWithRole(): Created list of %d members." % len(members) )

        members = self._remove_blacklist_dns(members)
        return members   
    
    
    def listUsersWithCapability(self, capablty):
        return self.proxy.listUsersWithCapability( capability=capablty)
    
    def listGroups(self, user, ca):
        return self.proxy.listGroups( username=user, userca=ca)

    def getACL(self, container):
        pass
    
    def getDefaultACL(self,groupname):
        pass


################################################
#   Attribute-related methods. 
###############################################

    def createAttributeClass(self,name, description, unique):
        self.attributes.createAttributeClass(name,description,unique)


    #Unpacks array of AttributeClass_Holders and returns list of 
    def listAttributeClasses(self):
        acs = self.attributes.listAttributeClasses()
        log.debug("Attribute classes: %s" % acs)
        #acs = self.attproxy.call_method('listAttributeClasses')
        #
        #self._description = None
        #            self._name = None
        #            self._uniquenessChecked = None
        attclasses = []
        if acs:
            for ac in acs:
                acobj = VOMSAttributeClass(ac._name, ac._description,ac._uniquenessChecked)
                attclasses.append(acobj)
        return attclasses

    # Unpacks Attribute_Holder and returns a Python Dictionary of key -> values. 
    def listUserAttributes(self,dn,ca ):
        atts = self.attributes.listUserAttributes(dn=dn, ca=ca)
        #atts = self.attproxy.call_method('listUserAttributes', dn=dn, ca=ca)
        
        if atts:
            attributes = {}
            for a in atts:
                k = a._attributeClass._name
                log.debug("Attribute key = %s" %k)
                v = a._value
                log.debug("Attribute val = %s" % v)
                attributes[k]=v        
            return attributes
        return None
    #listUserAttributes(dn,ca)


    def setUserAttribute(self,dn, ca, attrName, attrValue):
        #self.attproxy.call_method('setUserAttribute', dn=dn, ca=ca, attrName=attrName,attrValue=attrValue)
        log.debug("VOMSServer.setUserAttribute( %s, %s, %s, %s): Calling..." % ( dn, ca,attrName, attrValue))
        try:
            self.attributes.setUserAttribute(dn=dn, ca=ca, attrName=attrName, attrValue=attrValue)
        except Exception, e:
            log.warn("VOMSServer.setUserAttribute(): Underlying call produced exception." )




#################################################################################    
#
# VOMS Admin API Methods: Administrative (State-changing) 
#
#################################################################################
    def createUser(self, newmember):
        '''
        Argument: VOMSMember object to add to VOMS
        Returns soap response.
        '''
        if newmember.mail == "":
            newmember.mail="unknown@domain.com"
        if not newmember.mail:
            newmember.mail="unknown@domain.com"
        
        userobj={}
        userobj['DN']=newmember.dn
        userobj['CA']=newmember.ca
        userobj['CN']=newmember.cn
        userobj['certUri']=newmember.certuri
        userobj['mail']=newmember.mail
        
        try:
            resp = self.proxy.createUser(newmember.dn, newmember.ca, newmember.cn, newmember.mail)
            return resp
        except:
            log.warn("VOMSServer.createUser(): Error in underlying proxy command." )
        return None
        
       
    def createGroup(self, groupname):
        '''
        Creates a group.
        Groupname e.g., '/voname/group/sub1/newgroup'
        
        '''
        
        #import vomsSOAPpy as SOAPpy
        log.debug("VOMSServer.createGroup( groupname=%s )" % groupname )
        try:
            resp = self.proxy.createGroup(groupname)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp

       
    def deleteUser(self, username, userca):
        
        log.debug("VOMSServer.deleteUser( username=%s , userca=%s )" % (username, userca) )
        try:
            resp = self.proxy.deleteUser(username, userca)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp
    
    def deleteGroup(self, groupname):
        #import vomsSOAPpy as SOAPpy
        log.debug("VOMSServer.deleteGroup(groupname=%s)" % groupname )
        try:
            resp = self.proxy.deleteGroup(groupname)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp
    
    def createRole(self, rolename):
        '''
        Deletes role from VOMS. 
        
        Argument:
        rolename: In form "Role=<role>"
        
        '''
        log.debug("VOMSServer.createRole( rolename=%s )" % rolename )
        try:
            resp = self.proxy.createRole(rolename)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp
    
    def deleteRole(self, rolename):
        log.debug("VOMSServer.deleteRole( rolename=%s )" % rolename )
        try:
            resp = self.proxy.deleteRole(rolename)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp
    
    def createCapability(self, capability):
        pass
    
    def deleteCapability(self, capability):
        pass
    
    def addMember(self, groupname , username, userca):
        log.debug("VOMSServer.addMember(groupname=%s , username=%s , userca=%s)" %(groupname, username, userca))
        try:
            resp = self.proxy.addMember(groupname, username, userca)
            return resp
        except Exception, e:
            raise VOMSException("%s" % e)
        return None
    
    def removeMember(self, groupname, username, userca):
        log.debug("VOMSServer.removeMember(groupname=%s , username=%s , userca=%s)" %(groupname, username, userca))
        try:
            resp = self.proxy.removeMember(groupname, username, userca)
            return resp
        except Exception, e:
            raise VOMSException("%s" % e)
        return None
    
    def assignRole(self, groupname, rolename, username, userca):
        try:
            resp = self.proxy.assignRole(groupname, rolename, username, userca)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp
    
    def dismissRole(self,  parentname, rolename, username, userca):
        try:
            resp = self.proxy.dismissRole(groupname, rolename, username, userca)
        except Exception, e:
            raise VOMSException("%s" % e)
        return resp

    # Capability and ACL functionality not needed. 
        
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


    def deleteObjUser(self, memberobj):
        mo = memberobj
        log.debug("VOMSServer.deleteObjUser(): Deleting user '%s'" % mo.dn)
        return self.deleteUser(mo.dn, mo.ca)




    def doCommand(self, command):
        """
        Interface for CLI-processed arbitrary commands. A sensible subset of the VOMSadmin API
        is available via a command line. 
        
        listMembers    Returns simple list of DNs. 
        listMembers <group> , e.g. "listMembers /voname/group"
        listSubGroups <group> , e.g. "listSubGroups /voname" for whole VO
        listUsersWithRole <group> <role>, e.g. "listUWR /atlas/usatlas Role=production" 
        
        getVOName
        getVersion                               Prints VOMSAdmin version.
        listMembers                              Prints DNs of all members. 
        listMembers /vo/group                    Lists DNs of group members.
        listSubGroups /voname                    Lists subgroups.
        listUsersWithRole /vo/group Role=role    Lists DNs of members with role.
        
        Note: doCommand does not return values. It prints to stdout. If you need to process 
        responses, then you need to call the VOMSAdmin methods directly. 
        
        """        
        log.debug("VOMSServer.doCommand(): Got command '%s'" % command)
        if not command or (command == ''):
            print('You need to provide a command. Try "--help"')
            return

        #parts = command.split()
        parts = command
        com = parts[0]
        n = 0
        for p in parts:            
            log.debug("VOMSServer.doCommand(): Arg %d is '%s'" %  (n,p ))
            n = n+1


        # creatAttributeClass(self,name, description, unique)
        if com == "createAttributeClass" :
            if len(parts) > 3:
                n = parts[1]
                d = parts[2]
                u = parts[3]
                self.creatAttributeClass(n,d,u)

        elif com == "createGroup":
            if len(parts) > 2:
                p = parts[1]
                g = parts[2]
                self.createGroup(parentname=p, groupname=g)         
        
        elif com == "createGroup":
            if len(parts) > 1:
                groupname = parts[1]
                self.createGroup(groupname)

        elif com == "createUser":
            if len(parts) > 2:
                dn = parts[1]
                cn = parts[2]
                ca = parts[3] 
                mail = parts[4]
                certuri = parts[5]
                #DN, CN, CA
                # certUri=None, mail=None
                newuser = VOMSMember(DN=dn, CN=cn, CA=ca, certUri=certuri, mail=mail)
                self.createUser(newuser)
        
        elif com == "deleteGroup":
            if len(parts) > 1:
                g = parts[1]
                self.deleteGroup(groupname=g)        


        elif com == "getVersion":
            print( self.getVersion())

        elif com == "getVOName":
            print( self.getVOName())

        # creatAttributeClass(self,name, description, unique)
        elif com == "listAttributeClasses" :
            print(self.listAttributeClasses())

        elif com == "listAttributeDuplicates" :
            if len(parts) > 1:
                a = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % a)
                print(self.listAttributeDuplicates(a)) 
            else:
                print("listAttributeDuplicates() requires attribute argument.")
                           
        
        
        elif com == "listMembers":
            if len(parts) > 1:
                g = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % g)
                ms = self.listMembers(group=g)
                for m in ms:
                    print("%s,%s" % ( m.dn, m.ca))
            else:
                ms = self.listMembers()
                for m in ms:
                    print("%s,%s" % ( m.dn, m.ca))

        elif com == "listMembersEmail":
            if len(parts) > 1:
                g = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % g)
                ms = self.listMembers(group=g)
                for m in ms:
                    print( "%s,%s" % ( m.dn, m.mail))
            else:
                ms = self.listMembers()
                for m in ms:
                    print( "%s,%s" % ( m.dn, m.mail))
        
        
        elif com == "listRoles":
            rs = self.listRoles()
            for r in rs:
                print( r )
        
        elif com == "listSubGroups":
            if len(parts) > 1:
                g = parts[1]
                sgs = self.listSubGroups(group=g)
                for sg in sgs:
                    print sg
            else:
                print "'listSubgroups' requires a subgroup argument, e.g. /voname/group" 
        
        # listUserAttributes(self,dn,ca ):
        elif com == "listUserAttributes":
            if len(parts) > 2:
                dn = parts[1]
                ca = parts[2]
                attributes = self.listUserAttributes(dn, ca)
                for k in attributes.keys():
                    print("%s = %s" % (k, attributes[k] ))

        
        elif com == "listUsersWithRole" :
            if len(parts) > 2:
                #listUsersWithRole /vo/group Role=role
                g= parts[1]
                r= parts[2]
                members = self.listUsersWithRole(group=g, role=r)
                for m in members:
                    print m.dn

        # removeMember(self,group,dn,ca ):
        elif com == "removeMember":
            if len(parts) > 2:
                g = parts[1]
                dn = parts[2]
                ca = parts[3]
                attributes = self.removeMember(g, dn, ca)
            else:
                print("removeMember() requires 3 args: group dn ca")        
        
        
        #setUserAttribute(self,dn, ca, attrName, attrValue)
        elif com == "setUserAttribute" :
            pass
        




        #
        # Other methods not part of API
        #

        elif com == "listMembersEmail":
            if len(parts) > 1:
                g = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % g)
                ms = self.listMembers(group=g)
                for m in ms:
                    print( "%s,%s" % ( m.dn, m.mail))
            else:
                ms = self.listMembers()
                for m in ms:
                    print( "%s,%s" % ( m.dn, m.mail))
        
        elif com == "listMembersSimple":
            if len(parts) > 1:
                g = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % g)
                ms = self.listMembers(group=g)
                for m in ms:
                    print( "%s" % ( m.dn))
            else:
                ms = self.listMembers()
                for m in ms:
                    print( "%s" % ( m.dn))
        
        
        
        
        elif com == "createUserTest" :
            newmember = VOMSMember(DN="/DC=org/DC=doegrids/OU=People/CN=John R. Hover 123456", 
                                       CA="/DC=org/DC=DOEGrids/OU=Certificate Authorities/CN=DOEGrids CA 1", 
                                       CN="John R. Hover", 
                                       certUri=None, 
                                       mail="jhover@somewhere.bnl.gov")
            self.createUser(newmember)

        elif com == "deleteUserTest" :
            oldmember = VOMSMember(DN="/DC=org/DC=doegrids/OU=People/CN=John R. Hover 123456", 
                                       CA="/DC=org/DC=DOEGrids/OU=Certificate Authorities/CN=DOEGrids CA 1", 
                                       CN="John R. Hover", 
                                       certUri=None, 
                                       mail="jhover@somewhere.bnl.gov")
            self.deleteUser(oldmember.dn, oldmember.ca)


        else:
            print("Command '%s' not recognized. Either not implemented or bad arg count." % com)


    def getVersion(self):
        '''
        Collects major, minor, and patch versions and combines them.
        
        '''
        maj=self.getMajorVersionNumber()
        min=self.getMinorVersionNumber()
        pat=self.getPatchVersionNumber()
        return "%s.%s.%s" % (maj, min, pat)

    def _listAllSubgroups(self, grouplist, group):
        '''
        Recursive function to list all subgroups of a given group
      '''
        log.debug("VOMSServer._listAllSubgroups(): Calling listSubGroups on %s" % group)
        sgs = self.listSubGroups(group)
        log.debug("VOMSServer._listAllSubgroups(): About to iterate over %s" % sgs)
        for sg in sgs:
            grouplist.append(sg)
            self._listAllSubgroups(grouplist, sg)
        log.debug("VOMSServer._listAllSubgroups(): Returning grouplist called on %s" % group )
        return grouplist
    
    def listAllGroups(self):
        '''
        Returns (Python) List of all groups and subgroups.
       '''
        allgroups = []
        allgroups.append(u'/%s' % self.vo)
        allgroups = self._listAllSubgroups(allgroups, "/%s" % self.vo)
        return allgroups

    def listAttributeDuplicates(self, attributename):
        '''
        Determines which members have matching attributes and prints them:
        
        <attribute value>
            <DN1>
            <groups1>
            <group2>
            <group3>
            <email>
                   
        
        
        '''



    def _syncMembers(self, other, sync_attributes=True):
        '''
        Makes sure all other members exist in this VOMSServer, and removeslocal users that
        do not exist on other server. 
        If attributes = True, it synchronizes AttributeClasses and all Member attributes. 
              
        '''
        try:
            log.info("VOMSServer._syncMembers(): Retrieving members of %s" % other.section)
            othermembers = other.listMembers()
            othermembers = self._remove_blacklist_dns(othermembers)
            log.info("VOMSServer._syncMembers(): Retrieved %d members from %s" % (len(othermembers), other.section))
            
            log.info("VOMSServer._syncMembers(): Retrieving members of %s" % self.section)
            selfmembers = self.listMembers()
            selfmembers = self._remove_blacklist_dns(selfmembers)
            log.info("VOMSServer._syncMembers(): Retrieved %d members from %s" % (len(selfmembers), self.section))
            
            othern = 1
            otherlen = len(othermembers)      
            for m in othermembers:
                if m in selfmembers:
                    log.debug("VOMSServer._syncMembers(): Member %s (%d of %d) already in %s" % ( m.dn, othern, otherlen, self.section ))
                else:
                    try:
                        log.info("VOMSServer._syncMembers(): Adding member %s (%d of %d)" % (m.dn, othern, otherlen))
                        self.createUser(m)
                    except Exception, e:
                        log.warning("VOMSServer._syncMembers(): Error: %s" % e )
                othern += 1
    
            #
            # Remove local users that do not exist on other server
            #
            selfn = 1
            selflen = len(selfmembers) 
            for m in selfmembers:
                if m in othermembers:
                    log.debug("VOMSServer._syncMembers(): Member %s (%d of %d) in both %s and %s" % ( m.dn, selfn, selflen, self.section, other.section ))
                else:
                    try:
                        log.info("VOMSServer._syncMembers(): Removing member %s (%d of %d)" % (m.dn, selfn, selflen))
                        self.deleteObjUser(m)
                    except Exception, e:
                        log.warning("VOMSServer._syncMembers(): Error: %s" % e )
                selfn += 1
    
            if  sync_attributes:
                # Get other attribute Classes and create on self.
                    
                
                # Retrieve attributes fo othermembers and sync. 
                # Getting each attribute requires a separate call, so we just unconditionally set 
                # the attribute, rather than checking to see if it is alrady correct. 
                #
                log.info("VOMSServer._syncMembers(): Attribute syncing requested. Getting attributes from %s." % other.section)
                
                othern = 1
                otherlen = len(othermembers) 
                for m in othermembers:
                    log.debug("VOMSServer._syncMembers(): Getting attributes for %s (%d of %d." % (m.dn, othern, otherlen))
                    try:
                        attributes = other.listUserAttributes(m.dn, m.ca)
                        if attributes:
                            for k in attributes.keys():
                                if attributes[k]:
                                    log.info("VOMSServer._syncMembers(): Setting attribute %s = %s for %s" % (k, attributes[k],m.dn ))
                                    self.setUserAttribute(m.dn, m.ca, k, attributes[k])
                                else:
                                    log.info("VOMSServer._syncMembers(): Attribute %s = %s for %s, skipping." % (k, attributes[k],m.dn ))
                    except Exception, e:
                        log.warning("VOMSServer._syncMembers(): Error: %s Caught while handling attributes for %s" % (e, m.dn) )
                    othern += 1
                        
                log.info("VOMSServer._syncMembers(): Done synching attributes.")                      
        except Exception, e:
            log.warning("VOMSServer._syncMembers(): Major error: %s" % e )

    
    def _syncGroups(self, other):
        '''
         Make sure all other groups exist in this VOMS Server. And ensure that their
         membership is the same. 
         
        '''
        log.info("VOMSServer._syncGroups(): Synchronizing groups from %s."% other.section )
        selfgroups = self.listAllGroups()
        log.debug("VOMSServer._syncGroups(): Self groups: %s" % selfgroups)
        othergroups = other.listAllGroups()
        log.debug("VOMSServer._syncGroups(): Other groups: %s" % othergroups)

        #
        # Synchronize group names
        #
        for g in othergroups:
            if g not in selfgroups:
                log.debug("VOMSServer._syncGroups(): Group %s in other, but not self."% g )
                nodes = g.split('/')                
                parent ='/'.join(nodes[:-1]) 
                try:
                    log.info("VOMSServer._syncGroups(): Creating local group: %s" % g)
                    self.createGroup(g)
                except Exception, e:
                    log.warning("VOMSServer._syncGroups(): Error: %s" % e )
            
            else:
                log.debug("VOMSServer.synchronize(): Group %s already in both."% g )
                
        for g in selfgroups:
            if g in othergroups:
                log.debug("VOMSServer._syncGroups(): Group %s in both." % g)
            else:                
                try:
                    log.info("VOMSServer._syncGroups(): Removing group %s." % g)
                    #self.deleteGroup(g)
                except Exception, e:
                    log.warning("VOMSServer._syncGroups(): Error: %s" % e )

        self._syncGroupMembers(other, othergroups, selfgroups)
    
        log.info("VOMSServer._syncGroups(): Done.")

    def _syncAttributeClasses(self, other):
        otherattr = other.listAttributeClasses()
        selfattr = self.listAttributeClasses()
        try:
            for oa in otherattr:
                if oa not in selfattr:
                    self.createAttributeClass(oa.name, oa.description, oa.unique)
            log.info("VOMSServer._syncAttributeClasses(): Attribute class sync complete.")
        except Exception, e:
            log.warning("VOMSServer._syncAttributeClasses(): Error: %s" % e )
        
    def _syncGroupMembers(self, other, othergroups, selfgroups):
        '''
         Make sure all groups in this server contain same members as other server. 
        '''
        #
        # Synchronize group membership
        #
        log.info("VOMSServer._syncGroupMembers(): Synchronizing %s from %s" % (othergroups, other.section))
        log.debug("VOMSServer._syncGroupMembers(): Grabbing role list from %s for later use." % other.section)
        otherroles=[]
        try:
            ors = other.listRoles() 
        except Exception, e:
            log.warning("VOMSServer._syncGroupMembers(): Error during listRoles(): %s" % e )
        for r in ors:
            otherroles.append(r)

        
        for g in selfgroups:
            log.debug("VOMSServer._syncGroupMembers(): Retrieving members of %s from %s" % (g, other.section))
            othermembers = other.listMembers(group=g)
            log.debug("VOMSServer._syncGroupMembers(): Retrieved %d members from %s" % (len(othermembers), g))
            
            log.debug("VOMSServer._syncGroupMembers(): Retrieving members of %s from %s" % (g, self.section))
            selfmembers = self.listMembers(group=g)
            log.debug("VOMSServer._syncGroupMembers(): Retrieved %d members from %s" % (len(selfmembers), g))
                  
            for m in othermembers:
                try:
                    if m in selfmembers:
                        log.debug("VOMSServer._syncGroupMembers(): %s already in %s" % ( m.dn, g ))
                    else:
                        try:
                            log.info("VOMSServer._syncGroupMembers(): Adding %s to %s" % ( m.dn, g))
                            self.addMember(groupname=g, username=m.dn, userca=m.ca)
                        except Exception, e:
                            log.warning("VOMSServer._syncGroupMembers(): Error adding user %s: %s" % (m.dn, e) )
                except Exception, e:
                    log.warning("VOMSServer._syncGroupMembers(): Error syncing othermembers: %s" % e )    
            #
            # Remove local users that do not exist on other server
            #
            for m in selfmembers:
                try:
                    if m in othermembers:
                        log.debug("VOMSServer._syncGroupMembers(): %s in both %s and %s" % ( m.dn, self.section, other.section ))
                    else:
                        try:
                            log.info("VOMSServer._syncGroupMembers(): Removing %s" % m.dn)
                            self.removeMember(groupname=g, username=m.dn, userca=m.ca)
                        except Exception, e:
                            log.warning("VOMSServer._syncGroupMembers(): Error removing user %s: %s" % (m.dn, e) )
                except Exception, e:
                    log.warning("VOMSServer._syncGroupMembers(): Error: %s" % e )                        
                        
            log.info("VOMSServer._syncGroupMembers(): Group %s members now synchronized" % g)
    
            #
            # Now synchronize role ability per group
            #
            if len(otherroles) > 0:
                log.info("VOMSServer._syncGroupMembers(): Now synchronizing roles for group %s" % g)
                self._syncRoleMembers(other, g, otherroles)



    def _syncRoles(self, other):
        '''
        Make sure all Roles on other exist on this VOMSServer
        '''

        otherroles=[]
        selfroles=[]

        ors = other.listRoles() 
        for r in ors:
            otherroles.append(r)
        srs = self.listRoles()
        for r in srs:
            selfroles.append(r)
            
        for r in otherroles:
            log.debug("VOMSServer._syncRoles(): Other: %s" % r)
        
        for r in selfroles:
            log.debug("VOMSServer._syncRoles(): Self: %s" % r)
        
        for r in otherroles:
            if r in selfroles:
                log.debug("VOMSServer._syncRoles(): %s exists in both %s and %s" % ( r, other.section, self.section))
            else:
                log.info("VOMSServer._syncRoles(): Adding %s to %s" % ( r, self.section))
                self.createRole(r)
        
        for r in selfroles:
            if r in otherroles:
                log.debug("VOMSServer._syncRoles(): %s exists in both %s and %s" % ( r, other.section, self.section))
            else:
                log.info("VOMSServer._syncRoles(): Removing %s from %s" % ( r, self.section))
                #self.deleteRole(r)

    
    def _syncRoleMembers(self, other, group, rolelist):
        '''
        Synchronizes the role members for a specific group.
        '''
        log.debug("VOMSServer._syncRoleMembers(): Syncing roles for group %s " % group)
        for r in rolelist:
            othermembers = other.listUsersWithRole(group=group, role=r)
            selfmembers = self.listUsersWithRole(group=group, role=r)
            for m in othermembers:
                try:
                    if m in selfmembers:
                        log.debug("VOMSServer._syncRoleMembers(): %s already has %s in group %s " % ( m.dn, r, group ))
                    else:
                        try:
                            log.info("VOMSServer._syncRoleMembers(): Adding %s for %s in group %s" % (r, m.dn, group))
                            #self.addMember(groupname=g, username=m.dn, userca=m.ca)
                            self.assignRole(group, r, m.dn, m.ca)
                        except Exception, e:
                            log.warning("VOMSServer._syncRoleMembers(): Error adding %s: %s" % (m.dn, e ))
                except Exception, e:
                    log.warning("VOMSServer._syncRoleMembers(): Error handing othermembers: %s" % e )
        log.debug("VOMSServer._syncRoleMembers(): Done syncing roles for group %s " % group)
                    
            
   
    def synchronize(self, other):
        '''
       Makes this server reflect the contents of other.
       
       USE WITH CAUTION! Be sure you don't confuse source with target, self with other
               
       '''
        log.info("VOMSServer.synchronize(): Mirroring contents of %s to %s" % (other.section , self.section))
        try:
            self._syncAttributeClasses(other) # This syncs attributes available
            self._syncRoles(other)   # This syncs names of roles available
            self._syncMembers(other)  # This syncs members and their per-member attributes. 
            self._syncGroups(other)  # This syncs groups, group members, and roles per group
            log.info("VOMSServer._synchronize(): %s successfully synchronized from %s" % (self.section, other.section ))
        except Exception, e:
            log.warning("VOMSServer._synchronize(): Synchronization failed. Error: %s" % e)



class CachingVOMSWrapper(VOMSServer):
    """
    Provides additional queries, the results of which are cached. 
    Contains a Member dictionary keyed on DN. 
    Contains Group sets. 
    Presents simplified API of read-only information calls. 
    Implements caching of information from calls--synchronously.

    """
    def __init__(self, config, section):
        VOMSServer.__init__(self, config, section)
        log.debug("CachingVOMSWrapper.__init__(): Begin...")
        self.vogroup = "/%s" % self.vo
        self.groupmembers = {}    # dict Key: group -> Grouphash: (lastchecked, DnHash: DN -> lastaccessed  )
        self.rolemembers = {}     # dict Key: group -> Grouphash+ role   Value: ( bool, lastchecked )           
        self.ttl = int(config.get(section, 'ttl')) 
        log.debug("CachingVOMSWrapper.__init__(): Done.")
    
    
    def isGroupMember(self, DN, group=None):
        '''
        Uses internal caching to answer query. Grabs the members of the specified group
        if cache is invalid. 
        
        Returns 0 for no, 1 for yes.
               
        '''        
        if not group:
            group=self.vogroup

        log.debug("isGroupMember(): DN: %s group: %s" % ( DN, group ))
            
        nowtime = time.time()
       
        try:
            (lastchecked, dns) = self.groupmembers[group]
            if nowtime - lastchecked > self.ttl:
                log.info("isGroupMember(): Cache miss by ttl. Updating...")
                self._updateGroupMembers(group)
            else:
                log.info("isGroupMember(): Cache hit by ttl. Continuing...")
        except KeyError:
            log.info("isGroupMember(): Cache miss by group. Updating...")
            self._updateGroupMembers(group)
        
        # cache is current, one way or another 
        try:
            (lc, dnhash) = self.groupmembers[group]
        except KeyError:
            log.error("isGroupMember(): No such group %s" % group)
            return 0    
        
        try:
            ans = dnhash[DN]
            dnhash[DN] = nowtime
            log.info("isGroupMember(): User %s is a member of group %s." % (DN, group))
            return ans
        except KeyError:
            log.info("isGroupMember(): User %s not a member of group %s" % (DN, group))
            return 0
            
            
    def _updateGroupMembers(self, group=None):
        
        if not group:
            group=self.vogroup
                
        nowtime = time.time()    
        
        log.debug("_updateGroupMembers(): Grabbing members for group %s" % group)
        members = self.listMembers(group)
        
        dnhash = {}
        for m in members:
            dn = m.dn
            dnhash[dn] = 0
            log.debug("_updateGroupMembers(): Cached %s in group %s" % (dn, group) )    
        self.groupmembers[group] = (nowtime, dnhash)    
        log.debug("_updateGroupMembers(): Completed caching for group %s" % group)    
               
            

    def isRoleMember(self, DN, group, role):
        '''
        Uses caching to answer request about whether user DN is allowed this role
        in specified group. 
        
        Returns 0 for no, 1 for yes
        
        '''
        pass



    def setTTL(self, seconds):
        self.ttl = seconds

    def _updateIfNeeded(self):
        now = time.time()
        elapsed = now - self.lastupdate
        if elapsed > self.ttl:
            log.debug('CachingVOMSWrapper._updateIfNeeded(): Triggering cache update...')
            self._update()
            log.debug('CachingVOMSWrapper._updateIfNeeded(): Cache update complete. ')
        else:
            log.debug('CachingVOMSWrapper._updateIfNeeded(): Cache updated %d seconds ago. Update not needed. ' % elapsed)

    def _constructGroups(self, memdict, groupdict, groupname):
        """
        Recursive function to construct group maps. 
        Memberdict is assumed to already be populated.
        
        """
        log.debug('vomsapi.CachingVOMSWrapper._constructGroups(): Called on %s' % groupname)
        
        mdict = {}
        ms = self.listMembers(group=groupname)
        for m in ms:
            log.debug("CachingVOMSWrapper._constructGroups(): Putting member %s in group %s" % (m.dn, groupname))
            mdict[m.dn] = memdict[m.dn]
        groupdict[groupname] = mdict
        
        sgs = self.listSubGroups(group=groupname)
        for s in sgs:
            self._constructGroups(memdict, groupdict, s)

    
    def _updateCache(self):
        """
        Update member and group lists from this VOMS server.
        Assumes contents of mulitple VOMS servers for a single VO are interchangeable. 
        
        """
        
        try:
            # Collect all members
            log.debug("CachingVOMSWrapper._update(): Collecting members...")
            newmembers = {}
            ms = self.listMembers()
            for m in ms:
                newmembers[m.dn] = m
            
            # Collect groups
            # List subgroups with members recursively
            log.debug("CachingVOMSWrapper._update(): Collecting groups...")
            newgroups = {}
            self._constructGroups(newmembers, newgroups, "/%s" % self.vo)
            
            # Maps created successfully
            newcache = VOMSCache()
            newcache.members= newmembers
            newcache.groups=newgroups
            newcache.lastupdate=time.time()
            
            #
            # Now that we have a fully filled cache, we set 
            #
            self.cache = newcache

        
        except Exception, e:
            log.info("CachingVOMSWrapper._update(): Failed update from [%s]: Error: %s " % 
                     (self.section, e))
        
   
    def __repr__(self):
        s = VOMSServer.__repr__(self)
        s +="CachingVOMSWrapper object:\n"
        s +="  TTL = %d\n" % self.ttl
        return s

    def printGroups(self):
        """
        Included mainly to implicitly test other methods. 
        """
        self._updateIfNeeded()
        s = ""
        ks = self.groups.keys()
        ks.sort()
        for g in ks:
            s += "%s\n" % g
            ks = self.groups[g].keys()
            ks.sort()
            for m in ks:
                s += "   %s\n" % m
        return s


class VOMSMember(object):
    '''
    Represents a single VOMS Member
    '''
    # Save decorator for demise of Python 2.3...
    #
    #@staticmethod
    def parseSOAPUser(struct):
        '''
        Static method. Parses the SOAPpy.Types.structType encoding the "User" type from the 
        VOMSAdmin WSDL. 
        
        Returns a VOMSMember object that contains the same info. 
        
        '''
        #log.debug("VOMSMemeber.parseSOAPUser(): Struct entry: %s" % struct)
        vm = VOMSMember( DN=struct['DN'],
                           CN=struct['CN'],
                           CA=struct['CA'],
                           certUri=struct['certUri'],
                           mail=struct['mail'],
                           )
        #log.debug("VOMSMember.parseSOAPUser(): Created VOMSMember: %s" % vm)
        return vm
    parseSOAPUser = staticmethod(parseSOAPUser)
    
    def __init__(self, DN, CN, CA, certUri=None, mail=None):
        '''
        Initialize VOMSMember with explicit parameters.
        '''
        self.dn = DN.strip()
        self.dnlower = self.dn.lower()
        self.cn = CN
        self.ca = CA.strip()
        self.calower = self.ca.lower()
        self.certuri = certUri
        self.mail = mail
        
    def __repr__(self):
        '''
        String representation of VOMSMember
      '''
        s=""
        s+="DN: %s\n" % self.dn
        #s+="CN: %s\n" % self.cnlower
        s+="CN: %s\n" % self.cn
        #s+="CA: %s\n" % self.calower
        s+="CA: %s\n" % self.ca
        s+="CertUri: %s\n" % self.certuri
        s+="Mail: %s\n" % self.mail
        return s
    
    def __hash__(self):
            s = self.__repr__()
            return s.__hash__()
        
    def __eq__(self, other):
        '''
        Return 1 if equal, 0 otherwise...
        One VOMSMember is the same as another if they have the same DN and CA.         
      '''
        #dncmp= cmp(self.dnlower, other.dnlower)
        dncmp= cmp(self.dn, other.dn)
        if dncmp == 0:
            #
            # Only go to the trouble of comparing CAs if DNs are identical. 
            #
            #cacmp = cmp(self.calower, other.calower)
            cacmp = cmp(self.ca, other.ca)
            if cacmp == 0:
                return 1
            else:
                return 0
        else:
            return 0
 
    def __cmp__(self, other):
        '''
        For sorting, by DN alphabetical, then by CA alphabetical
        '''
        #dncmp = cmp(self.dnlower, other.dnlower )
        dncmp= cmp(self.dn, other.dn)
        if dncmp == 0:
            #return cmp(self.calower, other.calower)
            return cmp(self.ca, other.ca)
        else:
            return dncmp

def _findDuplicateDNs(userlist):
    '''
    Utility method to remove duplicate-except-for-case VOMS members.    
    '''
    from operator import attrgetter
    # sort list by DN 
    sortedlist = sorted(userlist, key=attrgetter('dnlower'))
    # step through
    toremove = []
    for i in range(0,len(sortedlist)-1):
        if sortedlist[i].dn.lower() == sortedlist[i+1].dn.lower():
            toremove.append(sortedlist[i+1])
            log.info("User: %s same as %s except for case. Remove latter..." % ( sortedlist[i].dn, sortedlist[i+1].dn ))
    
    for e in toremove:
        log.info("Removing duplicate user %s." % e.dn)
        userlist.remove(e)
    return userlist

class VOMSAttributeClass(object):
    '''
    Simple Python native class to hold info about VOMS Attribute Classes. 
        
    '''
    def __init__(self, name, description=None, unique=False):
        self.name = name
        self.description = description
        self.unique=False
    
    def __repr__(self):
        return "name=%s, description=%s, unique=%s" % (self.name, self.description,self.unique)

    def __eq__(self, other):
        return self.name == other.name
        

class VOMSException(exceptions.Exception): pass
'''
    Exception class to represent an error in call to VOMS Admin interface. 
'''

def _test():
    import os
    from ConfigParser import ConfigParser
    #
    # Having proxies set in the environment will mess things up. This seems to be the
    # case because SOAPpy doesn't deal with proxies correctly. Remove them. 
    #
    
    for k in  os.environ.keys():
        kl = k.lower()
        if kl == "http_proxy" or kl == "https_proxy":
            del os.environ[k]
    
    # Read in config file
    config=ConfigParser()
    config.read(['/home/jhover/workspace/python-vomsadmin/config/python-vomsadmin.conf'])
    vomses = config.get('main', 'vomses').split(',')
    servers = {}
    for v in vomses:
        vs = VOMSServer(config, v)
        servers[v] = vs
    
    for v in vomses:
        print v

    (k,s) = servers.popitem()
    
    print s.listMembers()
   


if __name__ == '__main__':
    _test()
