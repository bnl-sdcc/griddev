# 
# Bare bones Vihuela plugin to test functionality. 
# Only logs
#
#
#
import os, stat, sys, logging, threading, signal, time, sets
from vihuela.core import Plugin


class DummyPlugin(Plugin):
    
    def __init__(self, config,section ):
        super(DummyPlugin, self).__init__( config, section)
        self.klassname="vihuela.plugins.DummyPlugin"
        self.log.debug('vihuela.plugins.DummyPlugin: Init...')
        
         
    def run_action(self):
        try:
            self.log.info("vihuela.plugins.DummyPlugin: Running Action...")
        except:
            self.log.warn("vihuela.plugins.DummyPlugin: Exception thrown...")
    