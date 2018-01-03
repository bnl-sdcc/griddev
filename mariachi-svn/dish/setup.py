#!/usr/bin/env python2.4
#
# Setup prog for DISH 
#
#
release_version='0.1'

from distutils.core import setup

setup(
    name='dish',
    version=release_version,
    description='Distributed Interactive Shell.',
    long_description='''DISH (Distributed Interactive Shell) is a tool to run shell commands on multiple hosts simultanously.''',
    license='GPL',
    author='John R. Hover',
    author_email='jhover@bnl.gov',
    url='http://www-mariachi.physics.sunysb.edu/wiki/index.php/SoftwareDevelopment',
    py_modules=[  'dish.core',
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
    data_files=[      ('/etc/dish', ['config/dish.conf',]),
                      ('/usr/bin', ['scripts/dish-binary.py',]),
                      ('usr/share/doc/dish', ['README.txt','LGPL.txt','GPL.txt' ])
                     ]
)

