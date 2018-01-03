#include "libsrm_v1_1.h"

#include <sys/types.h>
#include <errno.h>
#include <grp.h>
#include <pwd.h>
#include <stdio.h>
#include <sys/stat.h>
#include "srmH.h"
#include "soapSRMServerV1.nsmap"
#include "cgsi_plugin.h"


save_errmsg (char **errbuf, const char *errmsg)
{
  *errbuf = strdup(errmsg);
}


int
srm_ping(char *srmep, char **errbuf)
{
  struct tns__pingResponse out;
  struct soap soap;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  if (soap_call_tns__ping (&soap, srmep,
			   "ping", &out)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    soap_print_fault (&soap, stderr);
    save_errmsg (errbuf, soap.fault->faultstring);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  soap_end (&soap);
  soap_done (&soap);
  return (out._Result);
}


int
srm_setfilestatus(char *srmep, int reqid, int fileid, char *state, char **errbuf)
{
  struct tns__setFileStatusResponse out;
  struct soap soap;
  int flags;
  
  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);
  
  if (soap_call_tns__setFileStatus (&soap, srmep,
				    "setFileStatus", reqid, fileid, state, &out)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    soap_print_fault (&soap, stderr);
    save_errmsg (errbuf, soap.fault->faultstring);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  soap_end (&soap);
  soap_done (&soap);
  return (0);
}


int
srm_get(char *srmep, int nbfiles, char **surls, int nbprotocols, char **protocols,
        int *reqid, struct srm_filestatus **filestatuses, char **errbuf)
{
  int errflag = 0;
  struct ns11__RequestFileStatus *f;
  struct srm_filestatus *fs;
  int i;
  int n;
  struct tns__getResponse outg;
  char *p;
  struct ArrayOfstring protoarray;
  struct ns11__RequestStatus *reqstatp;
  int sav_errno;
  struct soap soap;
  struct ArrayOfstring surlarray;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  surlarray.__ptr = (char **)surls;
  surlarray.__size = nbfiles;
  surlarray.__offset = 0;
  protoarray.__ptr = protocols;
  protoarray.__size = nbprotocols;
  protoarray.__offset = 0;

  if (soap_call_tns__get (&soap, srmep, "get", &surlarray,
			  &protoarray, &outg)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    soap_print_fault (&soap, stderr);
    save_errmsg (errbuf, soap.fault->faultstring);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  reqstatp = outg._Result;
  if (reqstatp->fileStatuses == NULL) {
    save_errmsg(errbuf, "protocol not supported. fileStatuses is null");
    soap_end (&soap);
    soap_done (&soap);
    errno = EPROTONOSUPPORT;
    return (-1);
  }
  *reqid = reqstatp->requestId;
  n = reqstatp->fileStatuses->__size;
  if ((*filestatuses = malloc (n * sizeof(struct srm_filestatus))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating fileStatuses");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  f = reqstatp->fileStatuses->__ptr;
  fs = *filestatuses;
  for (i = 0; i < n; i++) {
    if ((f+i)->SURL && (fs->surl = strdup ((f+i)->SURL)) == NULL)
      errflag++;
    if ((f+i)->state) {
      if (strcmp ((f+i)->state, "Pending") == 0 ||
	  strcmp ((f+i)->state, "pending") == 0)
	fs->status = 0;
      else if (strcmp ((f+i)->state, "Failed") == 0 ||
	       strcmp ((f+i)->state, "failed") == 0)
	fs->status = -1;
      else
	fs->status = 1;
    }
    fs->fileid = (f+i)->fileId;
    if ((f+i)->TURL && (fs->turl = strdup ((f+i)->TURL)) == NULL)
      errflag++;
    fs++;
  }
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}


#define DEFPOLLINT 10

int
srm_put(char *srmep, int nbfiles, char **surls, int *filesizes, int nbprotocols, char **protocols,
        int *reqid, int **fileids, char **token, char ***turls, char **errbuf)
{
  int *f;
  int i;
  int n;
  struct tns__putResponse outp;
  struct tns__getRequestStatusResponse outq;
  char *p;
  struct ArrayOfboolean permarray;
  struct ArrayOfstring protoarray;
  int r = 0;
  struct ns11__RequestStatus *reqstatp;
  int sav_errno;
  struct ArrayOflong sizearray;
  struct soap soap;
  struct ArrayOfstring srcarray;
  struct ArrayOfstring surlarray;
  char **t;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  surlarray.__ptr = (char **)surls;
  surlarray.__size = nbfiles;
  surlarray.__offset = 0;
  protoarray.__ptr = protocols;
  protoarray.__size = nbprotocols;
  protoarray.__offset = 0;

  srcarray.__ptr = (char **)surls;
  srcarray.__size = nbfiles;
  srcarray.__offset = 0;
  sizearray.__ptr = filesizes;
  sizearray.__size = nbfiles;
  sizearray.__offset = 0;
  if ((permarray.__ptr =
       soap_malloc (&soap, nbfiles * sizeof(xsd__boolean))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating array xsd__boolean");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  for (i = 0; i< nbfiles; i++)
    permarray.__ptr[i] = true_;
  permarray.__size = nbfiles;
  permarray.__offset = 0;
  if (soap_call_tns__put (&soap, srmep, "put", &srcarray,
			  &surlarray, &sizearray, &permarray, &protoarray, &outp)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    soap_print_fault (&soap, stderr);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  reqstatp = outp._Result;
  if (reqstatp->fileStatuses == NULL) {
    save_errmsg(errbuf, "protocol not supported. fileStatuses is null");
    soap_end (&soap);
    soap_done (&soap);
    errno = EPROTONOSUPPORT;
    return (-1);
  }
  *reqid = reqstatp->requestId;
  /* wait for file "ready" */
  while (strcmp (reqstatp->state, "pending") == 0 ||
	 strcmp (reqstatp->state, "Pending") == 0) {
    sleep ((r++ == 0) ? 1 : (reqstatp->retryDeltaTime > 0) ?
	   reqstatp->retryDeltaTime : DEFPOLLINT);
    if (soap_call_tns__getRequestStatus (&soap, srmep,
					 "getRequestStatus", *reqid, &outq)) {
      if (soap.error == SOAP_EOF) {
        save_errmsg(errbuf, "connection fails or timeout");
        soap_end (&soap);
        soap_done (&soap);
        return (-1);
      }
      save_errmsg (errbuf, soap.fault->faultstring);
      soap_print_fault (&soap, stderr);
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    reqstatp = outq._Result;
  }
  if (strcmp (reqstatp->state, "failed") == 0 ||
      strcmp (reqstatp->state, "Failed") == 0) {
    if (reqstatp->errorMessage) {
      if (strstr (reqstatp->errorMessage, "ile exists"))
	sav_errno = EEXIST;
      else if (strstr (reqstatp->errorMessage, "does not exist") ||
	       strstr (reqstatp->errorMessage, "GetStorageInfoFailed"))
	sav_errno = ENOENT;
      else if (strstr (reqstatp->errorMessage, "nvalid arg"))
	sav_errno = EINVAL;
      else if (strstr (reqstatp->errorMessage, "protocol"))
	sav_errno = EPROTONOSUPPORT;
      else
	sav_errno = ECOMM;
    } else
      sav_errno = ECOMM;
    save_errmsg (errbuf, reqstatp->errorMessage);
    soap_end (&soap);
    soap_done (&soap);
    errno = sav_errno;
    return (-1);
  }
  n = reqstatp->fileStatuses->__size;
  if ((f = malloc (n * sizeof(int))) == NULL ||
      (t = malloc (n * sizeof(char *))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating arrays int and char*");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  for (i = 0; i < n; i++) {
    f[i] = (reqstatp->fileStatuses->__ptr+i)->fileId;
    if (strcmp ((reqstatp->fileStatuses->__ptr+i)->state, "ready") &&
	strcmp ((reqstatp->fileStatuses->__ptr+i)->state, "Ready"))
      t[i] = NULL;
    else
      t[i] = strdup ((reqstatp->fileStatuses->__ptr+i)->TURL);
  }
  *fileids = f;
  *token = NULL;
  *turls = t;
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}


int
srm_getrequeststatus(char *srmep, int reqid,
                     struct srm_filestatus **filestatuses, char **errbuf)
{
  int errflag = 0;
  struct ns11__RequestFileStatus *f;
  struct srm_filestatus *fs;
  int i;
  int n;
  struct tns__getRequestStatusResponse outq;
  char *p;
  struct ns11__RequestStatus *reqstatp;
  int sav_errno;
  struct soap soap;
  struct ArrayOfstring surlarray;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  if (soap_call_tns__getRequestStatus (&soap, srmep,
				       "getRequestStatus", reqid, &outq)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    save_errmsg (errbuf, soap.fault->faultstring);
    soap_print_fault (&soap, stderr);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  reqstatp = outq._Result;
  n = reqstatp->fileStatuses->__size;
  if ((*filestatuses = malloc (n * sizeof(struct srm_filestatus))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating array filestatuses");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  f = reqstatp->fileStatuses->__ptr;
  fs = *filestatuses;
  for (i = 0; i < n; i++) {
    if ((f+i)->SURL && (fs->surl = strdup ((f+i)->SURL)) == NULL)
      errflag++;
    if ((f+i)->state) {
      if (strcmp ((f+i)->state, "Pending") == 0 ||
	  strcmp ((f+i)->state, "pending") == 0)
	fs->status = 0;
      else if (strcmp ((f+i)->state, "Failed") == 0 ||
	       strcmp ((f+i)->state, "failed") == 0)
	fs->status = -1;
      else
	fs->status = 1;
    }
    fs->fileid = (f+i)->fileId;
    if ((f+i)->TURL && (fs->turl = strdup ((f+i)->TURL)) == NULL)
      errflag++;
    fs++;
  }
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}


int
srm_getfilemetadata(char *srmep, int nbfiles, char **surls, struct srm_filemetadata **metadata,
                    char **errbuf)
{
  struct tns__getFileMetaDataResponse out;
  struct ns11__FileMetaData *f;
  struct srm_filemetadata *fm;
  int ret;
  int n;
  int i;
  int sav_errno;
  int flags;
  struct soap soap;
  struct ArrayOfstring surlarray;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);
  
  /* issue "getFileMetaData" request */
  
  surlarray.__ptr = (char **)surls;
  surlarray.__size = nbfiles;
  surlarray.__offset = 0;
  
  if ((ret = soap_call_tns__getFileMetaData (&soap, srmep,
                                             "getFileMetaData", &surlarray, &out))) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_print_fault (&soap, stderr);
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    if (ret == SOAP_FAULT || ret == SOAP_CLI_FAULT) {
      if (strstr (soap.fault->faultstring, "No such file") ||
          strstr (soap.fault->faultstring, "could not get storage info by path"))
        sav_errno = ENOENT;
      else
        sav_errno = ECOMM;
    } else
      sav_errno = ECOMM;
    save_errmsg(errbuf, soap.fault->faultstring);
    soap_end (&soap);
    soap_done (&soap);
    errno = sav_errno;
    return (-1);
  }
  if (out._Result->__size == 0 || out._Result->__ptr[0].SURL == NULL) {
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOENT;
    return (-1);
  }

  n = out._Result->__size;
  if ((*metadata = malloc (n * sizeof(struct srm_filemetadata))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating array filestatuses");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  } 
  fm = *metadata;
  f = out._Result->__ptr; 
  for (i=0; i<n; i++) {
    fm->surl = strdup((f+i)->SURL);
    fm->size = (f+i)->size;
    fm->owner = ((f+i)->owner) ? strdup((f+i)->owner) : NULL;
    fm->group = ((f+i)->group) ? strdup((f+i)->group) : NULL;
    fm->permMode = (f+i)->permMode;
    fm->checksumType = ((f+i)->checksumType) ? strdup((f+i)->checksumType) : NULL;
    fm->checksumValue = ((f+i)->checksumValue) ? strdup((f+i)->checksumValue) : NULL;
    fm->isPinned = (f+i)->isPinned;
    fm->isPermanent = (f+i)->isPermanent;
    fm->isCached = (f+i)->isCached;
    fm++;
  }
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}


int
srm_pin(char *srmep, int nbfiles, char **surls,
        int *reqid, struct srm_filestatus **filestatuses, char **errbuf)
{
  int errflag = 0;
  struct ns11__RequestFileStatus *f;
  struct srm_filestatus *fs;
  int i;
  int n;
  struct tns__pinResponse outg;
  struct ns11__RequestStatus *reqstatp;
  struct soap soap;
  struct ArrayOfstring surlarray;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  surlarray.__ptr = (char **)surls;
  surlarray.__size = nbfiles;
  surlarray.__offset = 0;

  if (soap_call_tns__pin (&soap, srmep, "pin", &surlarray,
                          &outg)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    save_errmsg(errbuf, soap.fault->faultstring);
    soap_print_fault (&soap, stderr);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  reqstatp = outg._Result;
  if (reqstatp->fileStatuses == NULL) {
    save_errmsg(errbuf, "protocol not supported. fileStatuses is null");
    soap_end (&soap);
    soap_done (&soap);
    errno = EPROTONOSUPPORT;
    return (-1);
  }
  *reqid = reqstatp->requestId;
  n = reqstatp->fileStatuses->__size;
  if ((*filestatuses = malloc (n * sizeof(struct srm_filestatus))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating fileStatuses");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  f = reqstatp->fileStatuses->__ptr;
  fs = *filestatuses;
  for (i = 0; i < n; i++) {
    if ((f+i)->SURL && (fs->surl = strdup ((f+i)->SURL)) == NULL)
      errflag++;
    if ((f+i)->state) {
      if (strcmp ((f+i)->state, "Pending") == 0 ||
	  strcmp ((f+i)->state, "pending") == 0)
	fs->status = 0;
      else if (strcmp ((f+i)->state, "Failed") == 0 ||
	       strcmp ((f+i)->state, "failed") == 0)
	fs->status = -1;
      else
	fs->status = 1;
    }
    fs->fileid = (f+i)->fileId;
    if ((f+i)->TURL && (fs->turl = strdup ((f+i)->TURL)) == NULL)
      errflag++;
    fs++;
  }
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}


int
srm_unpin(char *srmep, int nbfiles, char **surls, int reqid, struct srm_filestatus **filestatuses,
          char **errbuf)
{
  int errflag = 0;
  struct ns11__RequestFileStatus *f;
  struct srm_filestatus *fs;
  int i;
  int n;
  struct tns__unPinResponse outg;
  struct ns11__RequestStatus *reqstatp;
  struct soap soap;
  struct ArrayOfstring surlarray;
  int flags;

  soap_init (&soap);
  flags = CGSI_OPT_DISABLE_NAME_CHECK;
  soap_register_plugin_arg (&soap, client_cgsi_plugin, &flags);

  surlarray.__ptr = (char **)surls;
  surlarray.__size = nbfiles;
  surlarray.__offset = 0;

  if (soap_call_tns__unPin (&soap, srmep, "unPin", &surlarray, reqid,
                            &outg)) {
    if (soap.error == SOAP_EOF) {
      save_errmsg(errbuf, "connection fails or timeout");
      soap_end (&soap);
      soap_done (&soap);
      return (-1);
    }
    save_errmsg(errbuf, soap.fault->faultstring);
    soap_print_fault (&soap, stderr);
    soap_end (&soap);
    soap_done (&soap);
    return (-1);
  }
  reqstatp = outg._Result;
  if (reqstatp->fileStatuses == NULL) {
    save_errmsg(errbuf, "protocol not supported. fileStatuses is null");
    soap_end (&soap);
    soap_done (&soap);
    errno = EPROTONOSUPPORT;
    return (-1);
  }
  n = reqstatp->fileStatuses->__size;
  if ((*filestatuses = malloc (n * sizeof(struct srm_filestatus))) == NULL) {
    save_errmsg(errbuf, "out of memory allocating fileStatuses");
    soap_end (&soap);
    soap_done (&soap);
    errno = ENOMEM;
    return (-1);
  }
  f = reqstatp->fileStatuses->__ptr;
  fs = *filestatuses;
  for (i = 0; i < n; i++) {
    if ((f+i)->SURL && (fs->surl = strdup ((f+i)->SURL)) == NULL)
      errflag++;
    if ((f+i)->state) {
      if (strcmp ((f+i)->state, "Pending") == 0 ||
	  strcmp ((f+i)->state, "pending") == 0)
	fs->status = 0;
      else if (strcmp ((f+i)->state, "Failed") == 0 ||
	       strcmp ((f+i)->state, "failed") == 0)
	fs->status = -1;
      else
	fs->status = 1;
    }
    fs->fileid = (f+i)->fileId;
    if ((f+i)->TURL && (fs->turl = strdup ((f+i)->TURL)) == NULL)
      errflag++;
    fs++;
  }
  soap_end (&soap);
  soap_done (&soap);
  return (n);
}
