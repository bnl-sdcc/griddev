#!/usr/bin/env python

import sys
import os

from ConfigParser import ConfigParser
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# other useful utilites for logging
def prettyObjectPrint(obj):
    '''
    Creates string representation of arbitrary complex objects. 
    From http://code.activestate.com/recipes/137951/
    '''    
    import types

    # There seem to be a couple of other types; gather templates of them
    MethodWrapperType = type(object().__hash__)
    
    objclass  = None
    objdoc    = None
    objmodule = '<None defined>'
    methods   = []
    builtins  = []
    classes   = []
    attrs     = []
    for slot in dir(obj):
        attr = getattr(obj, slot)
        if   slot == '__class__':
            objclass = attr.__name__
        elif slot == '__doc__':
            objdoc = attr
        elif slot == '__module__':
            objmodule = attr
        elif (isinstance(attr, types.BuiltinMethodType) or 
              isinstance(attr, MethodWrapperType)):
            builtins.append( slot )
        elif (isinstance(attr, types.MethodType) or
              isinstance(attr, types.FunctionType)):
            methods.append( (slot, attr) )
        elif isinstance(attr, types.TypeType):
            classes.append( (slot, attr) )
        else:
            attrs.append( (slot, attr) )
    
    # Organize them
    methods.sort()
    builtins.sort()
    classes.sort()
    attrs.sort()

    s = "[%s]\n" % objclass
    
    if attrs:
        for (attr, val) in attrs:
            if attr[0] != '_':
                s+="  %s = %s\n" %( attr,str(val))
    return s        














print("SQLAlchemy Demo...")

Base = declarative_base()
class CertifyHost(Base):
    __tablename__ = 'hosts'
    hostname = Column('hostname', Text, primary_key=True)
    config = Column('config', Text)
    section = Column('section', Text)
    adminpluginclass = Column('adminpluginclass', Text)
    certpluginclass = Column('certpluginclass', Text)
    iopluginclass = Column('iopluginclass', Text)
    certfile = Column('certfile', Text)
    keyfile = Column('keyfile', Text)
    certhostname = Column('certhostname', Text)
    subjectaltnames = Column('subjectaltnames', Text)
    service = Column('service', Text)
    prefix = Column('prefix', Text)
    svcprefix = Column('svcprefix', Text)
    targetdir = Column('targetdir', Text)
    owneruser = Column('owneruser', Text)
    ownergroup = Column('ownergroup', Text)                
    
    def __init__(self, config, section, host, service ):        
        self.config = config
        self.section = section        
        self.hostname = host
        self.service = service
                   
        self.adminpluginclass='VDTAdminPlugin'
        self.certpluginclass='OpenSSLCertPlugin'
        self.iopluginclass='SSHIoPlugin'
        
        self.certfile='/etc/grid-security/hostcert.pem'
        self.keyfile='/etc/grid-security/hostkey.pem'
        
        self.certhostname=self.hostname
        self.subjectaltnames = 'Email: jhover@bnl.gov'

        
        self.prefix='host'
        self.svcprefix=None
        self.targetdir='/etc/grid-security'
        self.owneruser='root'
        self.ownergroup='root'    

#    def __repr__(self):
#        return "<CertifyHost('%s','%s','%s','%s')>" % (self.config, 
#                                                       self.section, 
#                                                       self.hostname, 
#                                                       self.service)


    def __str__(self):
        return prettyObjectPrint(self)
  

class SQLAlchemyTest(object):    
    
    def __init__(self):
        self.dbfile = os.path.expanduser("~/sqladb.sq3")
        self.engine = create_engine('sqlite:///%s' % self.dbfile)
        
        
    def printVersion(self):
        print("SQLAlchemy version %s" % sqlalchemy.__version__)
    
    def gatherEngines(self):
        print("Database engines available:")
        self.dbeng={'SQLite': 'sqlite3',
               'Postgres': 'psycopg2',
               'MySQL' : 'MySQLdb',
               'Oracle' : 'cx_Oracle',
               }
        self.avail={}
        
        '''
           Driver URL format: driver://username:password@host:port/database
           Drivers: sqlite, mysql, postgres, oracle, mssql, firebird
        
        '''
        
        # PostGres DB Engine
        for (n,m) in self.dbeng.items():
            try:
                __import__(m)
                self.avail[n] = True
                print("%s is available via %s." % (n,m))
            except ImportError:
                self.avail[n] = False
                print("%s not available." % n)
    
    def createSQLiteDB(self):
        if self.avail['SQLite']:
           
            # Create sample database for CertifyHost    
            metadata = MetaData()
            host_table= Table('hosts', metadata,
                            Column('hostname', Text, primary_key=True),
                            Column('config', Text),
                            Column('section', Text),
                            Column('adminpluginclass', Text),
                            Column('certpluginclass', Text),
                            Column('iopluginclass', Text),
                            Column('certfile', Text),
                            Column('keyfile', Text),
                            Column('certhostname', Text),
                            Column('subjectaltnames', Text),
                            Column('service', Text),
                            Column('prefix', Text),
                            Column('svcprefix', Text),
                            Column('targetdir', Text),
                            Column('owneruser', Text),
                            Column('ownergroup', Text),                
            )
            print("Creating CertifyHost table...")
            # Following no longer necessary with DeclarativeBase class usage.
            #mapper(CertifyHost, host_table)
            metadata.create_all(self.engine)
    
    def testSave(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        print("Creating CertifyHost instance...")
        self.session.add_all([
                         CertifyHost('config','section','info.bnl.gov','ldap' ),
                         CertifyHost('config','section','web01.bnl.gov','http' ),
                         CertifyHost('config','section','ldap01.bnl.gov','ldap' ),
                         CertifyHost('config','section','web02.bnl.gov','http' ),]
                        )
        print(self.session.new)
        self.session.commit()
        rows = self.session.query(CertifyHost).all()
        for r in rows:
            print(r)


    def testChange(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        instances = self.session.query(CertifyHost).all()
        for i in instances:
            print("%s" % i)
        
        

    def testLoad(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        instances = self.session.query(CertifyHost).all()
        for i in instances:
            print("%s" % i)

def save():
    t = SQLAlchemyTest()
    t.gatherEngines()
    t.createSQLiteDB()
    t.testSave()

    
def load():
    t = SQLAlchemyTest()
    t.gatherEngines()
    t.testLoad()

def change():
    t = SQLAlchemyTest()
    t.gatherEngines()
    t.testChange()

    
def info(): 
    t = SQLAlchemyTest()
    t.printVersion()
    t.gatherEngines()
 

if __name__ == '__main__':
    usage = "sqladb.py  [info, save, load]"
      
    
    args = sys.argv[1:]
    if len(args) < 1:
        print(usage)
        sys.exit()
    
    cmd =  args[0].strip().lower()
    if cmd == "info":
        info()
        sys.exit() 
    elif cmd == "save":
        save()
    elif cmd == "load":      
        load()
    elif cmd == "change":
        change()
    
    else:
        print('Command %d not recognized' % cmd)
        print(usage)
        
        

        
        
        

