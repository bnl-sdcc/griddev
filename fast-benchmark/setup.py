#!/usr/bin/env python
#
# Setup prog for Certify certificate management utility

import sys
from distutils.core import setup

from certify import core
release_version=core.__version__

setup(
    name="fast-benchmark",
    version=release_version,
    description='ATLAS hardware benchmark(s)',
    long_description='''ATLAS hardware benchmark(s)''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'fbmk',
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
    scripts=[ 'bin/bmk_lib.sh',
             ],
    data_files=[ ('share/certify', 
                      ['README.txt',
                       'NOTES.txt',            
                       'LGPL.txt',
                        ]
                  ),
                  ('share/certify/config', ['config/certify.conf','config/hosts.conf']              
                   ),
               ]
)

