#!/usr/bin/env python
#
# Distutils setup script for python-gridftp
# Created as part of the Don Quixote 2 DDM project
# # https://uimon.cern.ch/twiki/bin/view/Atlas/DistributedDataManagement
#
#


from distutils.core import setup, Extension

release_version = '0.99'

setup(
    name='python-gridftp',
    version=release_version,
    description='Python GridFTP extension',
    long_description='''Provides GridFTP interface for Python applications''',
    license='GPL',
    author='Miguel Branco',
    author_email='miguel.branco@cern.ch',
    url='https://uimon.cern.ch/twiki/bin/view/Atlas/DistributedDataManagement',

    
    #
    # Module Description
    #
    py_modules= ['GridFTP'],
    
    
    #           
    # Describe extensions...
    #
    
    ext_modules=[Extension( 
                      'libgridftp', ['libgridftp.c','libgridftp.i'], 
                      include_dirs=['./','/afs/cern.ch/atlas/offline/external/GRID/build/globus/include/gcc32dbg',],
                      library_dirs=['/afs/cern.ch/atlas/offline/external/GRID/build/globus/lib'],
                      libraries=['globus_gssapi_gsi_gcc32dbg', 'globus_gss_assist_gcc32dbg', 
                            'globus_ftp_client_gcc32dbg', 'globus_gass_copy_gcc32dbg'],
                                               )
                  ],
    
    
    
    #
    # Info for Sourceforge/RPM
    #
    classifiers=[ 'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Physics',
                ],
    )

