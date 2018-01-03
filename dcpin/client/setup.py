#!/usr/bin/env python

from distutils.core import setup

release_version = '0.1'

setup(
    name='dcpin-client',
    version=release_version,
    description='dCache File Pinning System - Client',
    long_description='''dcpin is a system to add on the capability of pinning and unpinning 
files stored in the dCache distributed filesystem.''',
    license='GPL',
    author='John Hover,Xin Zhao, Hironori Ito',
    author_email='jhover@bnl.gov',
    url='http://www.usatlas.bnl.gov/griddev/',
    scripts=['scripts/dcpin-client.py' ],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System :: Distributed Computing',
    ],
    data_files=[( '/etc/dcpin',['config/client.conf',] )],

)