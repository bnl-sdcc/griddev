#!/bin/env python
# 
# This is a quick-and-dirty wrapper script for voms-admin.py designed to replicate 
# one VOMS to another. It was necessary to get nicknames from CERN to BNL.  
#
# Author John Hover <jhover@bnl.gov>
#
#

###################################################################################
#
#
#  Classes and Functions. 
#
#
#
##################################################################################

class Member(object):
    
    def __init__(self, dn, ca):
        self.dn = dn
        self.ca = ca
        self.nickname = None
    
    def __repr__(self):
        s=""
        s+="DN: %s\n" % self.dn
        s+="CA: %s\n" % self.ca
        #s+="CertUri: %s\n" % self.certuri
        #s+="Mail: %s\n" % self.mail
        return s
    
    def __hash__(self):
            s = self.__repr__()
            return s.__hash__()
        
    def __eq__(self, other):
        '''
        Return 1 if equal, 0 otherwise...
        One Member is the same as another if they have the same DN and CA.         
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
        By DN alphabetical, then by CA alphabetical
        '''
        dncmp = cmp(self.dn, other.dn )
        if dncmp == 0:
            return cmp(self.ca, other.ca)
        else:
            return dncmp

#################################################################################
#
#
#  Synchronization script. 
#
#
#
###################################################################################


import commands

CERN_VOMS="voms.cern.ch"
BNL_VOMS="vo.racf.bnl.gov"

cernmembers=[]
bnlmembers=[]



def syncMembers():
    print("retrieving members from CERN")
    (s,o) = commands.getstatusoutput("voms-admin --host voms.cern.ch --vo atlas list-members /atlas")
    users = o.split("\n")
    print("found %d members at CERN" %  len(users))
    for u in users:
        (udn, uca) = u.split(',')
        nu = Member(udn.strip(), uca.strip())
        try:
            (s,o) = commands.getstatusoutput('voms-admin --nousercert --host voms.cern.ch --vo atlas list-user-attributes "%s" "%s" ' % (nu.dn, nu.ca))
            atts = o.split("\n")
            for a in atts:
                (key,val)=a.split('=')
                print("for user %s found attribute %s=%s" % (nu.dn, key,val))
                nu.__setattr__(key,val)
        except Exception, errMessage:
            print("error getting attribute(s) for %s, Error: %s" %(nu.dn, errMessage))
        cernmembers.append(nu)
    print("cached all members from CERN")

    
    print("retrieving members from BNL")
    (s,o) = commands.getstatusoutput("voms-admin --host vo.racf.bnl.gov --vo atlas list-members /atlas")
    users = o.split("\n")
    print("found %d members at BNL" %  len(users))
    for u in users:
        (udn, uca) = u.split(',')
        nu = Member(udn.strip(), uca.strip())
        bnlmembers.append(nu)
    print("cached all members from CERN")
    
    for m in cernmembers:
        if m not in bnlmembers:
            print("member %s not in BNL, adding..." % m.dn)
            (s,o) = commands.getstatusoutput('voms-admin --nousercert --host vo.racf.bnl.gov --vo atlas create-user "%s" "%s" "" "" ' % (m.dn, m.ca))
            if s == 0:
                print("create user %s succeeded." % m.dn)
            else:
                print("create user %s failed. Error: %s" % (m.dn, o))
            (s,o) = commands.getstatusoutput('voms-admin --nousercert --host vo.racf.bnl.gov --vo atlas set-user-attribute "%s" "%s" nickname %s ' % (m.dn,m.ca,m.nickname))
            if s == 0:
                print("set-attribute nickname for user %s succeeded." % m.dn)
            else:
                print("set-attribute nickname for user %s failed. Error: %s" % (m.dn, o))


def syncRoles():
    pass

def syncGroups():
    pass
    
    
def main():
    print("syncing members...")
    syncMembers()
    print("done synching members.")
    
    
    
    
main()    
    
    
