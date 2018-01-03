#!/usr/bin/env python

from distutils.core import setup

release_version = '0.1'

setup(
    name='dcpin-common',
    version=release_version,
    description='dCache File Pinning System - Common Files and Libraries',
    long_description='''dcpin is a system to add on the capability of pinning and unpinning 
files stored in the dCache distributed filesystem.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='http://www.usatlas.bnl.gov/griddev/',
    packages=['dcpin' ],
    package_dir={'dcpin': 'dcpin'},

    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
        'Topic :: System :: Distributed Computing',
    ],
    data_files=[('share/doc/dcpin-%s' % release_version, ['docs/DEVEL.txt','docs/INSTALL.txt',
                  'docs/LICENSE.txt','docs/USAGE.txt', 'docs/README.txt']),
               ]
)