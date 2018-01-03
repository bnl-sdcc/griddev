#!/usr/bin/env python
#
# Setup prog for interdash dashboard app
#
#
release_version='0.1'

from distutils.core import setup

setup(
    name='interdash',
    version=release_version,
    description='Facility dashboard app.',
    long_description='''Web-based facility dashboard app.''',
    license='GPL',
    author='John R. Hover',
    author_email='jhover@bnl.gov',
    url='http://www.racf.bnl.gov/experiments/usatlas/griddev',
    packages=[  'site', 
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
    
    data_files=[ ( '/etc/httpd/http.d/',['config/interdash.conf',]),
                #( '/etc/mariachi', ['config/mariachi-ws.conf','misc/no_data-648x504.png']), 
                ('/usr/share/doc/interdash', ['README.txt',
                                             'LGPL.txt',
                                             'GPL.txt',]),
                ('/usr/share/interdash', ['share/file.txt',
                                                 ]),                                                          
                ('/usr/share/interdash/templates',['share/templates/base.html',
                                                          ]),
                ('/usr/share/interdash/static/css/custom',['static/css/custom/default.css',                                                                  
                                                                  ]), 
               ]
)

