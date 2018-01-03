#!/usr/bin/env python
#
# Setup prog for mariachi-data-ws
#
#
release_version='0.99'

from distutils.core import setup

setup(
    name='mariachi-data-ws',
    version=release_version,
    description='MARIACHI Data Web Services.',
    long_description='''Web-based access to MARIACHI data.''',
    license='GPL',
    author='John R. Hover',
    author_email='jhover@bnl.gov',
    url='http://www-mariachi.physics.sunysb.edu/wiki/index.php/SoftwareDevelopment',
    packages=[  'mdsite', 
                'mariachiws',
                'mdsite.templatetags'
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
    
    data_files=[ ( '/etc/httpd/http.d/',['config/mariachi-python.conf',]),
                #( '/etc/mariachi', ['config/mariachi-ws.conf','misc/no_data-648x504.png']), 
                ('/usr/share/doc/mariachi', ['README.txt',
                                             'LGPL.txt',
                                             'GPL.txt',]),
                ('/usr/share/mariachi-data-ws', ['share/manalysis.R',
                                                 'README.txt',
                                                 'config/mariachi-ws.conf',
                                                 'misc/no_data-648x504.png'
                                                 ]),                                                          
                ('/usr/share/mariachi-data-ws/templates',['share/templates/dataquery.html',
                                                          'share/templates/base.html',
                                                          'share/templates/analysis.html',
                                                          ]),
                ('/usr/share/mariachi-data-ws/static/css/custom',['static/css/custom/default.css',                                                                  
                                                                  ]), 
               ]
)

