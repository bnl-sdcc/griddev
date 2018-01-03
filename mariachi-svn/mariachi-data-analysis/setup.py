#!/usr/bin/env python
#
# Setup prog for VOMSAdmin Library
#
#

import sys
from distutils.core import setup

# For now, don't forget to increment this in certify-binary.py
release_version='0.7.0'

# Re-write version string in certify-binary.py
#f = open('./certify/certify-binary.py' ,'w')

setup(
    name="mariachi-data-analysis",
    version=release_version,
    description='Utilities for hanlding MARIACHI data analysis.',
    long_description='''Simple tools for handling MARIACHI data analysis.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www-mariachi.physics.sunysb.edu/',
    packages=[ 'mariachida',
              ],
    classifiers=[
          'Development Status :: 3 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Physics',
    ],
    scripts=[ 'scripts/mdanalysis',
             ],
             
    data_files=[ ('share/mariachi-data-analysis', 
                      ['share/analysis2.R',
                       'config/analysis.conf',
                      ]
                  ),
               ]
)

