# 
# Bare bones Vihuela plugin to test functionality. 
# Only logs
#
#
#
import os, stat, sys, logging, threading, signal, time, sets,urllib
import commands
from vihuela.core import Plugin

VIHUELA_TMP_SCRIPT='/tmp/vihuela-temp-script'

class SystemUpdatePlugin(Plugin):
    
    def __init__(self, config,section ):
        super(SystemUpdatePlugin, self).__init__( config, section)
        self.klassname="vihuela.plugins.SystemUpdatePlugin"
        self.script_url=config.get(section,'script_url')
        self.certfile = config.get(section,'cert_file')
        self.keyfile = config.get(section,'key_file')
        self.strict= config.get(section,'strict')
        self.log.debug('vihuela.plugins.SystemUpdatePlugin.__init__: Done..')
        
         
    def run_action(self):
        self.log.info("vihuela.plugins.SystemUpdatePlugin: Running Action...")
        opener= urllib.URLopener(key_file = self.keyfile, cert_file= self.certfile )
        url = self.script_url
        response = opener.open(url, data=None)
        self.log.debug('vihuela.plugins.SystemUpdatePlugin.run_action): Getting URL.')
        script_txt =  response.read()
        self.log.debug('vihuela.plugins.SystemUpdatePlugin.run_action): Script:\n%s' % script_txt)
        f = open( VIHUELA_TMP_SCRIPT,'w')
        f.write(script_txt)
        f.close()
        os.chmod(VIHUELA_TMP_SCRIPT, 700)
        (status, output) = commands.getstatusoutput(VIHUELA_TMP_SCRIPT)
        if status == 0:
            self.log.debug('vihuela.plugins.SystemUpdatePlugin.run_action): Script output:\n%s' % output)
        else:
            self.log.error('vihuela.plugins.SystemUpdatePlugin.run_action): Nonzero exit code. Script output:\n%s' % output)
    
        