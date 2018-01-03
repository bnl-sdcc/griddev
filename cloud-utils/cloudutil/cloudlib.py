#!/bin/env  python
#
# Prints correlated sir-XXXXXXXXXX, i-YYYYYYYYYY, and Condor information.  
# Uses ec2-tools and condor_status 
#
__author__ = "John Hover"
__copyright__ = "2013 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "alpha"

import subprocess
import logging
import os
from optparse import OptionParser
from ConfigParser import ConfigParser

class CloudUtilCLI(object):
    """class to handle the command line invocation of APF. 
       parse the input options,
       setup everything, and run CloudUtil class
    """
    def __init__(self):
        self.options = None 
        self.args = None
              
  
    def parseopts(self):
        parser = OptionParser(usage='''%prog [OPTIONS]
cloudutil manages cloud-based clusters. 

This program is licenced under the GPL, as set out in LICENSE file.

Author(s): John Hover <jhover@bnl.gov>
''', version="")


        parser.add_option("-d", "--debug", 
                          dest="logLevel", 
                          default=logging.WARNING,
                          action="store_const", 
                          const=logging.DEBUG, 
                          help="Set logging level to DEBUG [default WARNING]")
        parser.add_option("-v", "--info", 
                          dest="logLevel", 
                          default=logging.WARNING,
                          action="store_const", 
                          const=logging.INFO, 
                          help="Set logging level to INFO [default WARNING]")
        parser.add_option("--quiet", dest="logLevel", 
                          default=logging.WARNING,
                          action="store_const", 
                          const=logging.WARNING, 
                          help="Set logging level to WARNING [default]")
        parser.add_option("-c", "--conf", 
                          dest="confFiles", 
                          default="~/etc/cloudutil.conf",
                          action="store", 
                          metavar="FILE1[,FILE2,FILE3]", 
                          help="Load configuration from FILEs (comma separated list)")
        parser.add_option("--log", dest="logfile", 
                          default="stdout", 
                          metavar="LOGFILE", 
                          action="store", 
                          help="Send logging output to LOGFILE or SYSLOG or stdout [default <syslog>]")
        (self.options, self.args) = parser.parse_args()


    def setuplogging(self):
        self.log = logging.getLogger('main')
        if self.options.logfile == "stdout":
            logStream = logging.StreamHandler()
        elif self.options.logfile == 'syslog':
            logStream = logging.handlers.SysLogHandler('/dev/log')
        else:
            lf = self.options.logfile
            logdir = os.path.dirname(lf)
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            logStream = logging.FileHandler(filename=lf)    

        formatter = logging.Formatter('%(asctime)s - %(name)s: %(levelname)s: %(module)s: %(message)s')
        logStream.setFormatter(formatter)
        self.log.addHandler(logStream)
        self.log.setLevel(self.options.logLevel)
        self.log.debug('Logging initialised.')



    def getconfigs(self):
        '''
        Read and parse config file(s)
        
        '''
        self.log.info("Raw config file option: %s" % self.options.confFiles)
        filelist = self.options.confFiles = self.options.confFiles.split(',')
        cflist = []
        for f in filelist:
            nf = os.path.expanduser(f)
            cflist.append(nf)
        self.log.debug("Expanded config files: %s" % cflist)
        self.config = ConfigParser()
        read_configs = self.config.read(cflist)
        if len(read_configs) > 0:
            self.log.info("Main config file(s) read: %s" % cflist)
        else:
            raise NoConfigFileException()
        
        
    def execute(self):
        '''
        
        '''
        self.log.debug("Creating cloudUtil w/ config.")
        self.cu = CloudUtil(self.config)

        #self.cu.printProviders()
           
        self.cu.gatherCloudClusterNodes()
        
        self.cu.printCloudClusterNodes()
   
      


class CloudUtil(object):
    '''
    Top-level manager object handling all operations...
    '''
    def __init__(self, config):
        self.log = logging.getLogger('main')
        
        # Handle configs...        
        self.config = config
        cp = ConfigParser()      
        files = self.config.get('cloudutil', 'cloudsfile')
        filelist = files.split(',')
        self.log.info("Raw cloudsfile config var: %s" % filelist)
        cflist = []
        for f in filelist:
            nf = os.path.expanduser(f)
            cflist.append(nf)
        self.log.debug("Expanded cloudsfile file list: %s" % cflist)
        self.cconfig = ConfigParser()
        read_configs = self.cconfig.read(cflist)
        if len(read_configs) > 0:
            self.log.info("Cloud config file(s) read: %s" % cflist)
        else:
            raise NoConfigFileException()
        
        # Set up providers      
        self.providers = []      
        for s in self.cconfig.sections():
            p = CloudProvider(self.cconfig, s)
            self.providers.append(p)
        self.log.info("Found %d providers." % len(self.providers))
        for p in self.providers:
            self.log.debug("Provider: %s" % p)
        
        # Establish data structures. 
        self.allcondorinfo = []    # local batch slot info list
        self.allcondorbyname = {}   # local batch slots hashed by hostname
        self.allcloudinfo = []      # all cloud instance info list
        self.allcloudbyname = {}    # Cloud instances hashed by internal hostname. 
        self.cloudclusternodes = [] # Aggregated/correlated cloudInstanceInfo list.

        self.log.info("CloudUtil object initialized.")
    
    def printProviders(self):
        for p in self.providers:
            print(p)
      
    def getCloudInstanceInfo(self):
        for p in self.providers:
            self.log.debug("[%s] Gathering Cloud instance info..." % p.section)
            cloudinfolist = p.getCloudInfo()
            for ci in cloudinfolist:
                self.allcloudinfo.append(ci)       
        self.log.debug("Assembled list of %d CloudInfo items." % len(self.allcloudinfo))
        
        self.log.debug("Indexing cloud instances by internal hostname...")
        for node in self.allcloudinfo:
            #self.log.debug("Adding node %s to index..." % node.internalhostname)
            self.allcloudbyname[node.internalhostname] = node
        self.log.debug("Created index of length %d" % len(self.allcloudbyname))


    def gatherCloudClusterNodes(self):
        '''
        Get info from batch system, and all cloud providers, and create CloudClusterNodes
        
        '''
        self.log.debug("Gathering Condor info...")
        self.getCondorInfo()
        self.getCloudInstanceInfo()

        # Handle all instances that are seen in Condor...            
        errlist = []
        for node in self.allcondorinfo:
            ccn = CloudClusterNode()
            ccn.bi = node
            try:
                ccn.ci = self.allcloudbyname[node.machine]
            except Exception, e:
                errlist.append("Unable to find cloud instance for hostname %s" % node.machine)
                ccn.ci = CloudInstanceInfo()
            self.cloudclusternodes.append(ccn)
        if len(errlist) > 0:
            self.log.warning("Unable to find cloud instance for %d hostnames " % len(errlist))

        self.log.info("Found %d Condor slots with corresponding Cloud instance" % len(self.cloudclusternodes))

        
        # Find all instances NOT seen in Condor, but present in Cloud
        errlist = []
        for node in self.allcloudinfo:
            try:
                condorinfo = self.allcondorbyname[node.internalhostname]
                # Do nothing, these have already been handled. 
            except Exception, e:
                # Found a cloud instance with no corresponding Condor slot
                errlist.append("Unable to find condor instance for host %s" % node.internalhostname)
                ccn = CloudClusterNode()
                ccn.ci = node
                self.cloudclusternodes.append(ccn)
        self.log.info("Found %d cloud instances without corresponding Condor slot" % len(errlist))
        self.log.debug("Gathered CloudCluster info on %d total nodes" % len(self.cloudclusternodes))

        
    def printCloudClusterNodes(self):
        for node in self.cloudclusternodes:
            print(node)        



    def getCondorInfo(self):
        '''
          Gather information about Condor slots. Fill self.allcondorinfo 
            condor_status -format "%s " Name
                  -format "%s " Machine 
                  -format "%s " OpSys -format "%s " Arch 
                  -format "%s " State 
                  -format "%s " Activity 
                  -format "%s " 'strcat(currentTime - EnteredCurrentActivity)' 
                  -format "%s\n"  'interval(currentTime - EnteredCurrentActivity)'
        
        
        '''

        qc = '''condor_status -format "%s " Name -format "%s " Machine -format "%s " OpSys -format "%s " Arch -format "%s " State -format "%s " Activity -format "%s " 'strcat(currentTime - EnteredCurrentActivity)' -format "%s\n" 'interval(currentTime - EnteredCurrentActivity)' '''
        p = subprocess.Popen(qc, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = None
        (out, err) = p.communicate()
        lines = out.split("\n")
        self.log.debug("Got %d lines from condor_status" % len(lines))
        for line in lines:
            if not line.strip() == '':    # Ignore blank lines...
                try:
                    fields = line.split()
                    name = fields[0].strip()
                    machine = fields[1].strip()
                    opsys = fields[2].strip()
                    arch = fields[3].strip()
                    state = fields[4].strip()
                    act = fields[5].strip()
                    acttimesec = fields[6].strip()
                    acttime = fields[7].strip()
                    
                    condorinfo = CondorSlotInfo()
                    condorinfo.setInfo(name, machine,opsys,arch,state,act,acttimesec,acttime)
                    self.allcondorinfo.append(condorinfo)
                except Exception:
                    self.log.warn("Problem parsing line: '%s'" % line)
        
        self.log.debug("Created CondorInfo list with %d elements" % len(self.allcondorinfo))
        
        self.log.debug("Indexing condor slots by machine hostname...")
        for node in self.allcondorinfo:
            #self.log.debug("Adding node %s to index..." % node.internalhostname)
            self.allcondorbyname[node.machine] = node
        self.log.debug("Created index of length %d" % len(self.allcondorbyname))
        

def retire(self, provider='all', num='all'):
    '''
    
    '''

def purge(self, provider='all'):
    '''
    
    '''        


class CloudProvider(object):
    '''
    Class to encapsulate all interactions with a particular Cloud provider, e.g. 
    EC2 us-east-1 or Openstack 4.0 at BNL. 

    '''
    def __init__(self, config, section):
        self.log = logging.getLogger('main')
        self.section = section
        self.config = config
        self.rcfile = os.path.expanduser(self.config.get(self.section, 'rcfile'))
        self.client = self.config.get(self.section, 'client')
        self.cloudbyname = {}   # Hash for info indexed by machine hostname
        self.cloudinfolist = [] # List for cloudinfo objects. 
               




    def getCloudInfo(self):
        '''
          Get information about all Cloud instances. 
          
          ec2-describe-instances
          
          --> 2 lines
          
RESERVATION     r-e753839c      
                415974413739    
                atlas-wn-1

INSTANCE        i-bf2615ce      
                ami-0bb33862    
                ec2-107-20-59-188.compute-1.amazonaws.com       
                ip-10-226-94-242.ec2.internal   
                running         
                0               
                m1.small        
                2013-01-18T16:49:47+0000        
                us-east-1b      
                aki-427d952b                    
                monitoring-disabled     
                107.20.59.188   
                10.226.94.242                   
                instance-store  
                spot    
                sir-b8499a11                    
                paravirtual     
                xen     
                2b924763-ab1a-476d-8473-330aa7b0937e    
                sg-c46b4fac     
                default 
                false
        '''
        cil= []
        qc = '. %s ; %s-describe-instances ' % ( self.rcfile, self.client)
        self.log.debug("Executing command %s" % qc)
        
        p = subprocess.Popen(qc, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = None
        (out, err) = p.communicate()
        lines = out.split("\n")
        self.log.debug("Got %d lines from %s-describe-instances" % (len(lines), self.client))
        self.cloudinfolist = []
        for line in lines:
            if not line.strip() == '':    # Ignore blank lines...
                try:
                    cloudinfo = CloudInstanceInfo()
                    fields = line.split()
                    linetype = fields[0].strip()
                    if linetype == 'RESERVATION':
                        pass
                    elif linetype == 'INSTANCE':
                        cloudinfo.instanceid = fields[1].strip()           
                        cloudinfo.imageid = fields[2].strip()
                        cloudinfo.externalhostname = fields[3].strip()
                        cloudinfo.internalhostname = fields[4].strip()
                        cloudinfo.state = fields[5].strip()
                        cloudinfo.something = fields[6].strip()
                        cloudinfo.instancetype = fields[7].strip()
                        cloudinfo.startdate = fields[8].strip()
                        cloudinfo.zone = fields[9].strip()                    
                        cloudinfo.kernelid = fields[10].strip()
                        cloudinfo.monitorstatus = fields[11].strip()
                        cloudinfo.externalip = fields[12].strip()
                        cloudinfo.internalip = fields[13].strip()
                        cloudinfo.storagetype = fields[14].strip()
                        cloudinfo.reservationtype = fields[15].strip()
                        cloudinfo.reservationid = fields[16].strip()
                        #vmtype
                        #vmflavor
                        #code
                        #securitygroupid
                        self.cloudinfolist.append(cloudinfo)
                except Exception, e:
                    cloudinfo = None
                    self.log.warn("Problem parsing line: '%s' Error: %s" % (line, e))
        
        self.log.debug("Created CloudInstanceInfo list with %d elements" % len(self.cloudinfolist))
        return self.cloudinfolist
       
    def getRequestInfo(self):
        '''
          Gather information about Spot Requests. 
        '''
                

    def __str__(self):
        s = "[%s] rcfile=%s client=%s" % (self.section, self.rcfile, self.client)
        return s

    def __repr__(self):
        s = self.__str__(self)
        return s



class CondorSlotInfo(object):
    '''
    condor_status -format "%s " Name
                  -format "%s " Machine 
                  -format "%s " OpSys -format "%s " Arch -format "%s " State 
                  -format "%s " Activity 
                  -format "%s " 'strcat(currentTime - EnteredCurrentActivity)' 
                  -format "%s\n"  'interval(currentTime - EnteredCurrentActivity)'
    
    '''
    def __init__(self):
        self.name = None            # slotX@hostname
        self.machine = None         # just hostname
        self.opsys = None
        self.arch = None
        self.state = None
        self.activity = None
        self.durationsecs = None
        self.durationpretty = None
    
    
    def setInfo(self, name,machine,opsys,arch,state,activity,durationsecs,durationpretty):
        self.name = name
        self.machine = machine
        self.opsys = opsys
        self.arch = arch
        self.state = state
        self.activity = activity
        self.durationsecs = int(durationsecs)
        self.durationpretty = durationpretty


    def __str__(self):
        s = "%s\t%s\t%s\t%s\t%s\t%s\t%d\t%s" % (self.name,
                                                  self.machine,
                                                  self.opsys,
                                                  self.arch,
                                                  self.state,
                                                  self.activity,
                                                  self.durationsecs,
                                                  self.durationpretty)
        return s

        
    def __repr__(self):
        s = self.__str__(self)
        return s



class CloudRequestInfo(object):
    def __init__(self):
        self.sir = None
    

class CloudInstanceInfo(object):
    def __init__(self):
        self.instanceid = None
        self.imageid = None
        self.externalhostname = None     # external dns hostname, if applicable
        self.internalhostname = None     # internal dns hostname, if applicable
        self.state = None                # running|terminated  
        self.something = None            # 0 ??
        self.instancetype = None         # m1.small | m1.medium
        self.startdate = None             # human readable start time
        self.zone = None                 # availability zone
        self.kernelid = None
        self.monitorstatus = None
        self.externalip = None
        self.internalip = None
        self.storagetype = None
        self.reservationtype = None
        self.reservationid = None


    def __str__(self):
        s = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.instanceid, 
                                                self.imageid, 
                                                self.externalhostname, 
                                                self.internalhostname, 
                                                self.state, 
                                                self.something,
                                                self.instancetype,
                                                self.startdate,
                                                self.zone,
                                                self.kernelid,
                                                self.monitorstatus,
                                                self.externalip, 
                                                self.internalip,
                                                self.storagetype,
                                                self.reservationtype,
                                                self.reservationid,                                                
                                                )
        return s

    def __repr__(self):
        s = self.__str__(self)
        return s


class CloudClusterNode(object):
    '''
        Composite object representing a request + instance + batch slot. 
    '''
    def __init__(self):
        # Initially empty
        self.bi = CondorSlotInfo()
        self.ci = CloudInstanceInfo()
        
    def __str__(self):        
        s = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.bi.machine,
                                  self.bi.state,
                                  self.bi.activity,
                                  self.bi.durationpretty,
                                  self.ci.instanceid,
                                  self.ci.reservationtype, 
                                  self.ci.reservationid, 
                                  self.ci.imageid,
                                  self.ci.state,
                                  self.ci.instancetype,
                                  self.ci.externalhostname,  
                                  self.ci.zone
                                  )
        return s


    def __repr__(self):
        s = self.__str__(self)
        return s


class NoConfigFileException(Exception):
    '''
     When bad config files are passed in. 
    '''





    

 



