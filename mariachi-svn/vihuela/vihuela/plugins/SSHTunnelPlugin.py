# 
# Vihuela plugin that establishes, monitors and maintains a SSH tunnel from viheula host 
# to a remote host. This will allow remote logins to a vihuela system even if it is behind 
# a firewall or NAT. 
#
#
# 1) Copy your id_rsa and id_rsa.pub
#
# 2) As mariachi, edit /home/mariachi/.ssh/config and add the following lines
#
# Host mariachi-with-tunnel
#    Hostname www-mariachi.physics.sunysb.edu
#    RemoteForward 22221 localhost:22
#    User    daq
#
# 3) Execute:
#
#  ssh -f remote-with-tunnel "ping -i 15 127.0.0.1"
#
# 4) Execute:
#  ping -i 15 127.0.0.1
# and leave it running. 
#
#
import os, stat, sys, logging, threading, signal, time, sets,urllib
import commands
from vihuela.core import Plugin

class SSHTunnelPlugin(Plugin):
    
    def __init__(self, config,section ):
        super(SystemUpdatePlugin, self).__init__( config, section)
        self.klassname="vihuela.plugins.SSHTunnelPlugin"
        self.user=config.get(section,'user')
        self.certfile = config.get(section,'sshpubkey')
        self.keyfile = config.get(section,'sshprivkey')
        self.remote_host = config.get(section, 'remotehost')
        self.remote_port = config.get(section, 'remoteport')
        self.log.debug('vihuela.plugins.SSHTunnelPlugin.__init__: Done..')
        
         
    def run_action(self):
        try:
            self.log.debug('vihuela.plugins.SSHTunnelPlugin.run_action(): Checking for tunnel...')
            if not self.tunnel_running():
                self.log.debug('vihuela.plugins.SSHTunnelPlugin.run_action(): Establishing tunnel...')
                self.setup_tunnel()
        except:
            self.log.warn('vihuela.plugins.SSHTunnelPlugin.run_action(): Caught exception.')
                
        
    def tunnel_running(self):
        self.log.info("vihuela.plugins.SSHTunnelPlugin: Check status...")
       
        #(status, output)=   
        
    def setup_tunnel(self):
        self.log.info("vihuela.plugins.SSHTunnelPlugin: Check status...")
        
        