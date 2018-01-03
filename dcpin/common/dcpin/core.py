'''
  server.py
  dcpin system core code. 


 John Hover <jhover@bnl.gov>
 
'''
import Pyro.core
import sys, logging




class DcMessage(Pyro.core.ObjBase):
    '''
    Represent a request or response between the client and server. 
    '''
    SUCCESS = 1
    FAILURE = 2
    ERROR = 3
    code= { 1 : "SUCCESS" , 2 : "FAILURE" , 3:"ERROR" }
        
    def __init__(self, inittype, initmessage, initpayload=None):
        logging.debug("dcpin.core.DcMessage.__init__(): Begin...")
        Pyro.core.ObjBase.__init__(self)
        self.type = inittype
        self.message = initmessage
        self.data = initpayload

    def __str__(self):
        logging.debug("dcpin.core.DcMessage.__str__(): Converting to string.")
        return "%s: %s " % (self.code[self.type], self.message )




class DcFileInfo(Pyro.core.ObjBase):
    '''
    Represent all information about a particular file/path/pfnsid in dCache.
    '''
    attribute_names = ['cached', 'precious', 'fclient', 'fstore', 'sticky', 'bad']
    def __init__(self, filepath, pnfsid="NApnfsid", fileowner="NAuser", filegroup="NAgroup", poolNodes=None ):
        logging.debug("dcpin.core.DcFile.__init__(): Begin...")
        Pyro.core.ObjBase.__init__(self)
        self.path = filepath     # pnfs path of file, e.g. /pnfs/usatlas.bnl.gov/data/file.txt
        self.id = pnfsid         # pnfs ID of file
        self.owner = fileowner   #
        self.group = filegroup   #
        self.pools = poolNodes   # List of dCache pool nodes on which the file resides. May be empty
        self.attributes = {} # Hash of hashes  of attributes, one for each pool the file is in.
                             # where the key of the sub-hash is 
        logging.debug("dcpin.core.DcFile.__init__(): Done...")
    
        
    def __str__(self):
        logging.debug("dcpin.core.DcFile.__str__(): Converting to string.")
        s =  'file: %s\n' % self.path
        s += '   pnfsid: %s\n' % self.id
        s += '   owner: %s\n' % self.owner
        s += '   group: %s\n' % self.group
        for p in self.pools:
            s += '   pool: %s\n' % p
            mykeys = self.attributes[p].keys()
            mykeys.sort()
            for a in mykeys :
                s +=  '       %s: %s\n' % (a, self.attributes[p][a])
        return s
        
     
