%module libsrm_v1_1
%{
#include "libsrm_v1_1.h"
%}

%include "cpointer.i"
%include "carrays.i"

%include "libsrm_v1_1.h"

%pointer_functions(struct srm_filestatus *, fslist_ptr);
%array_functions(struct srm_filestatus *, fslist_array);

%pointer_functions(struct srm_filestatus, fs_ptr);
%array_functions(struct srm_filestatus, fs_array);

%pointer_functions(struct srm_filemetadata *, fmdlist_ptr);
%array_functions(struct srm_filemetadata *, fmdlist_array);

%pointer_functions(struct srm_filemetadata, fmd_ptr);
%array_functions(struct srm_filemetadata, fmd_array);

%pointer_functions(int, int_ptr);
%array_functions(int, int_array);

%pointer_functions(int *, intlist_ptr);
%array_functions(int *, intlist_array);

%pointer_functions(char **, strlist_ptr);
%array_functions(char **, strlist_array);

%pointer_functions(char *, str_ptr);
%array_functions(char *, str_array);

