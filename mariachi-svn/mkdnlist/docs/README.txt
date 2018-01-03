URL to retrieve XML-formatted list of DNs from VOMS. 

https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?method=listMembers


This also works:
 wget --no-check-certificate --private-key /home/jhover/.globus/userkey.pem --certificate /home/jhover/.globus/usercert.pem https://voms.fnal.gov:8443/voms/cms/services/VOMSAdmin?method=listMembers

This is a small edit.

