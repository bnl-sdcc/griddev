# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _libgridftp

def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types



deletefile = _libgridftp.deletefile

getfilesize = _libgridftp.getfilesize

new_long_ptr = _libgridftp.new_long_ptr

copy_long_ptr = _libgridftp.copy_long_ptr

delete_long_ptr = _libgridftp.delete_long_ptr

long_ptr_assign = _libgridftp.long_ptr_assign

long_ptr_value = _libgridftp.long_ptr_value

new_str_ptr = _libgridftp.new_str_ptr

copy_str_ptr = _libgridftp.copy_str_ptr

delete_str_ptr = _libgridftp.delete_str_ptr

str_ptr_assign = _libgridftp.str_ptr_assign

str_ptr_value = _libgridftp.str_ptr_value

