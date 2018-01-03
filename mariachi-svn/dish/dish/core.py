# 
# core.py -- Core module for Distributed Interactive Shell
#
# This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 

import os, sys, logging, getpass, time, pexpect
from ConfigParser import ConfigParser



class DishConsole(object):
    """
    Top level class. Handles user console interaction. 
    Handles all hostgroup(s). Individual host connections handled by HostGroup class.
    
    """    
    def __init__(self,config):

        logging.debug("Begin core.DishConsole.__init__()")
        self.cfg = config
        #
        # Process all groups defined in config. Maybe they won't 
        # get used this time, but we want to fail early if there is
        # a typo
        self.hostgroupnames = config.get('global','hostgroups').split(',')
        logging.debug("Hostgroupnames are %s" % self.hostgroupnames)
        self.hostgroups = {}
        for c in self.hostgroupnames:
            self.hostgroups[c]=(HostGroup(config,c))
        #
        # Now establish list of hostgroups to actually do commands on..
        #
        self.grouplist = config.get('args','grouplist',raw=True).split(',')
        logging.debug("End core.DishConsole.__init__()")


    def doCommand(self, line):
        logging.debug("DishConsole.doCommand(): %s" % line ,)
        answers = []
        for group in self.grouplist:
            anslist = self.hostgroups[group].doCommand(line)
            for a in anslist:
                answers.append(a)
        return answers

    def __repr__(self):
        """
        Returns a string representation of this object.
        """
        s = ""
        for group in self.hostgroups:
            s = s + group
        return s



class HostGroup(object):
    """
    Represents a group of nodes.
    """
    def __init__(self,config,section):
        """
        Handles connections to all hosts.
        """
        
        logging.debug("Begin core.HostGroup.__init__()")
        self.cfg = config
        self.section = section
        hostlist = config.get(section,"hosts")
        self.hosts = hostlist.split(',')
        logging.debug("Got hosts: %s" % self.hosts)
        self.connections={}
        for host in self.hosts:
            self.connections[host] = SSHConnection(config, section, host)
        logging.debug("core.HostGroup.__init__(): Created group of %d hosts and connections." % len(self.hosts))        
        logging.debug("End core.HostGroup.__init__()")
    
    def __repr__(self):
        """
        Returns a string representation of this object.
        """
        s = ""
        for host in self.hosts:
            s = s + host + "\n"
        return s
    
    
    def connectAll(self):
        """
        Triggers creation of connection objects for all...
        """
        for host in self.hosts:
            self.connections[host].connect()
        
    
    def doCommand(self,line):
        answers = []
        for host in self.hosts:
            conn = self.connections[host]
            ans = conn.doCommand(line)
            answers.append(ans)
        return answers
               
    

class SSHConnection(object):
    """
    Handles all communication with an SSH session using pexpect.
    """
    
    BAD_HOSTKEY="Host key verification failed."
    FIRST_CONNECT="Are you sure you want to continue connecting (yes/no)?"
    USER_PROMPT="]$"
    ROOT_PROMPT="]#"
        
        
    def __init__(self, config, section, hostname):
        """
        Creates new console object with no active session.
        """
        logging.debug("Begin SSHConnection.__init__()")
        self.config = config
        self.section = section
        self.host = hostname 
        self.user = self.config.get('args' ,'user')
        if self.user == 'root':
            self.prompt=SSHConnection.ROOT_PROMPT
        else:
            self.prompt=SSHConnection.USER_PROMPT
        
        self.password = None
        self.connection = None
        logging.debug("End SSHConnection.__init__()")
    
    def doCommand(self,line):
        
        if self.connection:
           self.connection.sendline(line)
           self.connection.expect(self.prompt)
           answers = self._parse_pexpect_before(self.connection.before) 
           return "[%s]: Success" % self.host

    def connect(self):
        ''' 
        Establishes a active session on the console.
        '''        
        logging.debug("SSHConnection._connect(): Connecting...")
        connectstr='ssh -p %s %s@%s' % (self.port, self.acct, self.host)
        logging.debug("SSHConnection._connect(): " + connectstr)
        self.connection = pexpect.spawn(connectstr)
        self.connection.expect('password:')
        logging.debug("SSHConnection._connect(): Sending password...")
        self.connection.sendline(self.password)
        index = self.connection.expect([ self.prompt, 'Permission denied'] )
        if index == 0:
            logging.debug("SSHConnection._connect(): Connected.")
            return 1
        elif index == 1:
            self.connection.close()
            self.connection=  None
            logging.error("SSHConnection._connect(): Permission denied -- bad password.")
            raise Exception("SSHConnection._connect(): Permission denied -- bad password.")

           
    #
    # Utility methods
    #
    def close(self):
        logging.debug("SSHConnection._close(): Closing session...")
        cn= self.connection
        cn.sendline('..')
        cn.expect(self.prompt)
        cn.sendline('logoff')
        cn.expect('closed.')
        logging.debug("SSHConnection._close(): SSH session closed.")
        cn.close()
        logging.debug("SSHConnection._close(): Pexpect session closed.")
        
    def _remove_empty(list):
        '''
          takes a list of strings. strips each element, removes empty lines and
          any lines that contain the alsoremove string.
        '''
        logging.debug('SSHConnection._remove_empty(): Begin')
        answerlist = []
        answer = None
        for i in range(0, len(list)):
            line = list[i]
            line = line.strip()
            logging.debug('SSHConnection._remove_empty(): examining line "%s"' % line)
            if not ( line == "" ):
                 logging.debug('SSHConnection._remove_empty(): line is non-empty.')
                 answerlist.append(line)
        if len(answerlist) == 0:
            answer = None
        else:
            answer = answerlist
        logging.debug('SSHConnection._remove_empty(): Done. Returning.')
        return answer

    def _parse_pexpect_before(rawoutput):
        '''
        Takes standard pexpect client.before output and returns a Python list
        of answer lines, not including command issued, blank lines, 
        or trailing prompt, or "None" 
         '''
        logging.debug('SSHConnection._parse_pexepect_before(): %d chars of output' % len(rawoutput) )
        linelist = rawoutput.splitlines()
        for i in range( 0, len(linelist)):
            logging.debug('SSHConnection._parse_pexepect_before(): line %d is "%s"' % (i, linelist[i] ))
        # discard first line, since this is the issued command
        answers = _remove_empty(linelist[1:])
        if len(answers) == 0:
            logging.debug('SSHConnection._parse_pexepect_before(): No answer lines.')
            return None
        else:
            logging.debug('SSHConnection._parse_pexepect_before(): No answer lines.')
            return answers

