#include "srmStub.h"
#include "soapSRMServerV1.nsmap"
main()
{
	struct soap soap;
	soap_init(&soap);


	if (soap_call_tns__ping ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "ping",/* struct tns__pingResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__getEstPutTime ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "getEstPutTime",/* struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOflong * arg2, struct ArrayOfboolean * arg3, struct ArrayOfstring * arg4, struct tns__getEstPutTimeResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__put ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "put",/* struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOflong * arg2, struct ArrayOfboolean * arg3, struct ArrayOfstring * arg4, struct tns__putResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__getRequestStatus ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "getRequestStatus",/* xsd__int  arg0, struct tns__getRequestStatusResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__copy ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "copy",/* struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOfboolean * arg2, struct tns__copyResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__getProtocols ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "getProtocols",/* struct tns__getProtocolsResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__getEstGetTime ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "getEstGetTime",/* struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct tns__getEstGetTimeResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__advisoryDelete ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "advisoryDelete",/* struct ArrayOfstring * arg0, struct tns__advisoryDeleteResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__pin ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "pin",/* struct ArrayOfstring * arg0, struct tns__pinResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__unPin ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "unPin",/* struct ArrayOfstring * arg0, xsd__int  arg1, struct tns__unPinResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__setFileStatus ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "setFileStatus",/* xsd__int  arg0, xsd__int  arg1, xsd__string  arg2, struct tns__setFileStatusResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__mkPermanent ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "mkPermanent",/* struct ArrayOfstring * arg0, struct tns__mkPermanentResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__get ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "get",/* struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct tns__getResponse * out*/ ))
		soap_print_fault(&soap,stderr);


	if (soap_call_tns__getFileMetaData ( &soap, "http://wacdr002d.cern.ch:8082/srm/managerv1", "getFileMetaData",/* struct ArrayOfstring * arg0, struct tns__getFileMetaDataResponse * out*/ ))
		soap_print_fault(&soap,stderr);


}
