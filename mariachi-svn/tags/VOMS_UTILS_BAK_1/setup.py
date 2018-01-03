#!/usr/bin/env python2.4
#
# Setup prog for VOMS utilities
#
#
release_version='0.1'

from distutils.core import setup

setup(
    name='voms-utils',
    version=release_version,
    description='Utilities for dealing with VOMS',
    long_description='''Simple tools for dealing with VOMS information.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='http://www-mariachi.physics.sunysb.edu/wiki/index.php/SoftwareDevelopment',
    py_modules=[  'vomsutils',
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
    data_files=[      ('/etc/grid-security', ['config/mkdnlist.conf',]),
                            ('/usr/sbin', ['scripts/mkdnlist.py',]),
                            ('usr/share/doc/voms-utils', ['README.txt','GPL.txt',])
                     ]
)

