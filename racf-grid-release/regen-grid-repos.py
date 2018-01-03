#!/bin/env python
# 
# Regenerates repos relevant to executing distribution and architecture only. 
#
# Assumes hierarchy:
#
#
#     REPOROOT
#            repo1 (e.g. production, testing)
#                 dist1 (e.g. rhel, fedora
#                      ver1 (e.g. 5Client, 6Workstation, 16)  
#                          arch (e.g i386, x86_64)
#
#

import subprocess 
import sys
import logging
import os
import re
import shutil

REPOROOT="/afs/usatlas.bnl.gov/mgmt/repo/grid"
REGENCMD="createrepo -v ./"
ARCHS=['i386','x86_64']
PLATFORMS=['fedora','rhel']
REPOS=['development','testing','production','external']
USAGE="regen-repos.py [ REPONAME ]"
RELEASEMAP={ 'Fedora release 14 (Laughlin)' : ('fedora','14'),
             'Fedora release 16 (Verne)' : ('fedora','16'),
             'Red Hat Enterprise Linux Client release 5.7 (Tikanga)' : ('rhel','5Client'),
             'Red Hat Enterprise Linux Client release 5.8 (Tikanga)' : ('rhel','5Client'),
             'Red Hat Enterprise Linux Client release 5.9 (Tikanga)' : ('rhel','5Client'),
             'Red Hat Enterprise Linux Workstation release 6.2 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.3 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.4 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.5 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.6 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.7 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Workstation release 6.8 (Santiago)' : ('rhel','6Workstation'),
             'Red Hat Enterprise Linux Server release 7.1 (Maipo)' : ('rhel','7Workstation'),
             'Red Hat Enterprise Linux Server release 7.2 (Maipo)' : ('rhel','7Workstation'),            
            }

class RepoManager(object):
    
    def __init__(self, reporoot=REPOROOT, repos=REPOS, archs=ARCHS):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('RepoManager initialized.')
        self.dist = None
        self.distver = None
        self.reporoot = reporoot
        self.repos = repos
        self.archs = archs

    def getdistinfo(self):
        f = open('/etc/redhat-release','r')
        rs = f.readline()
        rs = rs.strip()
        logging.debug("release string: %s" % rs)
        (self.dist, self.distver) = RELEASEMAP[rs] 
        logging.info("Distribution=%s, Version=%s" % (self.dist, self.distver))
    
    def regen(self, rootpath):        
        oldpath = os.getcwd()
        os.chdir(rootpath)
        cmd = REGENCMD
        logging.info("Running regen command: '%s'" % cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)     
        (out, err) = p.communicate()
        print(out)
        print(err)
        if p.returncode == 0:
            logging.info('Regen return OK.')
        os.chdir(oldpath)

    def generatepaths(self):
        allpaths = []
        for repo in self.repos:
            for arch in self.archs:
                repopath = "%s/%s/%s/%s/%s" % ( self.reporoot,
                                           repo,
                                           self.dist,
                                           self.distver,
                                           arch
                                           )
                logging.debug("path: %s" % repopath)
                allpaths.append(repopath)
        return allpaths

def main():
    print(sys.argv)
    #print("targets: %s" % targets)
    try:
        dm = RepoManager()
        dm.getdistinfo()
        pathlist = dm.generatepaths()
        for p in pathlist:
            logging.info("Regenerating at %s" % p)
            dm.regen(p)
    except Exception, e:
        logging.error("ERROR: %s" % str(e) )
    
if __name__=='__main__':
    main()


