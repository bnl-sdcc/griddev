#!/usr/bin/env python
#
# VOMSAdmin Utility Library
# 
# vomsadmin.py:   Serves as a full Python interface to the VOMSAdmin API. All input
# and output is in the form of Python objects. Lib interaction with VOMS servers
# is done via SOAPpy. 
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
#
#
import sys
import logging
import ConfigParser
import exceptions
import urllib
import time
#
# mySOAPpy has had HTTPS via SSL certficates hacked in. Too bad the real one
# hasn't done this--it wasn't that hard. 
#
import vomsSOAPpy as SOAPpy
from vomsSOAPpy import SOAPConfig, WSDL

# try out ZSI instead of SOAPpy
#from ZSI.client import Binding
#from ZSI.ServiceProxy import ServiceProxy 

from xml.dom.minidom import parse, parseString

log=logging.getLogger()





class VOMSServer(object):
    """
    Represents a single VOMS Server.
    
    """ 
    def __init__(self, config, section):
        log.debug('VOMSServer.__init__(): New VOMSServer created...')
        self.section=section
        self.vo=config.get(section, 'voname')
        self.serviceurl=config.get(section, 'service_location')
        self.certfile = config.get('main', 'cert_file')
        self.keyfile = config.get('main', 'key_file')
        self.strict = config.get('main' , 'strict')
        self.ttl = config.get(section, 'ttl')
        try:
            self.httpproxy= config.get('main', 'httpproxy')
        except ConfigParser.NoOptionError:
            self.httpproxy = None
        opener=urllib.FancyURLopener(cert_file=self.certfile , key_file=self.keyfile)
        # Grab WSDL from service, for fixing. 
        wsdlurl="%s?wsdl" % self.serviceurl
        log.debug("VOMSServer.__init__(): wsdl url is %s" % wsdlurl)
        try:
            r=opener.open(wsdlurl)
        except IOError, ioe:
            log.critical("VOMSServer.__init__(): IOError. '%s'. Do you have read access to private key? Network connectivity? Proxy?" % ioe)
            sys.exit()
        wsdlstr=r.read()
        #log.debug("VOMSServer.__init__(): wsdl string is %s" % wsdlstr)
        self.wsdl=wsdlstr
        #
        # Next line shouldn't be necessary, but it. See docstring for more info.
        #
        self._fix_soap_fault_in_wsdl()
        cfg=SOAPConfig( cert_file=self.certfile , key_file=self.keyfile )
        self.proxy= WSDL.Proxy(self.wsdl, config=cfg)
        log.debug('VOMSServer.__init__(): VOMSServer initialized fully.')


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
        except Exception :
            log.critical("VOMSServer._fix_soap_fault_in_wsdl(): XML Parser error. Either something is actually wrong with WSDL, or URL is unreachable. Is HTTPS_PROXY set--it shouldn't be?.")
            sys.exit()


    def __repr__(self):
        s=""
        s+= "VOMSServer object:\n"
        s+= "  Section: %s\n" % self.section
        s+= "  VO: %s\n" % self.vo
        s+= "  Base Service URL: %s\n" % self.serviceurl
        return s 
       

#################################################################################    
#
# VOMS Admin API Methods: Informational 
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


    def listSubGroups(self,group):
        """
        Lists all subgroups of the given group.
        
        Arguments:
        
        group:  Group name in form of "/voname/groupname"
        
        Returns full paths for each group, e.g. /voname/group1
        """
        log.debug('VOMSServer.listSubGroups(): Called on group %s' % group)
        resp = self.proxy.listSubGroups(group)
        return resp


    def listMembers(self, group=None):
        """
        Lists all the members of the VO or specified group. 
        
        Arguments:
        
        group:  Group name in form of "/voname/groupname"
        
        Returns (Python) list of VOMSMember objects of members of <group>, or all 
        members ofthe VO if group argument is omitted.              
        """    
        if group:
            resp = self.proxy.listMembers(group)
        else:
            resp = self.proxy.listMembers()
                
        members=[]
        
        for r in resp:
            vm=VOMSMember.parseSOAPUser(r)
            members.append(vm)
        if len(members) == 0:
            log.debug("VOMSServer.listMembers(): Group %s had no members." % group )
        else:
            log.debug("VOMSServer.listMembers(): Created list of %d members." % len(members) )
        return members   
   
   
    def listRoles(self, user=None, ca=None):
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
        
        Returns (Python) list of VOMSMember objects.               
        """    
        resp = self.proxy.listUsersWithRole( groupname=group, rolename=role)
        members=[]
        
        for r in resp:
            vm=VOMSMember.parseSOAPUser(r)
            members.append(vm)
        
        if len(members) == 0:
            log.debug("VOMSServer.listUsersWithRole(): Server %s group %s has no members with %s." % (self.section, group, role) )
        else:
            log.debug("VOMSServer.listUsersWithRole(): Created list of %d members." % len(members) )
        
        return members   
    
    
    def listUsersWithCapability(self, capablty):
        return self.proxy.listUsersWithCapability( capability=capablty)
    
    def listGroups(self, user, ca):
        return self.proxy.listGroups( username=user, userca=ca)

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
        '''
        Argument: VOMSMember object to add to VOMS
        Returns soap response.
        '''
        
        userobj={}
        userobj['DN']=newmember.dn
        userobj['CA']=newmember.ca
        userobj['CN']=newmember.cn
        userobj['certUri']=newmember.certuri
        userobj['mail']=newmember.mail
        
        resp = self.proxy.createUser(user=userobj)
        return resp
        
       
    def createGroup(self, parentname, groupname):
        '''
        Creates a group.
        Parentname e.g, '/voname/group/sub1'
        Groupname e.g., '/voname/group/sub1/newgroup'
        
        '''
        try:
            resp = self.proxy.createGroup(parentname, groupname)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp

       
    def deleteUser(self, username, userca):
        try:
            resp = self.proxy.deleteUser(username, userca)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def deleteGroup(self, groupname):
        try:
            resp = self.proxy.deleteGroup(groupname)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def createRole(self, rolename):
        '''
        Deletes role from VOMS. 
        
        Argument:
        rolename: In form "Role=<role>"
        
        '''
        try:
            resp = self.proxy.createRole(rolename)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def deleteRole(self, rolename):
        try:
            resp = self.proxy.deleteRole(rolename)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def createCapability(self, capability):
        pass
    
    def deleteCapability(self, capability):
        pass
    
    def addMember(self, groupname , username, userca):
        try:
            resp = self.proxy.addMember(groupname, username, userca)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def removeMember(self, groupname, username, userca):
        try:
            resp = self.proxy.removeMember(groupname, username, userca)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def assignRole(self, groupname, rolename, username, userca):
        try:
            resp = self.proxy.assignRole(groupname, rolename, username, userca)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
    
    def dismissRole(self,  parentname, rolename, username, userca):
        try:
            resp = self.proxy.dismissRole(groupname, rolename, username, userca)
        except SOAPpy.Types.faultType, e:
            raise VOMSException("%s" % e)
        return resp
        
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
        log.debug("VOMSServer.deleteObjUser(): Deleteing user '%s'" % mo.dn)
        return self.deleteUser(mo.dn, mo.ca)




    def doCommand(self, command):
        """
        Interface for CLI-processed arbitrary commands. A sensible subset of the VOMSadmin API
        is available via a command line. 
        getVOName
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
            print 'You need to provide a command. Try "--help"'
            return

        parts = command.split()
        com = parts[0]
        log.debug("VOMSServer.doCommand(): First arg is '%s'" % com )
        
        if com == "getVOName":
            print self.getVOName()

        elif com == "getVersion":
            print self.getVersion()
        
        elif com == "listMembers":
            if len(parts) > 1:
                g = parts[1]
                log.debug("VOMSServer.doCommand(): Second arg is '%s'" % g)
                ms = self.listMembers(group=g)
                for m in ms:
                    print m.dn
            else:
                ms = self.listMembers()
                for m in ms:
                    print m.dn

        elif com == "listSubGroups":
            if len(parts) > 1:
                g = parts[1]
                sgs = self.listSubGroups(group=g)
                for sg in sgs:
                    print sg
            else:
                print "'listSubgroups' requires a subgroup argument, e.g. /voname/group" 
        else:
            print "Command '%s' not implemented." % com

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
        sgs = self.listSubGroups(group)
        for sg in sgs:
            grouplist.append(sg)
            self._listAllSubgroups(grouplist, sg)
        return grouplist
    
    def listAllGroups(self):
        '''
        Returns (Python) List of all groups and subgroups.
       '''
        allgroups = []
        allgroups.append(self.vo)
        allgroups = self._listAllSubgroups(allgroups, "/%s" % self.vo)
        return allgroups


    def _syncMembers(self, other):
        '''
        Makes sure all other members exist in this VOMSServer, and removeslocal users that
        do not exist on other server. 
        '''
        log.debug("VOMSServer.synchronize(): Retrieving members of %s" % other.section)
        othermembers = other.listMembers()
        log.debug("VOMSServer.synchronize(): Retrieved %d members from %s" % (len(othermembers), other.section))
        
        log.debug("VOMSServer.synchronize(): Retrieving members of %s" % self.section)
        selfmembers = self.listMembers()
        log.debug("VOMSServer.synchronize(): Retrieved %d members from %s" % (len(selfmembers), self.section))
              
        for m in othermembers:
            if m in selfmembers:
                log.debug("VOMSServer.synchronize(): Member %s already in %s" % ( m.dn, self.section ))
            else:
                try:
                    log.info("VOMSServer.synchronize(): Adding member %s" % m.dn)
                    self.createUser(m)
                except Exception, e:
                    log.warning("VOMSServer.synchronize(): Error: %s" % e )

        #
        # Remove local users that do not exist on other server
        #
        for m in selfmembers:
            if m in othermembers:
                log.debug("VOMSServer.synchronize(): Member %s in both %s and %s" % ( m.dn, self.section, other.section ))
            else:
                try:
                    log.info("VOMSServer.synchronize(): Removing member %s" % m.dn)
                    self.deleteObjUser(m)
                except Exception, e:
                    log.warning("VOMSServer.synchronize(): Error: %s" % e )

    
    
    def _syncGroups(self, other):
        '''
         Make sure all other groups exist in this VOMS Server
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
                    self.createGroup(parent, g)
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
                    self.deleteGroup(g)
                except Exception, e:
                    log.warning("VOMSServer._syncGroups(): Error: %s" % e )

        selfgroups = selfgroups[1:]    # strip off root VO group. It is already synchronized 
        othergroups = othergroups[1:]

        self._syncGroupMembers(other, othergroups, selfgroups)



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
                if m in selfmembers:
                    log.debug("VOMSServer._syncGroupMembers(): %s already in %s" % ( m.dn, g ))
                else:
                    try:
                        log.info("VOMSServer._syncGroupMembers(): Adding %s to %s" % ( m.dn, g))
                        self.addMember(groupname=g, username=m.dn, userca=m.ca)
                    except Exception, e:
                        log.warning("VOMSServer._syncGroupMembers(): Error: %s" % e )
    
            #
            # Remove local users that do not exist on other server
            #
            for m in selfmembers:
                if m in othermembers:
                    log.debug("VOMSServer._syncGroupMembers(): %s in both %s and %s" % ( m.dn, self.section, other.section ))
                else:
                    try:
                        log.info("VOMSServer._syncGroupMembers(): Removing %s" % m.dn)
                        self.removeMember(groupname=g, username=m.dn, userca=m.ca)
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
            log.info("VOMSServer._syncRoles(): Other: %s" % r)
        
        for r in selfroles:
            log.info("VOMSServer._syncRoles(): Self: %s" % r)
        
        for r in otherroles:
            if r in selfroles:
                log.info("VOMSServer._syncRoles(): %s exists in both %s and %s" % ( r, other.section, self.section))
            else:
                log.info("VOMSServer._syncRoles(): Adding %s to %s" % ( r, self.section))
                self.createRole(r)
        
        for r in selfroles:
            if r in otherroles:
                log.info("VOMSServer._syncRoles(): %s exists in both %s and %s" % ( r, other.section, self.section))
            else:
                log.info("VOMSServer._syncRoles(): Removing %s from %s" % ( r, self.section))
                self.deleteRole(r)

    
    def _syncRoleMembers(self, other, group, rolelist):
        '''
        Synchronizes the role members for a specific group.
        '''
        log.debug("VOMSServer._syncRoleMembers(): Syncing roles for group %s " % group)
        for r in rolelist:
            othermembers = other.listUsersWithRole(group=group, role=r)
            selfmembers = self.listUsersWithRole(group=group, role=r)
            for m in othermembers:
                if m in selfmembers:
                    log.debug("VOMSServer._syncRoleMembers(): %s already has %s in group %s " % ( m.dn, r, group ))
                else:
                    try:
                        log.info("VOMSServer._syncRoleMembers(): Adding %s for %s in group %s" % (r, m.dn, group))
                        #self.addMember(groupname=g, username=m.dn, userca=m.ca)
                        self.assignRole(group, r, m.dn, m.ca)
                    except Exception, e:
                        log.warning("VOMSServer._syncRoleMembers(): Error: %s" % e )
                    
            
   
    def synchronize(self, other):
        '''
       Makes this server reflect the contents of other.
       
       VERY DANGEROUS!!! USE WITH EXTREME CAUTION
               
       '''
        log.info("VOMSServer.synchronize(): Mirroring contents of %s to %s" % (other.section , self.section))
        self._syncMembers(other)
        self._syncRoles(other)
        self._syncGroups(other)



class CachingVOMSWrapper(VOMSServer):
    """
    Provides additional queries, the results of which are cached. 
    Contains a Member dictionary keyed on DN. 
    Contains Group sets. 
    Presents simplified API of read-only information calls. 
    Implements caching of information from calls.
    Handles VOMS server failure.  
             
    """
    def __init__(self, config, section):
        VOMSServer.__init__(self, config, section)
        log.debug("CachingVOMSWrapper.__init__(): Begin...")
        
        self.cache = VOMSCache()
                  
        log.debug("CachingVOMSWrapper.__init__(): Done.")
    
    def isMember(self, DN, group=None):
        #self._updateIfNeeded()
        thiscache = self.cache
                
        ret = 0
        try:
            m = thiscache.members[DN]
            ret = 1
        except KeyError:
            ret = 0
        return ret

    def isRoleMember(self, DN, group, role):
        self._updateIfNeeded()
        thiscache = self.cache
        

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

    
    def _update(self):
        """
        Update member and group lists from first available VOMS server for this
        Virtual Organization.
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
            newcache = {}
            newcache['members']= newmembers
            newcache['groups']=newgroups
            self.members = newmembers
            self.groups = newgroups
            self.lastupdate = time.time()
        
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
        self.dn = DN
        self.cn = CN
        self.ca = CA
        self.certuri = certUri
        self.mail = mail
        
    def __repr__(self):
        '''
        String representation of VOMSMember
      '''
        s=""
        s+="DN: %s\n" % self.dn
        s+="CN: %s\n" % self.cn
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
        One VOMSMemeber is the same as another if they have the same DN and CA.         
        '''
        dncmp= cmp(self.dn, other.dn)
        if dncmp == 0:
            #
            # Only go to the trouble of comparing CAs if DNs are identical. 
            #
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
        dncmp = cmp(self.dn, other.dn)
        if dncmp == 0:
            return cmp(self.ca, other.ca)
        else:
            return dncmp
            


class VOMSCache(object):
    '''
    Single cache object so that references to it can be altered atomically.
    
   '''
    def __init__(self):
        self.members = {}   # Dict on DN.
        self.groups={}      # Dict on group name, e.g. "/voname/groupname/subgroup"
                             # Values are themselves dicts, on DN   
        self.ttl = 3600
        self.lastupdate = 0



class VOMSException(exceptions.Exception): pass
'''
    Exception class to represent an error in call to VOMS Admin interface. 
'''

