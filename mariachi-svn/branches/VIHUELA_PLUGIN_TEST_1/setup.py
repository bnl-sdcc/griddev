#!/usr/bin/env python2.4
#
# Setup prog for vihuela
#
#
release_version='0.1'

from distutils.core import setup

setup(
    name='vihuela',
    version=release_version,
    description='Generic thread-running daemon.',
    long_description='''Vihuela is a generalized python thread running daemon. It is used as the data upload component of the MARIACHI data acquisition network.''',
    license='GPL',
    author='John R. Hover',
    author_email='jhover@bnl.gov',
    url='http://www-mariachi.physics.sunysb.edu/wiki/index.php/SoftwareDevelopment',
    py_modules=[ 'vihuela.plugins.DummyPlugin',
                           'vihuela.plugins.GridsitePlugin',
                           'vihuela.plugins.SystemUpdatePlugin',
                           'vihuela.plugins.myurllib224',
                           'vihuela.ProxyHTTPConnection',
                           'vihuela.plugins',
                           'vihuela.core',
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
    data_files=[      ('/etc/vihuela', ['config/vihuela.conf',]),
                            ('/etc/init.d',['misc/vihuela',]),
                            ('/usr/sbin', ['scripts/vihuela-daemon.py',]),
                            ('usr/share/doc/vihuela', ['README.txt','LGPL.txt','GPL.txt', 'misc/notes.txt', 'misc/uml-design.uxf'])
                     ]
)

