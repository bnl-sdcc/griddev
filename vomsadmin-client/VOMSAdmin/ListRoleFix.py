from VOMSAdminService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
import ZSI

class listRolesRequest:
    def __init__(self):
        self._in0 = None
        self._in1 = None
        return
listRolesRequest.typecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.admin","listRoles"), 
                                   ofwhat=[], 
                                   pyclass=listRolesRequest, 
                                   encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.admin")

class listRolesResponse:
    def __init__(self):
        self._listRolesReturn = None
        return
listRolesResponse.typecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.admin","listRolesResponse"), 
                                    ofwhat=[ns1.ArrayOf_soapenc_string_Def(pname="listRolesReturn", aname="_listRolesReturn", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                    pyclass=listRolesResponse, 
                                    encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.admin")
