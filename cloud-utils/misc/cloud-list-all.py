#!/bin/env  python
#
# Prints correlated sir-XXXXXXXXXX, i-YYYYYYYYYY, and Condor information.  
# Uses ec2-tools and condor_status 
#
#
#
#

import subprocess


EC2PROV={ 'platform' : 'ec2',
          'rcfile' : '~/ec2-caballero/ec2rc',
	  'apihostname' : 'ec2.amazonaws.com',
}

NOVAPROV={ 'platform' : 'nova',
          'rcfile' : '~/nova-essex/novarc',
          'apihostname' : 'gridreserve30.usatlas.bnl.gov',
}


PROVIDERS = [ EC2PROV, NOVAPROV ]

class CloudProvider(object):
    '''
	platform = [ec2, nova-essex, deltacloud]
	rcfile = ~/ec2-caballer/ec2rc
	apihostname = [ec2.amazonaws.com, gridreserve30.usatlas.bnl.gov]

    '''
    def __init__(self, platform, rcfile, apihost):
	self.platform = platform
	self.rcfile = rcfile
	self.apihost = apihost

    def __str__(self):
        s = "%s\t%s\t%s" % (self.platform, self.rcfile, self.apihost)
        return s

    def __repr__(self):
        s = "%s\t%s\t%s" % (self.platform, self.rcfile, self.apihost)
        return s



class CloudHost(object):
    def __init__(self, instanceid, imageid, hostname , ihostname, status, itype ):
        self.instanceid = instanceid
        self.imageid = imageid
        self.hostname = hostname          # external dns hostname, if applicable
        self.ihostname = ihostname        # internal dns hostname, if applicable
        self.status = status
	    # Information that may come from Nova
        self.ipaddr = None                # reachable ip address, possibly only from controller
        self.hostsysname = None
	    # Information that may come from Condor
        self.condorstate = None
        self.condoract = None
        self.arch = None
        self.acttime = None

    def __str__(self):
        s = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.instanceid, self.imageid, self.hostname, self.ihostname, self.imageid, self.condorstate, self.condoract, self.acttime)
        return s

    def __repr__(self):
        s = self.__str__(self)
        return s



def getnovalist(hostname):
    hostlist = []
    querycmd='ssh gridreserve30.usatlas.bnl.gov ". nova-essex/novarc ; nova list"'
    # querycmd="nova list" 
    p = subprocess.Popen(querycmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = None
    (out, err) = p.communicate()
    lines = out.split("\n")
    lines = lines[3:-2]
    for line in lines:
        #print ("line: %s" % line)
        fields = line.split()
        id=fields[1]
        name= fields[4]
        status = fields[6]
        netstr = fields[8]
        #print ("id: %s name: %s status: %s netstr: %s" % (id, name, status, netstr))
        ip=netstr.split("=")[1]
        #print ("id: %s name: %s status: %s ip: %s" % (id, name, status, ip))
        ch = CloudHost(id, name,status,ip)
        hostlist.append(ch)        
    return hostlist


def addinstanceinfo(hostlist):
    '''
        Add in instance info indexed by (host)name.
        INSTANCE  i-00000025 ami-00000004 server-37 server-37 running None (c8d55513d64243fa8e0b29384f6f0c81, ct44.usatlas.bnl.gov) 0  m1.small 2012-06-27T13:54:55.000Z nova
    '''
    #querycmd="euca-describe-instances" 
    querycmd="euca-describe-instances --config nova-essex/novarc" 
    p = subprocess.Popen(querycmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = None
    (out, err) = p.communicate()
    lines = out.split("\n")
    for line in lines:
        #print(line)
        fields = line.split()
        try:
            if fields[0] == "INSTANCE":
                instanceid=fields[1]
                imageid= fields[2]
                name = fields[3]
                state = fields[5]
                idx = fields[9]
                flavor = fields[10]
                startdate = fields[11]
                provider = fields[12]
                
                try:
                    ch = hostlist[name]
                    ch.instanceid = instanceid
                    ch.imageid=imageid
                    ch.state=state
                    ch.idx = idx
                    ch.flavor = flavor
                    ch.startdate = startdate
                    ch.provider = provider
                except:
                    pass
                #print("instid: %s imageid: %s name: %s state: %s idx: %s" % (instanceid,imageid, name, state, idx))
        except:
            pass
    
def addcondorinfo(hostlist):
    '''
    condor_status -pool gridtest03.racf.bnl.gov:29660

condor_status -format "%s\t" Name -format "%s\t" OpSys -format "%s\t" Arch -format "%s\t" State -format "%s\t" Activity -format "%s\t" 'strcat(LastHeardFrom - EnteredCurrentActivity)' -format "%s\n"  'interval(LastHeardFrom - EnteredCurrentActivity)'

condor_status -format "%s " Name -format "%s " OpSys -format "%s " Arch -format "%s " State -format "%s " Activity -format "%s\n"  'interval(LastHeardFrom - EnteredCurrentActivity)'
condor_status -format "%s " Name -format "%s " OpSys -format "%s " Arch -format "%s " State -format "%s " Activity -format "%s " 'strcat(LastHeardFrom - EnteredCurrentActivity)' -format "%s\n"  'interval(LastHeardFrom - EnteredCurrentActivity)'

    '''
    querycmd="condor_status -pool gridtest03.racf.bnl.gov:29660" 
    p = subprocess.Popen(querycmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = None
    (out, err) = p.communicate()
    lines = out.split("\n")
    for line in lines:
        if line[:6] == "server":
            #print(line)
            fields = line.split()
            fullname = fields[0]
            name = fullname.split(".")[0]
            opsys = fields[1]
            arch = fields[2]
            state = fields[3]
            act = fields[4]
            load = fields[5]
            mem = fields[6]
            acttime = fields[7]
            try:
                ch = hostlist[name]
                ch.condorstate = state
                ch.condoract = act
                ch.arch = arch
                ch.acttime = acttime
            except:
                pass
 

def main():

    plist = []
    for prov in PROVIDERS:
        po = CloudProvider(prov['platform'], prov['rcfile'], prov['apihostname'])
        plist.append(po)
    for p in plist:
        print(p) 


    
#

#    hlist=getnovalist()
#    hdict = {}
#    for h in hlist:
#        hdict[h.name]=h
#    addinstanceinfo(hdict)
    #for h in hlist:
        #print(h)
#    addcondorinfo(hdict)
#    for h in hlist:
#        print(h)
    


if __name__ == "__main__":
    main()



