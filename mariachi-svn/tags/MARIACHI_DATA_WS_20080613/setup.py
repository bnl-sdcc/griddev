#!/usr/bin/env python
#
# Setup prog for mariachi-data-ws
#
#
release_version='0.7'

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
                 ( '/etc/mariachi', ['config/mariachi-ws.conf','misc/no_data-648x504.png']), 
                 
                    #('/etc/logrotate.d',['config/vihuelalr',]),
                    #        ('/etc/init.d',['misc/vihuela',]),
                    #        ('/usr/sbin', ['scripts/vihuela-daemon.py',]),
                ('/usr/share/doc/mariachi', ['README.txt','LGPL.txt','GPL.txt',]),
                ('/usr/share/mariachi-data-ws/templates',['share/templates/mainpage.html',
                                                          'share/templates/dataquery.html',
                                                          'share/templates/base.html',
                                                          ]), 
               ]
)

