#
# Testing code stripped out of command line client...
#
#
 
 
if test:
       if log.getEffectiveLevel() > logging.INFO:
           log.setLevel(logging.INFO)
       
       
       if not serv:
           for v in vomses:     
               # Get VO Name
               vs=servers[v]
               n=vs.getVOName()
               log.info( "VO Name: %s" % n)
               
               # Get and print VOMSMember objects
               members = vs.listMembers()
               for m in members:
                   print m
               
               #
               # Check version numbers
               #
               log.info("VOMSAdmin Version: %s" % vs.getVersion() )
   
       elif serv and not cache:
           vs = servers[serv]
           voname=vs.vo
           log.info("VO Name: %s" % voname )
                   
           newuser="/DC=org/DC=doegrids/OU=People/CN=John Q. User 123456"
           newuserca="/DC=org/DC=DOEGrids/OU=Certificate Authorities/CN=DOEGrids CA 1"
           newcn="John Q. User 123456"
           newmail="jqu@bnl.gov"
           newcerturi=""
           
           # create user
           log.debug("vomsutil.py: Creating new user for VOMS server %s..." % voname)
           
           nvm=VOMSMember(newuser, newcn, newuserca)    
           print nvm
           try:
               log.info("Creating new user...")
               vs.createUser(nvm)
                # add user to VO
               #log.info("Adding user to VO...")
               #vs.addMember( '/%s' % voname , newuser, newuserca)      
          
               log.info("Creating new group...")
               # create group
               pname = '/%s' % voname
               gname = '/%s/test' % voname
               vs.createGroup(parentname=pname , groupname=gname)
   
               # create role
               log.info("Creating new Role...")
               vs.createRole('Role=testrole')
        
               # add user to group
               log.info("Adding user to group...")
               vs.addMember( '/%s/test' % voname , newuser, newuserca)
            
               # assign user to role
               log.info("Assigning Role to user...")
               vs.assignRole('/%s/test' % voname, 'Role=testrole', newuser, newuserca)
                        
           except Exception, e:
               print e
            
           # Get and print VOMSMember objects
           members = vs.listMembers()
           for m in members:
               print m
            
           try:
               log.info("Deleting user...")
               vs.deleteUser(newuser, newuserca)
               log.info("Deleting group...")
               vs.deleteGroup('/%s/test' % voname)
               log.info("Deleting role...")
               vs.deleteRole('Role=testrole')

                       
           except Exception, e:
               print e                
                            
                
       elif serv and cache:
           log.info("Testing CachingVOMSWrapper...")    
           usertocheck = "/DC=org/DC=doegrids/OU=People/CN=John R. Hover 47116"
       
           log.info( "Testing isGroupMember() with caching..." )
           s = servers[serv]
           while(True):
               ans = s.isGroupMember(DN=usertocheck)
               time.sleep(testinterval)
               ans = s.isGroupMember(DN=usertocheck)
       
        