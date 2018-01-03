#!/usr/bin/env python
#
# Setup prog for VOMSAdmin Library
#
#
import sys
import ConfigParser
from distutils.core import setup

major, minor, release, st, num = sys.version_info

release_version="0.9.9"

setup(
    name="vomsadmin-utils",
    version=release_version,
    description=' VOMS Admin utilities',
    long_description='''This package contains the VOMS-Admin command line utilities.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='http://www.racf.bnl.gov/experiments/usatlas/griddev/vomsadminclient',
    packages=[ 'VOMSAdminUtils',
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
    scripts = ['scripts/vomsadmin-util',
               'scripts/atlas-sync-cron.sh'                          
               ],
    data_files=[ ('share/vomsadmin-utils-%s' %  release_version, 
                      ['README.txt',
                       'NOTES.txt',                   
                       'GPL.txt',
                       'config/vomsadmin.conf',
                       ]
                  )
    ]
)

