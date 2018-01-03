#!/usr/bin/env python
#
# Setup prog for VOMSAdmin Library
#
#

import sys
from distutils.core import setup

# For now, don't forget to increment this in certify-binary.py
release_version='0.9.1'

# Re-write version string in certify-binary.py
#f = open('./certify/certify-binary.py' ,'w')

setup(
    name="cloud-utils",
    version=release_version,
    description='Utilities for handling cloud-based clusters',
    long_description='''Utilities for handling cloud-based clusters''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'cloudutil',
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
    scripts=[ 'bin/cloud-util',
              'bin/runbyip',
             ],
    data_files=[ ('share/cloudutils', 
                      ['README',
                        ]
                  ),
                  ('share/cloudutils/etc', ['etc/cloudutil.conf','etc/clouds.conf']              
                   ),
               ]
)