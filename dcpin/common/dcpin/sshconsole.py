#!/usr/bin/env python
'''
 sshconsole.py
 A pexpect-based interface to the dCache SSH admin console. 

 John Hover <jhover@bnl.gov>
 
'''
import pexpect, getpass, sys, logging
### remove this after RPM install to system paths...
sys.path.append('/home/jhover/devel/dcpin/common')
from dcpin.core import *


def _remove_empty(list, alsoremove):
    '''
      takes a list of strings. strips each element, removes empty lines and
      any lines that contain the alsoremove string.
    '''
    logging.debug('sshconsole._remove_empty(): Begin')
    answerlist = []
    answer = None
    for i in range(0, len(list)):
        line = list[i]
        line = line.strip()
        logging.debug('sshconsole._remove_empty(): examining line "%s"' % line)
        if not ( line == "" ) and (alsoremove not in line):
             logging.debug('sshconsole._remove_empty(): line is non-empty and has no "%s"' % alsoremove)
             answerlist.append(line)
    if len(answerlist) == 0:
        answer = None
    else:
        answer = answerlist
    logging.debug('sshconsole._remove_empty(): Done. Returning.')
    return answer

def _parse_pexpect_before(rawoutput):
    '''
    Takes standard pexpect client.before output and returns a Python list
    of answer lines, not including command issued, blank lines, 
    or trailing prompt, or "None" 
     '''
    logging.debug('sshconsole._parse_pexepect_before(): %d chars of output' % len(rawoutput) )
    linelist = rawoutput.splitlines()
    for i in range( 0, len(linelist)):
        logging.debug('sshconsole._parse_pexepect_before(): line %d is "%s"' % (i, linelist[i] ))
    # discard first line, since this is the issued command
    answers = _remove_empty(linelist[1:], "admin >")
    if len(answers) == 0:
        logging.debug('sshconsole._parse_pexepect_before(): No answer lines.')
        return None
    else:
        logging.debug('sshconsole._parse_pexepect_before(): No answer lines.')
        return answers

def _parse_rep_map(mapstring):
    '''
    Takes a "rep ls" map string, e.g. <-P---------(0)[0]> and 
    returns a properly filled out hash. 
    '''
    # Attribute meanings...
    # <CPCS----XE-(0)[0]> 69469 si={myStore:STRING}
    #  0123456789a
    # 0 = "cached" (<C---)
    # 1 = "precious" (<-P---)
    # 2 = "fclient" (<--C-)
    # 3 = "fstore" (<---S)
    # 4 = ?
    # 5 = ?
    # 6 = ?
    # 7 = ?
    # 8 = X "sticky" rep set sticky on
    # 9 = E "bad" rep set bad on
    # a = ?
    # (<num>) = locktime in milliseconds 
    # [<num>] =
    logging.debug('sshconsole._parse_rep_map(): Begin...')
    ms = mapstring[1:12]
    logging.debug("_parse_rep_map(): small map is %s" % ms)
    mh = {}
    #
    # Construct hash of index names to be used as keys
    #
    atthash = { 0 : 'cached',
                1 : 'precious',
                2 : 'fclient',
                3 : 'fstore', 
                4 : 'four',
                5 : 'five',
                6 : 'six',
                7 : 'seven',
                8 : 'sticky',
                9 : 'bad',
                10 : 'ten',
    }
    # 
    # Fill in main hash for map
    #
    for i in range(0,11):
        if ms[i] != '-':
            mh[atthash[i]] = 1
        else:
            mh[atthash[i]] = 0
    logging.debug('sshconsole._parse_rep_map(): Finished. Returning.')
    return mh


   

class DcSSHConsole(object):
    """
    Handles all communication with the dCache SSH Admin Console.
    """
        
    def __init__(self, config):
        """
        Creates new console object with no active session.
        """
        logging.debug("Begin sshconsole.DcSSHConsole.__init__()")
        self.cfg = config
        self.host = self.cfg.get('sshconsole','host')
        self.port = self.cfg.get('sshconsole','port')
        self.cipher = self.cfg.get('sshconsole','cipher')
        self.acct = self.cfg.get('sshconsole','account')
        self.password = self.cfg.get('sshconsole','password')
        self.prompt = "%s >" % self.acct
        self.connection = None
        logging.debug("End sshconsole.DcSSHConsole.__init__()")
    
    #
    # Utility methods
    #


    def _connect(self):
        ''' 
        Establishes a active session on the console.
        '''        
        logging.debug("DcSSHConsole._connect(): Connecting...")
        connectstr='ssh -p %s -c %s %s@%s' % (self.port, self.cipher, self.acct, self.host)
        logging.debug("DcSSHConsole._connect(): " + connectstr)
        self.connection = pexpect.spawn(connectstr)
        self.connection.expect('password:')
        logging.debug("DcSSHConsole._connect(): Sending password...")
        self.connection.sendline(self.password)
        index = self.connection.expect([ self.prompt, 'Permission denied'] )
        if index == 0:
            logging.debug("DcSSHConsole._connect(): Connected.")
            return 1
        elif index == 1:
            self.connection.close()
            self.connection=  None
            logging.error("DcSSHConsole._connect(): Permission denied -- bad password.")
            raise Exception("DcSSHConsole._connect(): Permission denied -- bad password.")

    def _close(self):
        logging.debug("DcSSHConsole._close(): Closing session...")
        cn= self.connection
        cn.sendline('..')
        cn.expect(self.prompt)
        cn.sendline('logoff')
        cn.expect('closed.')
        logging.debug("DcSSHConsole._close(): SSH session closed.")
        cn.close()
        logging.debug("DcSSHConsole._close(): Pexpect session closed.")

    def _getPnfsId(self, filepath):
        '''
        Retrieves the pnfsid of a single file
        '''
        logging.debug('DcSSHConsole._getPnfsId(): Begin...')
        cn= self.connection
        cn.sendline('cd PnfsManager')
        logging.debug('DcSSHConsole._getPnfsId(): trying tricky regex')
        cn.expect('\(PnfsManager\)')
        logging.debug('DcSSHConsole._getPnfsId(): tricky regex worked!')
        logging.debug('DcSSHConsole._getPnfsId(): before is "%s"' % cn.before)
        logging.debug('DcSSHConsole._getPnfsId(): after is "%s"' % cn.after)
        logging.debug('DcSSHConsole._getPnfsId(): requesting pnfsidof %s' % filepath)
        cn.sendline('pnfsidof %s' % filepath )
        i = cn.expect(['\(PnfsManager\)' , 'java.lang.NullPointerException : null' ])
        logging.debug('DcSSHConsole._getPnfsId(): before is "%s"' % cn.before)
        logging.debug('DcSSHConsole._getPnfsId(): after is "%s"' % cn.after)
        if i == 0:
            logging.debug('DcSSHConsole._getPnfsId(): Got answer.')
            answers = _parse_pexpect_before(cn.before)
            if answers:
                answer = answers[0]
        elif i == 1:
            logging.debug('DcSSHConsole._getPnfsId(): Got NullPointerException.')
            logging.debug('no file at that path: %s' % filepath)
            answer = None
        logging.debug('DcSSHConsole._getPnfsId(): Resetting console to root...')
        cn.sendline('..')
        cn.expect('\(local\)')
        logging.debug('DcSSHConsole._getPnfsId(): Done. Returning.')
        return answer

  
    def _getCacheInfo(self, pnfsid):
        '''
        What pool nodes does a copy of file reside in?
        Returns list of node names, or None
        '''
        #
        # May be empty! i.e. the file may not be in the cache (e.g. on tape)
        #
        answer = None
        logging.debug('DcSSHConsole._getCacheInfo(): Begin...')
        cn= self.connection
        cn.sendline('cd PnfsManager')
        cn.expect('\(PnfsManager\)')
        cn.sendline('cacheinfoof %s' % pnfsid )
        cn.expect('\(PnfsManager\)')
        logging.debug('DcSSHConsole._getCacheInfo(): Got prompt. OK.')
        lines = _parse_pexpect_before(cn.before)
        logging.debug('DcSSHConsole._getCacheInfo(): pool(s) = %s.' % answer)
        if lines:
            answer = []
            for line in lines:
                nodelist = line.split()
            for node in nodelist:
                answer.append(node)
        logging.debug('DcSSHConsole._getCacheInfo(): Resetting console to root...')
        cn.sendline('..')
        cn.expect('\(local\)')
        logging.debug('DcSSHConsole._getCacheInfo(): Done. Returning.')
        return answer


    def _getAttributes(self, pnfsid, poolnode):
        '''
        Get all attributes for a particular file in a pool
        '''
        logging.debug('DcSSHConsole._getAttributes(): Begin...')
        cn= self.connection
        cn.sendline('cd %s' % poolnode)
        cn.expect('\(%s\)' % poolnode )
        cn.sendline('rep ls %s' % pnfsid)
        cn.expect('\(%s\)' % poolnode )
        logging.debug('DcSSHConsole._getAttributes(): Got prompt. OK.')
        atts = _parse_pexpect_before(cn.before)
        logging.debug('DcSSHConsole._getAttributes(): attributes: %s' % atts )
        logging.debug('DcSSHConsole._getAttributes(): Resetting console to root...')
        cn.sendline('..')
        cn.expect('\(local\)')
        logging.debug('DcSSHConsole._getAttributes(): Done. Returning.')
        return atts

    def _pinFileReplica(self, pnfsid, poolnode):
        logging.debug('DcSSHConsole._pinFileReplica( "%s" , "%s" )' % (pnfsid, poolnode) )
        cn= self.connection
        cn.sendline('cd %s' % poolnode)
        cn.expect('\(%s\)' % poolnode )
        cn.sendline('set sticky allowed')
        cn.expect('\(%s\)' % poolnode )
        cn.sendline('rep set sticky %s on' % pnfsid)
        cn.expect('\(%s\)' % poolnode )
        logging.debug('DcSSHConsole._pinFileReplica: Got prompt. OK.')
        logging.debug('DcSSHConsole._pinFileReplica: Resetting console to root...')
        cn.sendline('..')
        cn.expect('\(local\)')
        logging.debug('DcSSHConsole._pinFileReplica: Done. Returning.')
        
    
    def _unPinFileReplica(self, pnfsid, poolnode):
        logging.debug('DcSSHConsole._unPinFileReplica( "%s" , "%s" )' % (pnfsid, poolnode) )
        cn= self.connection
        cn.sendline('cd %s' % poolnode)
        cn.expect('\(%s\)' % poolnode )
        cn.sendline('rep set sticky %s off' % pnfsid)
        cn.expect('\(%s\)' % poolnode )
        logging.debug('DcSSHConsole._unPinFileReplica: Got prompt. OK.')
        logging.debug('DcSSHConsole._unPinFileReplica: Resetting console to root...')
        cn.sendline('..')
        cn.expect('\(local\)')
        logging.debug('DcSSHConsole._unPinFileReplica: Done. Returning.')



    #
    # Our external interface methods
    #
    #

    def getFileInfo(self, filepaths):
        '''
        Retrieves fileInfo objects for each file path in list given as arg that 
        exists. 
        
        '''
        logging.debug("DcSSHConsole.getFileInfo()")
        if not self.connection:
            self._connect()
        answer= []
        
        for filepath in filepaths:
            dcf = None
            logging.debug("DcSSHConsole.getFileInfo(): Getting pnfsid...")
            pnid = self._getPnfsId(filepath)
            if pnid:
                logging.debug("DcSSHConsole.getFileInfo(): id is %s " % pnid )
                pools = self._getCacheInfo(pnid)
                logging.debug("DcSSHConsole.getFileInfo(): pool(s): %s " % pools )
                dcf = DcFileInfo(filepath, pnid , 'auser','agroup' , pools )
                if pools:
                    for node in pools:
                        atts = self._getAttributes(pnid, node)
                        logging.debug("DcSSHConsole.getFileInfo(): attributes(s): %s " % atts)
                        attstr = atts[0]
                        splitlist = attstr.split()
                        logging.debug("DcSSHConsole.getFileInfo(): split is: %s" % splitlist )
                        (p,map,size,storgrp) = tuple(splitlist)
                        atthash = _parse_rep_map(map)
                        atthash['sizeinbytes'] = size
                        atthash['storagegroup']= storgrp
                        # Add attribute hash to hash for this nodename 
                        dcf.attributes[node] = atthash
                        logging.debug("DcSSHConsole.getFileInfo(): p=%s map=%s size=%s storgrp= %s" %( p,map,size,storgrp ) )
                        
                logging.debug("DcSSHConsole.getFileInfo(): File object created.")
            answer.append(dcf)
        return answer

    def pinFile(self,filepaths):
        logging.debug("DcSSHConsole.pinFile(): Begin")
        dcfs = self.getFileInfo(filepaths)
        for dcf in dcfs:
            if dcf:
                for node in dcf.pools:
                    self._pinFileReplica(dcf.id, node)
        logging.debug("DcSSHConsole.pinFile(): End.")
        answer = DcMessage(DcMessage.SUCCESS, "Pinned %s" % filepaths)
        return answer
        
                
    def unPin(self,filepaths):
        logging.debug("DcSSHConsole.unPin(): Begin.")
        dcfs = self.getFileInfo(filepaths)
        for dcf in dcfs:
            if dcf:
                for node in dcf.pools:
                    self._unPinFileReplica(dcf.id, node) 
        logging.debug("DcSSHConsole.unPin(): End.")
        answer = DcMessage(DcMessage.SUCCESS, "Unpinned %s" % filepaths)
        return answer

    def closeConnection(self):
        logging.debug("closeConnection")
        if self.connection:
            self._close()
            self.connection = None
        answer = DcMessage(DcMessage.SUCCESS, "Closed Connection.")
        return answer

if __name__ == '__main__':
    '''
    Test script
    '''
    print "SSH Test"
    pw = getpass.getpass()    
    client = pexpect.spawn('ssh -p 22223 -c blowfish admin@dctest02.usatlas.bnl.gov')
    print "Connecting..."
    client.expect('password:')
    print "Sending password..."
    client.sendline(pw)
    index = client.expect([ PROMPT, 'Permission denied'] )
    if index == 0:
        print "Found prompt"
        #client.interact()
        client.sendline('help')
        print "Requesting help..."
        client.expect("admin >")
        print client.before
        client.sendline('logoff')
    elif index == 1:
        print "Permission denied -- bad password."
        sys.exit()