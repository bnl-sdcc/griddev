XERCES=/afs/cern.ch/atlas/offline/external/GRID/xerces-2_6_0
GSOAP=/afs/cern.ch/atlas/offline/external/GRID/gsoap-linux-2.3
GSOAP_IMP=/afs/cern.ch/atlas/offline/external/GRID/gsoap-linux-2.2.3
SWIG=/afs/cern.ch/atlas/offline/external/GRID/swig-1.3.21

PYTHON=/usr/include/python2.4/

CGSI_INC=/usr/include
CGSI_LIBS=/usr/lib

CC=cc -g -fPIC
SHLIBLDFLAGS=-shared

_libsrm_v1_1.so: libsrm_v1_1.o libsrm_v1_1_wrap.o stdsoap2.o srmC.o srmClient.o
	$(CC) $(SHLIBLDFLAGS) libsrm_v1_1.o libsrm_v1_1_wrap.o stdsoap2.o srmC.o srmClient.o -o _libsrm_v1_1.so -L$(CGSI_LIBS) -lcgsi_plugin_gsoap_2.6 -L$(GLOBUS_LOCATION)/lib -lglobus_gssapi_gsi_gcc32dbg -lglobus_gss_assist_gcc32dbg -lglobus_ftp_client_gcc32dbg -lglobus_gass_copy_gcc32dbg

srmtest: srmtest.c libsrm_v1_1.o stdsoap2.o srmC.o srmClient.o
	$(CC) -o srmtest  srmtest.c libsrm_v1_1.o stdsoap2.o srmC.o srmClient.o -L$(CGSI_LIBS) -lcgsi_plugin_gsoap_2.6 -L$(GLOBUS_LOCATION)/lib -lglobus_gssapi_gsi_gcc32dbg -lglobus_gss_assist_gcc32dbg -lglobus_ftp_client_gcc32dbg -lglobus_gass_copy_gcc32dbg

libsrm_v1_1.o: srmH.h srmStub.h soapSRMServerV1.nsmap libsrm_v1_1.h libsrm_v1_1.c
	$(CC) -c libsrm_v1_1.c -o libsrm_v1_1.o -I$(GSOAP)

libsrm_v1_1_wrap.o: libsrm_v1_1_wrap.c
	$(CC) -c libsrm_v1_1_wrap.c -o libsrm_v1_1_wrap.o -I$(PYTHON)

libsrm_v1_1_wrap.c libsrm_v1_1.py: libsrm_v1_1.i
	$(SWIG)/bin/swig -I$(SWIG)/lib/swig1.3/ -I$(SWIG)/lib/swig1.3/python -python libsrm_v1_1.i

stdsoap2.o: $(GSOAP)/stdsoap2.c
	$(CC) -c -I$(GSOAP) $(GSOAP)/stdsoap2.c

srmClient.o: srmClient.c
	$(CC) -c -I$(GSOAP) srmClient.c -o srmClient.o

srmServer.o: srmServer.c
	$(CC) -c -I$(GSOAP) srmServer.c -o srmServer.o

srmC.o: srmC.c
	$(CC) -c -I$(GSOAP) srmC.c -o srmC.o

srm.v1.1.o: srm.v1.1.c
	$(CC) -c -I$(GSOAP) srm.v1.1.c -o srm.v1.1.o

#srmH.h srmStub.h srmC.c srmClient.c soapSRMServerV1.nsmap: srm.v1.1.h
#	$(GSOAP)/soapcpp2 -c -p srm srm.v1.1.h

#CLASSPATH=$(GSOAP_IMP)/wsdlcpp:$(XERCES)/xmlParserAPIs.jar:$(XERCES)/xercesImpl.jar

#srm.v1.1.h: srm.v1.1.wsdl
#	java -classpath $(CLASSPATH) wsdlcpp -c srm.v1.1.wsdl

#clean:
#	rm -f soapSRMServerV1.* srmH.h libsrm_v1_1.py* libsrm_v1_1_wrap* *.o *.so *pyc *.xml *.xsd srmC* srmS* srmsoapSRMServerV1* srmtest
clean:
	rm -f libsrm_v1_1.py* libsrm_v1_1_wrap* *.o *.so *pyc *.xml *.xsd srmtest

