%module libgridftp
%{
#include "libgridftp.h"
%}

%include "cpointer.i"

%include "libgridftp.h"

%pointer_functions(long, long_ptr);
%array_functions(long, long_array);

%pointer_functions(char *, str_ptr);

