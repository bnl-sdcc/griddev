#!/usr/bin/env python

from distutils.core import setup

release_version = '0.1'

setup(
    name='dcpin-server',
    version=release_version,
    description='dCache File Pinning System - Server Daemon',
    long_description='''dcpin is a system to add on the capability of pinning and unpinning 
files stored in the dCache distributed filesystem.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='http://www.usatlas.bnl.gov/griddev/',
    scripts=['scripts/dcpin-server.py', ],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System :: Distributed Computing',
    ],
    data_files=[('share/doc/dcpin-%s/misc' % release_version, ['misc/dcache_file_lock.sh', 
                 'misc/refresh_dcache_ssh_process.sh',
                 'misc/lockfiles-README.txt']),
                 ('/etc/dcpin',['config/server.conf',]),
               ]

)
