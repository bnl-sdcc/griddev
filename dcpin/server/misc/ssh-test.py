#!/bin/env python
#
# Place to try stuff
#
#
#
#
#import paramiko
import pexpect, getpass, sys


if __name__ == '__main__':
#    print "SSH Test"
#    client = paramiko.SSHClient()
#    client.connect(hostname='dctest02.usatlas.bnl.gov', port=22223, 
#                    key_filename='/home/jhover/.ssh/dcache-script-admin-key')

    dcprompt = "admin >"
    
    pw = getpass.getpass()    
    client = pexpect.spawn('ssh -p 22223 -c blowfish admin@dctest02.usatlas.bnl.gov')
    print "Connecting..."
    client.expect('password:')
    print "Sending password..."
    client.sendline(pw)
    index = client.expect([ dcprompt, 'Permission denied'] )
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
        
    