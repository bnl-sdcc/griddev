#!/usr/bin/env python
#
# Setup prog for VOMSAdmin Library
#
#
release_version='0.2'

import sys
from distutils.core import setup

setup(
    name="python-vomsadmin",
    version=release_version,
    description='Utilities for dealing with VOMS',
    long_description='''Simple tools for dealing with VOMS information.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='http://www-mariachi.physics.sunysb.edu/wiki/index.php/SoftwareDevelopment',
    packages=[ 'vomsadmin',
               'vomsSOAPpy',
               'vomsSOAPpy.wstools',
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
    data_files=[ ('/usr/share/doc/python-vomsadmin-%s' %  release_version, 
                      ['README.txt',                   
                       'GPL.txt',
                       'config/python-vomsadmin.conf',
                       'config/VOMSAdmin.soappy.wsdl',   
                       ]
                  )
    ]
)

