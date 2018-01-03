#!/usr/bin/env python
#
# Setup prog for mariachi-data-ws
#
#
release_version='0.3'

from distutils.core import setup

setup(
    name='httpcheck',
    version=release_version,
    description='Functionality checker for http/mod_python/etc',
    long_description='''Functionality checker for http/mod_python/etc.''',
    license='GPL',
    author='John R. Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[  'httpcheck'
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
    
    data_files=[ ( '/etc/httpd/conf.d/',['config/httpcheck.conf',]),
                ('/usr/share/doc/httpcheck', ['README.txt',
                                             'LGPL.txt',
                                             'GPL.txt',]),
                ('/usr/share/httpcheck/httproot', ['share/index.html',]),
               ]
)

