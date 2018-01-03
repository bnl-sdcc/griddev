#!/usr/bin/env python2.4
#
#  Vihuela Core Library
#  Created for the MARIACHI Project 
# http://www-mariachi.physics.sunysb.edu/
#
# Inspiration and recipes from 
#   http://www.hackorama.com/python/upload.shtml
#   http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
#
# MARIACHI Author:
#   John Hover <jhover@bnl.gov>
#
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#

import vihuela
import vihuela.core
import vihuela.plugins
import os, stat, sys, logging, threading, signal, time, sets
import mimetools, mimetypes, urllib, sgmllib

log = logging.getLogger()


class ThreadManager(object):
    """
    vihuela.core.ThreadManager
    
    This class manages all the Plugin object threads. 

    """    
    
    def __init__(self, config):
#        threading.Thread.__init__(self)
        self.log = logging.getLogger()
        self.log.debug('vihuela.core.ThreadManager.__init__()...')
        self.config = config
        sects = config.get('daemon','sections')
        self.sections = sects.split(',')
        self.threads = []

 
        
#    def run(self):
    def mainloop(self):
        self.log.debug('vihuela.core.ThreadManager.mainloop(): creating threads...')
        for sect in self.sections:
            # Retrieve class object of desired class
            k = self.config.get(sect, 'class')
            self.log.debug('ThreadManager.mainloop(): Processing: %s ' % k)
            
            # Turn it into an invokable 
            klassname = "vihuela.plugins.%s.%s" % (k,k)
            self.log.debug("vihuela.core.ThreadManager.mainloop(): Loading plugin class '%s'" % klassname)
            classobj = _get_class(klassname)
            # make one...                            )
            t = classobj(self.config,sect)
            #t = GridsiteUploader(self.config,sect)
            self.threads.append(t)
       
        # start all threads...
        for t in self.threads:
            t.start()
  
      
        # Continue while there are still threads alive        
        try:
            while(1):
                time.sleep(3)
                self.log.debug('vihuela.core.ThreadManager.mainloop(): Checking for interrupt...')
                
        except (KeyboardInterrupt): 
            logging.info("Shutdown via Ctrl-C or -INT signal.")
            logging.debug(" Shutting down all threads...")
            for t in self.threads:
                t.join()
               
        self.log.debug('vihuela.core.ThreadManager.run(): all threads joined.')    
        self.log.debug('vihuela.core.ThreadManager.run(): Done.')



class Plugin(threading.Thread):
    """
vihuela.core.Plugin -- Base object for plugin architecture. Handles logging, sleeptime
for detecting stopevents, and exec interval. 

 """
    
    def __init__(self, config, section, *args, **kwds):
        
        threading.Thread.__init__(self)
        self.config = config
        self.section = section
        self.stopevent = threading.Event()
        self.sleeptime = float(config.get(section,'sleeptime'))
        self.interval = float(config.get(section,'exec_interval'))
        self.log = logging.getLogger()
        self.log.debug('core.Plugin.__init__: Done.')
        
    def join(self,timeout=None):
        """
        Stop the thread. Overriding this method required to handle Ctrl-C from console.
        """
        self.stopevent.set()
        self.log.debug('%s.join(): [%s] Stopping thread....' % (self.klassname, self.section))
        threading.Thread.join(self, timeout)
    
    
    def run(self):
        self.log.info("%s.run(): [%s] Starting..." % (self.klassname, self.section))
        while not self.stopevent.isSet():
            self.log.debug("%s.run(): [%s] looping..." % (self.klassname, self.section))            
            self.run_action()
            self.stopevent.wait(self.interval)
            
        self.log.info("%s.run(): [%s] ending..." % (self.klassname, self.section))


#
# Dynamic class loader for plugins from Robert Brewer
# From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/223972
#

import types

def _get_mod(modulePath):
    try:
        aMod = sys.modules[modulePath]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        aMod = __import__(modulePath, globals(), locals(), [''])
        sys.modules[modulePath] = aMod
    return aMod

def _get_func(fullFuncName):
    """Retrieve a function object from a full dotted-package name."""
    
    # Parse out the path, module, and function
    lastDot = fullFuncName.rfind(u".")
    funcName = fullFuncName[lastDot + 1:]
    modPath = fullFuncName[:lastDot]
    
    aMod = _get_mod(modPath)
    aFunc = getattr(aMod, funcName)
    
    # Assert that the function is a *callable* attribute.
    assert callable(aFunc), u"%s is not callable." % fullFuncName
    
    # Return a reference to the function itself,
    # not the results of the function.
    return aFunc

def _get_class(fullClassName, parentClass=None):
    """Load a module and retrieve a class (NOT an instance).
    
    If the parentClass is supplied, className must be of parentClass
    or a subclass of parentClass (or None is returned).
    """
    aClass = _get_func(fullClassName)
    
    # Assert that the class is a subclass of parentClass.
    if parentClass is not None:
        if not issubclass(aClass, parentClass):
            raise TypeError(u"%s is not a subclass of %s" %
                            (fullClassName, parentClass))
    
    # Return a reference to the class itself, not an instantiated object.
    return aClass

    


def main():
    pass
        


if __name__=="__main__":
    pass
    #main()
