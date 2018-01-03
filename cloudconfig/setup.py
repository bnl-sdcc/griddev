#!/usr/bin/env python
#
# Simple utility for early initialization of cloud VMs. 
#
# Goals: 
#  generic:  usable with EC2, libvirt, openstack, etc. 
#  modular:  Separate files for each function
#  flexible:  Doesn't assuma any one scheme. Allows local defaults.  
#

import sys
from distutils.core import setup

release_version='0.1.2'

# ===========================================================
#           data files
# ===========================================================

libexec_files = ['etc/exec.d/10userdata.sh',
                 'etc/exec.d/30ephemeral.sh',
                 'etc/exec.d/40runpuppet.sh',
                  ]
conf_files = [ 'etc/conf.d/ephemeral.conf',
               'etc/conf.d/userdata.conf',
               'etc/conf.d/runpuppet.conf',
              ]
etc_files = ['etc/cloudconfig.conf-example',]
initd_files = ['etc/cloudconfig',]
sysconf_files = [ 'etc/cloudconfig.sysconfig',]

# -----------------------------------------------------------
rpm_data_files=[('/etc/cloudconfig/exec.d',   libexec_files),
                ('/etc/cloudconfig/conf.d',   conf_files),
                ('/etc/cloudconfig',          etc_files),
                ('/etc/init.d',               initd_files),
                ('/etc/sysconfig',            sysconf_files),
                ('share/cloudconfig',         ['README.txt',
                                               'LGPL.txt',]),                                                                             
               ]      
    
setup(
    name="cloudconfig",
    version=release_version,
    description='Utility for early initialization of cloud VMs.',
    long_description='''Simple tools for for early initialization of cloud VMs.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'cloudconfig',
              ],
    classifiers=[
          'Development Status :: 3 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System Administration :: Management',
    ],
      
    data_files=rpm_data_files
)

