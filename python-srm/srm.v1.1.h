//gsoap tns schema namespace: http://tempuri.org/diskCacheV111.srm.server.SRMServerV1
//gsoap mime schema namespace: http://schemas.xmlsoap.org/wsdl/mime/
//gsoap tme schema namespace: http://www.themindelectric.com/
//gsoap soapenc schema namespace: http://schemas.xmlsoap.org/soap/encoding/
//gsoap ns11 schema namespace: http://www.themindelectric.com/package/diskCacheV111.srm/
//gsoap http schema namespace: http://schemas.xmlsoap.org/wsdl/http/
//gsoap ns13 schema namespace: http://www.themindelectric.com/package/
//gsoap ns12 schema namespace: http://www.themindelectric.com/package/java.lang/

//gsoap tns service namespace: http://srm.1.0.ns

//gsoap tns service location: http://wacdr002d.cern.ch:8082/srm/managerv1
//gsoap tns service name: soapSRMServerV1

/*start primitive data types*/
typedef char * xsd__string;
typedef int xsd__int;
typedef char * xsd__dateTime;
typedef LONG64 xsd__long;
typedef enum { false_, true_ } xsd__boolean;

/*end primitive data types*/

struct tns__getResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__advisoryDeleteResponse {
};

struct ns11__RequestStatus {
	xsd__int  requestId;
	xsd__string  type;
	xsd__string  state;
	xsd__dateTime  submitTime;
	xsd__dateTime  startTime;
	xsd__dateTime  finishTime;
	xsd__int  estTimeToStart;
	struct ArrayOfRequestFileStatus * fileStatuses;
	xsd__string  errorMessage;
	xsd__int  retryDeltaTime;
};

struct ArrayOfFileMetaData {
	struct ns11__FileMetaData * __ptr;
	int  __size;
	int  __offset;
};

struct ArrayOfstring {
	xsd__string * __ptr;
	int  __size;
	int  __offset;
};

struct ArrayOflong {
	xsd__long * __ptr;
	int  __size;
	int  __offset;
};

struct tns__putResponse {
	struct ns11__RequestStatus * _Result;
};

struct ArrayOfRequestFileStatus {
	struct ns11__RequestFileStatus * __ptr;
	int  __size;
	int  __offset;
};

struct tns__mkPermanentResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__copyResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__getEstGetTimeResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__getEstPutTimeResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__pinResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__pingResponse {
	xsd__boolean  _Result;
};

struct tns__getFileMetaDataResponse {
	struct ArrayOfFileMetaData * _Result;
};

typedef xsd__boolean  tns__Boolean ;

struct tns__getRequestStatusResponse {
	struct ns11__RequestStatus * _Result;
};

struct tns__getProtocolsResponse {
	struct ArrayOfstring * _Result;
};

struct tns__setFileStatusResponse {
	struct ns11__RequestStatus * _Result;
};

typedef xsd__long  tns__Long ;

struct ns11__FileMetaData {
	xsd__string  SURL;
	xsd__long  size;
	xsd__string  owner;
	xsd__string  group;
	xsd__int  permMode;
	xsd__string  checksumType;
	xsd__string  checksumValue;
	xsd__boolean  isPinned;
	xsd__boolean  isPermanent;
	xsd__boolean  isCached;
};

struct tns__unPinResponse {
	struct ns11__RequestStatus * _Result;
};

typedef xsd__int  tns__Integer ;

struct ArrayOfboolean {
	xsd__boolean * __ptr;
	int  __size;
	int  __offset;
};

struct ns11__RequestFileStatus {
	xsd__string  SURL;
	xsd__long  size;
	xsd__string  owner;
	xsd__string  group;
	xsd__int  permMode;
	xsd__string  checksumType;
	xsd__string  checksumValue;
	xsd__boolean  isPinned;
	xsd__boolean  isPermanent;
	xsd__boolean  isCached;
	xsd__string  state;
	xsd__int  fileId;
	xsd__string  TURL;
	xsd__int  estSecondsToStart;
	xsd__string  sourceFilename;
	xsd__string  destFilename;
	xsd__int  queueOrder;
};

//gsoap tns service method-action: ping "ping"
tns__ping( struct tns__pingResponse * out );
//gsoap tns service method-action: getEstPutTime "getEstPutTime"
tns__getEstPutTime( struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOflong * arg2, struct ArrayOfboolean * arg3, struct ArrayOfstring * arg4, struct tns__getEstPutTimeResponse * out );
//gsoap tns service method-action: put "put"
tns__put( struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOflong * arg2, struct ArrayOfboolean * arg3, struct ArrayOfstring * arg4, struct tns__putResponse * out );
//gsoap tns service method-action: getRequestStatus "getRequestStatus"
tns__getRequestStatus( xsd__int  arg0, struct tns__getRequestStatusResponse * out );
//gsoap tns service method-action: copy "copy"
tns__copy( struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct ArrayOfboolean * arg2, struct tns__copyResponse * out );
//gsoap tns service method-action: getProtocols "getProtocols"
tns__getProtocols( struct tns__getProtocolsResponse * out );
//gsoap tns service method-action: getEstGetTime "getEstGetTime"
tns__getEstGetTime( struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct tns__getEstGetTimeResponse * out );
//gsoap tns service method-action: advisoryDelete "advisoryDelete"
tns__advisoryDelete( struct ArrayOfstring * arg0, struct tns__advisoryDeleteResponse * out );
//gsoap tns service method-action: pin "pin"
tns__pin( struct ArrayOfstring * arg0, struct tns__pinResponse * out );
//gsoap tns service method-action: unPin "unPin"
tns__unPin( struct ArrayOfstring * arg0, xsd__int  arg1, struct tns__unPinResponse * out );
//gsoap tns service method-action: setFileStatus "setFileStatus"
tns__setFileStatus( xsd__int  arg0, xsd__int  arg1, xsd__string  arg2, struct tns__setFileStatusResponse * out );
//gsoap tns service method-action: mkPermanent "mkPermanent"
tns__mkPermanent( struct ArrayOfstring * arg0, struct tns__mkPermanentResponse * out );
//gsoap tns service method-action: get "get"
tns__get( struct ArrayOfstring * arg0, struct ArrayOfstring * arg1, struct tns__getResponse * out );
//gsoap tns service method-action: getFileMetaData "getFileMetaData"
tns__getFileMetaData( struct ArrayOfstring * arg0, struct tns__getFileMetaDataResponse * out );
