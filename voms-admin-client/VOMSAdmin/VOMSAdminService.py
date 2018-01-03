from VOMSAdminService_services import *
from ListRoleFix import *
from X509Helper import X509Helper
import sys
   
class VOMSAdmin:
    
    def __init__(self, **kw):
        self.port = VOMSAdminSoapBindingSOAP(**kw)
    
    def _callRemoteMethod(self, method_name, *args, **kw):
        
        try:
            res = self.port.__class__.__dict__[method_name](self.port, *args, **kw)
            return res
        
        except Exception, ex:
            print ex
            sys.exit(1)


    def getVOName(self):
        return self.getVoName()
    
    def getVoName(self):
        
        method_name = self.port.getVOName.__name__
        request = getVONameRequest()
        
        response = self._callRemoteMethod(method_name,request)
        return response._getVONameReturn
        
    
    def getUser(self, dn, ca):
        method_name = self.port.getUser.__name__
        request = getUserRequest()

        request._in0 = dn
        request._in1 = ca
        
        response = self._callRemoteMethod(method_name,request)
        return response._getUserReturn
        
    def createUser(self, dn,ca,cn,email):
                        
        method_name = self.port.createUser.__name__
        request = createUserRequest()
        
        u = ns0.User_Def(None)
        u._DN = dn
        u._CA = ca
        u._CN = cn
        u._mail = email
        
        
        request._in0 = u
        self._callRemoteMethod(method_name,request)
    
    
    def deleteUser(self,dn, ca):
        
        method_name = self.port.deleteUser.__name__
        request = deleteUserRequest()
        request._in0 = dn
        request._in1 = ca
        
        self._callRemoteMethod(method_name,request)
    
    
    
    def listUsers(self):
        vo_name = self.getVOName()
        return self.listMembers(vo_name)
    
    def createGroup(self, group_name):
        
        if not group_name.startswith("/"):
            group_name = self.getVOName()+"/"+group_name
        
        method_name = self.port.createGroup.__name__
        request = createGroupRequest()
        request._in0 = None
        request._in1 = group_name
        
        self._callRemoteMethod(method_name,request)
    
    def deleteGroup(self,group_name):
        if not group_name.startswith("/"):
            group_name = self.getVOName()+"/"+group_name
        
        method_name = self.port.deleteGroup.__name__
        request = deleteGroupRequest()
        request._in0 = group_name
        
        self._callRemoteMethod(method_name,request)
    
    
    def createRole(self,role_name):       
        method_name = self.port.createRole.__name__
        request = createRoleRequest()
        request._in0 = role_name
        
        self._callRemoteMethod(method_name,request)
    
    def deleteRole(self, role_name):
        method_name = self.port.deleteRole.__name__
        request = deleteRoleRequest()
        request._in0 = role_name
        
        self._callRemoteMethod(method_name,request)
        
    def  addMember(self,group_name, dn, ca):
        method_name = self.port.addMember.__name__
        
        request = addMemberRequest()
        
        request._in0 = group_name
        request._in1 = dn
        request._in2 = ca
        
        self._callRemoteMethod(method_name,request)
    
    def removeMember(self,group_name, dn, ca):
        
        method_name = self.port.removeMember.__name__
        
        request = removeMemberRequest()
        request._in0 = group_name
        request._in1 = dn
        request._in2 = ca
        
        self._callRemoteMethod(method_name,request)
    
    def assignRole(self, group_name, role_name, dn, ca):
        
        method_name = self.port.assignRole.__name__
        
        request = assignRoleRequest()
        request._in0 = group_name
        request._in1 = role_name
        request._in2 = dn
        request._in3 = ca
        
        self._callRemoteMethod(method_name,request)
        
    def dismissRole(self, group_name, role_name, dn, ca):
        
        method_name = self.port.dismissRole.__name__
        
        request = dismissRoleRequest()
        request._in0 = group_name
        request._in1 = role_name
        request._in2 = dn
        request._in3 = ca
        
        self._callRemoteMethod(method_name,request)
    
    def listMembers(self, group_name):
        
        method_name = self.port.listMembers.__name__
        
        request = listMembersRequest()
        request._in0 = group_name
        
        response = self._callRemoteMethod(method_name,request)
        return response._listMembersReturn
    
    def listUsersWithRole(self,group_name, role_name):
        
        method_name = self.port.listUsersWithRole.__name__
        
        request = listUsersWithRoleRequest()
        request._in0 = group_name
        request._in1 = role_name
        
        response = self._callRemoteMethod(method_name,request)
        return response._listUsersWithRoleReturn
    
    def listUserGroups(self,dn, ca):
        method_name = self.port.listGroups.__name__
        
        request = listGroupsRequest()
        request._in0 = dn
        request._in1 = ca
        
        response = self._callRemoteMethod(method_name,request)
        return response._listGroupsReturn
    
    
    def listUserRoles(self, dn,ca):
        return self.listRoles(dn, ca)
                    
    
    def listSubGroups(self,group_name):
        
        method_name = self.port.listSubGroups.__name__
        
        request = listSubGroupsRequest()
        request._in0 = group_name
        
        response = self._callRemoteMethod(method_name,request)
        return response._listSubGroupsReturn
    
    def listRoles(self, dn=None, ca=None):
        
        method_name = self.port.listRoles.__name__
        
        if (dn is None and ca is None):
            request = listRolesRequest()
        else:
            request = listRolesRequest1()
            request._in0 = dn
            request._in1 = ca
        
        response = self._callRemoteMethod(method_name,request)
        return response._listRolesReturn
                
        
    def listCas(self):
        
        method_name = self.port.listCAs.__name__
        request = listCAsRequest()
        
        response = self._callRemoteMethod(method_name, request)
        return response._listCAsReturn
    
    def getMajorVersionNumber(self):
        method_name = self.port.getMajorVersionNumber.__name__
        
        request = getMajorVersionNumberRequest()
        response = self._callRemoteMethod(method_name,request)
        return response._getMajorVersionNumberReturn
    
    def getMinorVersionNumber(self):
        method_name = self.port.getMinorVersionNumber.__name__
        
        request = getMinorVersionNumberRequest()
        response = self._callRemoteMethod(method_name,request)
        return response._getMinorVersionNumberReturn
    
    def getPatchVersionNumber(self):
        method_name = self.port.getPatchVersionNumber.__name__
        
        request = getPatchVersionNumberRequest()
        response = self._callRemoteMethod(method_name,request)
        return response._getPatchVersionNumberReturn
    
    def listGroups(self):
        
        def visitGroupTree(self, root, prefix=""):
            childrens = self.listSubGroups(root)
            
            print prefix, root
            if childrens is None:
                return
            
            for i in childrens:
                visitGroupTree(self,i, prefix+"\t")
            
        visitGroupTree(self, self.getVOName())
        
    

    