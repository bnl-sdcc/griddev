'''
  server.py
  dcpin system server code. 


 John Hover <jhover@bnl.gov>
 
 
'''

import Pyro.core
import sys, logging
from dcpin.core import *
from dcpin.sshconsole import DcSSHConsole

# There should only ever be one of this. Perhaps we should turn it into a factory?
#

class DCPinServer(Pyro.core.ObjBase):

    
    # These are the commands that are part of our generic pinning interface. These should have
    # some form of mapping to both the SSH Admin Console and SRMv2
    ourcommands=['getFileInfo','closeConnection' ]
    
    def __init__(self, config):
        logging.debug("DCPinServer.__init__()..." )
        Pyro.core.ObjBase.__init__(self)
        self.name = 'dcpinServerInstance'
        self.cfg = config
        if (self.cfg.get('server','dcinterface') == 'sshconsole'):
            logging.info("Server will use SSH Admin console interface...")
            self.dcinterface=DcSSHConsole(self.cfg)
        elif (self.cfg.get('server','dcinterface') == 'srmv2'):
            pass  # not implemented
        logging.debug("End DCPinServer.__init__()..." )    
    
    def shutDown(self):
        logging.debug("DCPinServer.shutdown(): Begin")
        self.dcinterface.closeConnection()
        logging.debug("DCPinServer.shutdown(): End")
        
    def doCommand(self, command ):
        '''
        doCommand(<string>)
        perform a command recieved from a client
        
        '''
        logging.debug("DCPinServer.doCommand(): Recieved command '%s'" % command.strip())
        cmdlist = command.split()
        basecmd = cmdlist[0]
        answer = DcMessage(DcMessage.ERROR, "Command not implemented: %s" % basecmd)
        try:
            if basecmd == 'getFileInfo':
                logging.debug("DCPinServer.doCommand(): Calling getFileInfo()")
                infolist = self.dcinterface.getFileInfo(cmdlist[1:])
                logging.debug("DCPinServer.doCommand(): Got fileinfo object. Converting to string.")
                text = ""
                for dcf in infolist:
                    text += str(dcf)
                answer = DcMessage(DcMessage.SUCCESS, text )
            
            elif basecmd == 'closeConnection':
                logging.debug("DCPinServer.doCommand(): Calling closeConnection()")
                answer = self.dcinterface.closeConnection()
                
            elif basecmd == 'pinFile':
                logging.debug("DCPinServer.doCommand(): Calling pinFile()")
                answer = self.dcinterface.pinFile(cmdlist[1:])
                
            elif basecmd == 'unPin':
                logging.debug("DCPinServer.doCommand(): Calling unPin()")
                answer = self.dcinterface.unPin(cmdlist[1:])
            
            elif basecmd == 'help':
                logging.debug("DCPinServer.doCommand(): Calling help()")
            
            else:
                pass
                
            
        except Exception:
            answer = DcMessage(DcMessage.ERROR, "Got exception:  %s " % sys.exc_type )
        
        logging.debug("DCPinServer.doCommand(): Finished command '%s' Returning." % basecmd)
        return answer
    
     
    
        
