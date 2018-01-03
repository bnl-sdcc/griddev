#!/usr/bin/env python
#

import sys
from distutils.core import setup

release_version='0.1'

setup(
    name="sqladb",
    version=release_version,
    description='Test project for SQLAlchemy',
    long_description='''Test project for SQLAlchemy.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'sqla',
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
    scripts=[ 'scripts/sqladb.sh',
             ],
    data_files=[ ('share/certify', 
                      ['README.txt',
                        ]
                  ),
                  ('share/certify/config', ['config/sqla.conf']              
                   ),
               ]
)

