#!/usr/bin/env python
#
# Setup prog for InCommon Utilities

import sys
from distutils.core import setup

release_version="0.9.0"

setup(
    name="icutils",
    version=release_version,
    description='Utilities for InCommon/Shibboleth file transfer.',
    long_description='''Utilities for InCommon/Shibboleth file transfer.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'icutils',
               'easywebdav'
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
    scripts=[ 'bin/fedcopy',
             ],
    data_files=[ ('share/icutils', 
                      ['README.txt',
                       'NOTES.txt',            
                        ]
                  ),
               ]
)

