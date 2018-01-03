#!/bin/env python
#
#
#

import threading
import logging
import time
import sys
import random

class MyThreadException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) # init the thread
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        self.log = logging.getLogger()
        self.threads = []
        for i in range(0,10):
            st = SubThread()
            self.threads.append(st)
        self.log.info("Created subthreads...")
        # Handle objects
        self.stopevent = threading.Event()
        self.log.info("Main thread initialized.")
        
    def run(self):
        for t in self.threads:
            t.start()
        while not self.stopevent.isSet():
            self.log.info("In MainThread.run(). Sleeping...")
            time.sleep(.2)

    def join(self,timeout=None):
        '''
        Stop the thread. Overriding this method required to handle Ctrl-C from console.
        '''
        self.stopevent.set()
        self.log.info('Stopping thread...')
        threading.Thread.join(self, timeout)
    
    def shutdown(self):
        for t in self.threads:
            t.join()
        self.log.info("All children joined.")



class SubThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) # init the thread
        self.log = logging.getLogger()
        # Handle objects
        self.stopevent = threading.Event()
        self.log.info("SubThread initialized.")

    def run(self):
        while not self.stopevent.isSet():
            try:  
                self.log.info("In [%s] Subthread.run(). Sleeping..." % self.name)
                num = random.randint(0,1000)
                if num <50:
                    raise MyThreadException("This is an exception from thread %s" % self.name)
                time.sleep(.2)
            except Exception, e:
                self.log.info("Caught exception in thread %s ERROR: %s" %(self.name,str(e) ))
            

    def join(self,timeout=None):
        '''
        Stop the thread. Overriding this method required to handle Ctrl-C from console.
        '''
        self.stopevent.set()
        self.log.info('Stopping thread...')
        threading.Thread.join(self, timeout)

   
def main():
    mt = MainThread()
    mt.start()
    try:
        while True:
            logging.info("main.py -- Running...")
            time.sleep(2)
    except (KeyboardInterrupt): 
                logging.info("Shutdown via Ctrl-C or -INT signal.")
                logging.info("Shutting down all threads...")
                mt.shutdown()
                mt.join()
                logging.info("All Handler threads joined. Exitting.")    
                sys.exit(0)
    
    
main()
    
    
    

