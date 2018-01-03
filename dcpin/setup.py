#!/usr/bin/env python
#

import os, sys, getopt

subprojects = [ 'common' , 'server' , 'client' ]

if __name__ == "__main__":
    
    usage = 'Simple build script. Passes args to setup.py on all subprojects: %s' % subprojects
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hdv", ["help", "debug", "verbose"])
    except getopt.GetoptError:
        print "Unknown option..."
        print usage                          
        sys.exit(1)        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage                     
            sys.exit()            
    
    if args:
        if "rpm_install" in args:
            for proj in subprojects:
                result = os.popen('sudo rpm -Uvh --force %s/dist/*.noarch.rpm' % proj )
                for line in result:
                    sys.stdout.write(line)
            sys.exit()
        
        allargs = " ".join(args)
        for proj in subprojects:
            print 'Changing dir to "%s" and running setup.py with args "%s" ' % (proj, allargs)
            result = os.popen('cd %s ; ./setup.py %s ' % ( proj, allargs) ).readlines()
            for line in result:
                sys.stdout.write(line)

        if "clean" in args:
            for proj in subprojects:
                print 'Changing dir to "%s" and removing dist, MANIFEST, etc...' % proj
                result = os.popen('rm -rf %s/dist %s/MANIFEST' % ( proj, proj) )
                for line in result:
                    sys.stdout.write(line)
            sys.exit()      


    else:
        print usage
        print 'No arguments given. Try "bdist_rpm" or "clean --all".'
            




