/* srmServer.c
   Generated by gSOAP 2.3.8 from srm.v1.1.h
   Copyright (C) 2001-2003 Genivia inc.
   All Rights Reserved.
*/
#include "srmH.h"
#ifdef __cplusplus
extern "C" {
#endif

SOAP_BEGIN_NAMESPACE(srm)

SOAP_SOURCE_STAMP("@(#) srmServer.c ver 2.3.8 2005-12-30 21:07:31 GMT")


SOAP_FMAC5 int SOAP_FMAC6 soap_serve(struct soap *soap)
{
	unsigned int n = SOAP_MAXKEEPALIVE;
	do
	{	soap_begin(soap);
		if (!--n)
			soap->keep_alive = 0;
		if (soap_begin_recv(soap))
		{	if (soap->error < SOAP_STOP)
				return soap_send_fault(soap);
			else
				continue;
		}
		if (soap_envelope_begin_in(soap) || soap_recv_header(soap) || soap_body_begin_in(soap))
			return soap_send_fault(soap);
		if (soap_peek_element(soap))
			return soap->error;
		if (!soap_match_tag(soap, soap->tag, "tns:ping"))
			soap_serve_tns__ping(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:getEstPutTime"))
			soap_serve_tns__getEstPutTime(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:put"))
			soap_serve_tns__put(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:getRequestStatus"))
			soap_serve_tns__getRequestStatus(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:copy"))
			soap_serve_tns__copy(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:getProtocols"))
			soap_serve_tns__getProtocols(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:getEstGetTime"))
			soap_serve_tns__getEstGetTime(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:advisoryDelete"))
			soap_serve_tns__advisoryDelete(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:pin"))
			soap_serve_tns__pin(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:unPin"))
			soap_serve_tns__unPin(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:setFileStatus"))
			soap_serve_tns__setFileStatus(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:mkPermanent"))
			soap_serve_tns__mkPermanent(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:get"))
			soap_serve_tns__get(soap);
		else if (!soap_match_tag(soap, soap->tag, "tns:getFileMetaData"))
			soap_serve_tns__getFileMetaData(soap);
		else 
			soap->error = SOAP_NO_METHOD;
		if (soap->error)
			return soap_send_fault(soap);
	} while (soap->keep_alive);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__ping(struct soap *soap)
{	struct tns__ping soap_tmp_tns__ping;
	struct tns__pingResponse out;
	soap_default_tns__pingResponse(soap, &out);
	soap_default_tns__ping(soap, &soap_tmp_tns__ping);
	soap_get_tns__ping(soap, &soap_tmp_tns__ping, "tns:ping", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__ping(soap, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__pingResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__pingResponse(soap, &out, "tns:pingResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__pingResponse(soap, &out, "tns:pingResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__getEstPutTime(struct soap *soap)
{	struct tns__getEstPutTime soap_tmp_tns__getEstPutTime;
	struct tns__getEstPutTimeResponse out;
	soap_default_tns__getEstPutTimeResponse(soap, &out);
	soap_default_tns__getEstPutTime(soap, &soap_tmp_tns__getEstPutTime);
	soap_get_tns__getEstPutTime(soap, &soap_tmp_tns__getEstPutTime, "tns:getEstPutTime", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__getEstPutTime(soap, soap_tmp_tns__getEstPutTime.arg0, soap_tmp_tns__getEstPutTime.arg1, soap_tmp_tns__getEstPutTime.arg2, soap_tmp_tns__getEstPutTime.arg3, soap_tmp_tns__getEstPutTime.arg4, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getEstPutTimeResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getEstPutTimeResponse(soap, &out, "tns:getEstPutTimeResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getEstPutTimeResponse(soap, &out, "tns:getEstPutTimeResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__put(struct soap *soap)
{	struct tns__put soap_tmp_tns__put;
	struct tns__putResponse out;
	soap_default_tns__putResponse(soap, &out);
	soap_default_tns__put(soap, &soap_tmp_tns__put);
	soap_get_tns__put(soap, &soap_tmp_tns__put, "tns:put", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__put(soap, soap_tmp_tns__put.arg0, soap_tmp_tns__put.arg1, soap_tmp_tns__put.arg2, soap_tmp_tns__put.arg3, soap_tmp_tns__put.arg4, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__putResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__putResponse(soap, &out, "tns:putResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__putResponse(soap, &out, "tns:putResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__getRequestStatus(struct soap *soap)
{	struct tns__getRequestStatus soap_tmp_tns__getRequestStatus;
	struct tns__getRequestStatusResponse out;
	soap_default_tns__getRequestStatusResponse(soap, &out);
	soap_default_tns__getRequestStatus(soap, &soap_tmp_tns__getRequestStatus);
	soap_get_tns__getRequestStatus(soap, &soap_tmp_tns__getRequestStatus, "tns:getRequestStatus", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__getRequestStatus(soap, soap_tmp_tns__getRequestStatus.arg0, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getRequestStatusResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getRequestStatusResponse(soap, &out, "tns:getRequestStatusResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getRequestStatusResponse(soap, &out, "tns:getRequestStatusResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__copy(struct soap *soap)
{	struct tns__copy soap_tmp_tns__copy;
	struct tns__copyResponse out;
	soap_default_tns__copyResponse(soap, &out);
	soap_default_tns__copy(soap, &soap_tmp_tns__copy);
	soap_get_tns__copy(soap, &soap_tmp_tns__copy, "tns:copy", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__copy(soap, soap_tmp_tns__copy.arg0, soap_tmp_tns__copy.arg1, soap_tmp_tns__copy.arg2, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__copyResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__copyResponse(soap, &out, "tns:copyResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__copyResponse(soap, &out, "tns:copyResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__getProtocols(struct soap *soap)
{	struct tns__getProtocols soap_tmp_tns__getProtocols;
	struct tns__getProtocolsResponse out;
	soap_default_tns__getProtocolsResponse(soap, &out);
	soap_default_tns__getProtocols(soap, &soap_tmp_tns__getProtocols);
	soap_get_tns__getProtocols(soap, &soap_tmp_tns__getProtocols, "tns:getProtocols", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__getProtocols(soap, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getProtocolsResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getProtocolsResponse(soap, &out, "tns:getProtocolsResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getProtocolsResponse(soap, &out, "tns:getProtocolsResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__getEstGetTime(struct soap *soap)
{	struct tns__getEstGetTime soap_tmp_tns__getEstGetTime;
	struct tns__getEstGetTimeResponse out;
	soap_default_tns__getEstGetTimeResponse(soap, &out);
	soap_default_tns__getEstGetTime(soap, &soap_tmp_tns__getEstGetTime);
	soap_get_tns__getEstGetTime(soap, &soap_tmp_tns__getEstGetTime, "tns:getEstGetTime", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__getEstGetTime(soap, soap_tmp_tns__getEstGetTime.arg0, soap_tmp_tns__getEstGetTime.arg1, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getEstGetTimeResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getEstGetTimeResponse(soap, &out, "tns:getEstGetTimeResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getEstGetTimeResponse(soap, &out, "tns:getEstGetTimeResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__advisoryDelete(struct soap *soap)
{	struct tns__advisoryDelete soap_tmp_tns__advisoryDelete;
	struct tns__advisoryDeleteResponse out;
	soap_default_tns__advisoryDeleteResponse(soap, &out);
	soap_default_tns__advisoryDelete(soap, &soap_tmp_tns__advisoryDelete);
	soap_get_tns__advisoryDelete(soap, &soap_tmp_tns__advisoryDelete, "tns:advisoryDelete", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__advisoryDelete(soap, soap_tmp_tns__advisoryDelete.arg0, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__advisoryDeleteResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__advisoryDeleteResponse(soap, &out, "tns:advisoryDeleteResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__advisoryDeleteResponse(soap, &out, "tns:advisoryDeleteResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__pin(struct soap *soap)
{	struct tns__pin soap_tmp_tns__pin;
	struct tns__pinResponse out;
	soap_default_tns__pinResponse(soap, &out);
	soap_default_tns__pin(soap, &soap_tmp_tns__pin);
	soap_get_tns__pin(soap, &soap_tmp_tns__pin, "tns:pin", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__pin(soap, soap_tmp_tns__pin.arg0, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__pinResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__pinResponse(soap, &out, "tns:pinResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__pinResponse(soap, &out, "tns:pinResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__unPin(struct soap *soap)
{	struct tns__unPin soap_tmp_tns__unPin;
	struct tns__unPinResponse out;
	soap_default_tns__unPinResponse(soap, &out);
	soap_default_tns__unPin(soap, &soap_tmp_tns__unPin);
	soap_get_tns__unPin(soap, &soap_tmp_tns__unPin, "tns:unPin", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__unPin(soap, soap_tmp_tns__unPin.arg0, soap_tmp_tns__unPin.arg1, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__unPinResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__unPinResponse(soap, &out, "tns:unPinResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__unPinResponse(soap, &out, "tns:unPinResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__setFileStatus(struct soap *soap)
{	struct tns__setFileStatus soap_tmp_tns__setFileStatus;
	struct tns__setFileStatusResponse out;
	soap_default_tns__setFileStatusResponse(soap, &out);
	soap_default_tns__setFileStatus(soap, &soap_tmp_tns__setFileStatus);
	soap_get_tns__setFileStatus(soap, &soap_tmp_tns__setFileStatus, "tns:setFileStatus", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__setFileStatus(soap, soap_tmp_tns__setFileStatus.arg0, soap_tmp_tns__setFileStatus.arg1, soap_tmp_tns__setFileStatus.arg2, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__setFileStatusResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__setFileStatusResponse(soap, &out, "tns:setFileStatusResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__setFileStatusResponse(soap, &out, "tns:setFileStatusResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__mkPermanent(struct soap *soap)
{	struct tns__mkPermanent soap_tmp_tns__mkPermanent;
	struct tns__mkPermanentResponse out;
	soap_default_tns__mkPermanentResponse(soap, &out);
	soap_default_tns__mkPermanent(soap, &soap_tmp_tns__mkPermanent);
	soap_get_tns__mkPermanent(soap, &soap_tmp_tns__mkPermanent, "tns:mkPermanent", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__mkPermanent(soap, soap_tmp_tns__mkPermanent.arg0, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__mkPermanentResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__mkPermanentResponse(soap, &out, "tns:mkPermanentResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__mkPermanentResponse(soap, &out, "tns:mkPermanentResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__get(struct soap *soap)
{	struct tns__get soap_tmp_tns__get;
	struct tns__getResponse out;
	soap_default_tns__getResponse(soap, &out);
	soap_default_tns__get(soap, &soap_tmp_tns__get);
	soap_get_tns__get(soap, &soap_tmp_tns__get, "tns:get", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__get(soap, soap_tmp_tns__get.arg0, soap_tmp_tns__get.arg1, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getResponse(soap, &out, "tns:getResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getResponse(soap, &out, "tns:getResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_FMAC5 int SOAP_FMAC6 soap_serve_tns__getFileMetaData(struct soap *soap)
{	struct tns__getFileMetaData soap_tmp_tns__getFileMetaData;
	struct tns__getFileMetaDataResponse out;
	soap_default_tns__getFileMetaDataResponse(soap, &out);
	soap_default_tns__getFileMetaData(soap, &soap_tmp_tns__getFileMetaData);
	soap_get_tns__getFileMetaData(soap, &soap_tmp_tns__getFileMetaData, "tns:getFileMetaData", NULL);
	if (soap->error)
		return soap->error;
	
	if (soap_body_end_in(soap)
	 || soap_envelope_end_in(soap)
#ifndef WITH_LEANER
	 || soap_getattachments(soap)
#endif
	 || soap_end_recv(soap))
		return soap->error;
	soap->error = tns__getFileMetaData(soap, soap_tmp_tns__getFileMetaData.arg0, &out);
	if (soap->error)
		return soap->error;
	soap_serializeheader(soap);
	soap_serialize_tns__getFileMetaDataResponse(soap, &out);
	soap_begin_count(soap);
	if (soap->mode & SOAP_IO_LENGTH)
	{	soap_envelope_begin_out(soap);
		soap_putheader(soap);
		soap_body_begin_out(soap);
		soap_put_tns__getFileMetaDataResponse(soap, &out, "tns:getFileMetaDataResponse", "");
		soap_body_end_out(soap);
		soap_envelope_end_out(soap);
	};
	if (soap_response(soap, SOAP_OK)
	 || soap_envelope_begin_out(soap)
	 || soap_putheader(soap)
	 || soap_body_begin_out(soap)
	 || soap_put_tns__getFileMetaDataResponse(soap, &out, "tns:getFileMetaDataResponse", "")
	 || soap_body_end_out(soap)
	 || soap_envelope_end_out(soap)
#ifndef WITH_LEANER
	 || soap_putattachments(soap)
#endif
	 || soap_end_send(soap))
		return soap->error;
	soap_closesock(soap);
	return SOAP_OK;
}

SOAP_END_NAMESPACE(srm)

#ifdef __cplusplus
}
#endif

/* end of srmServer.c */