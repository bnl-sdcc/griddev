VOMS utilites
================

Python tools for dealing with Virtual Organization Management Service

Tried to use SOAPpy and got "Invalid soap:fault binding element" errors.


URL to retrieve XML-formatted list of DNs from VOMS. 
https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?method=listMembers
https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?wsdl for WSDL
General form of queries with parameters:
https://lcg-voms.cern.ch:8443/voms/atlas/services/VOMSAdmin?method=listMembers&groupname=/atlas/usatlas

For testing outside of python, this works...
 wget --no-check-certificate --private-key /home/jhover/.globus/userkey.pem  
 --certificate /home/jhover/.globus/usercert.pem  
 https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?method=listMembers

 Method	                   P1          P2         P3
===========================================================
 INFORMATIONAL METHODS (implement first)
 ----------------------------------------------------------
 getMajorVersionNumber
 getMinorVersionNumber
 getPatchVersionNumber
 getVOName
 listRoles
 listCapabilities 
 listCAs
 listMembers
 listMembers               groupname
 listSubGroups             groupname
 getUser                   username     userca
 listUsersWithRole         groupname    rolename
 listUsersWithCapability   capability
 getGroupPath              groupname
 listGroups                username     userca
 listRoles                 username     userca
 listCapabilities          username     userca
 getACL                    container
 getDefaultACL             groupname 

 STATE ALTERING METHODS (implement later)
 ------------------------------------------------------------
 createUser                user
 createGroup               parentname   groupname
 deleteUser                username     userca
 deleteGroup               groupname
 createRole                rolename
 deleteRole                rolename
 createCapability          capability
 deleteCapability          capability
 addMember                 groupname    username    userca
 removeMember              groupname    username    userca
 assignRole                groupname    rolename    username   userca
 dismissRole               parentname   rolename    username   userca
 assignCapability          capability   username    userca
 dismissCapability         capability   username    userca
 setACL                    container    acl 
 addACLEntry               container    aclEntry
 removeACLEntry            container    aclEntry
 setDefaultACL             groupname    aclEntry
 addDefaultACL             groupname    aclEntry
 removeDefaultACLEntry     groupname    aclEntry
