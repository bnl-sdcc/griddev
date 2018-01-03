OVERVIEW
=======================================================
Python-vomsadmin is a command-line client for interacting with the Virtual Organization Management Service (VOMS). 

INSTALLATION
======================================================
There are two approaches to installation, RPM or home directory based. 

RPM Installation
--------------------
In root of source directory, run 

      python setup.py bdist_rpm

This should create the RPM in dist/.

The RPM requires python-ZSI (Zolera Soap Infrastructure). This is available in RPM format from EPEL, and directly from Fedora. 

NOTE: On Redhat/Fedora it may be necessary to disable certain rpmbuild "features" because the Redhat way breaks bdist_rpm:
As root, for all users:
   echo  "%_unpackaged_files_terminate_build 0" > /etc/rpm/macros.bdist_rpm

As user:
   echo "%_unpackaged_files_terminate_build 0" >> ~/.rpmmacros


Home Directory Installation
---------------------------
In the root of the source directory, run 

     python setup.py install --home=~/
     
This will install the package in ~/bin, ~/etc, ~/lib/python/, with logging to ~/var/log
The installation requires ZSI (Zolera Soap Infrastructure). This can be downloaded from:
   http://sourceforge.net/projects/pywebsvcs/files/ZSI/
ZSI 2.0 has been tested and works. 


USAGE NOTES
========================================================
-- The vomsadmin.conf file should serve as a guide to setting the client up to interact with your server.
-- As this was designed to work from a secure, single-user host in an automated fashion (for automatic synchronization) it may be necessary to make a userkey.pem without a password. To remove a passphrase from an existing key:
        openssl rsa -in userkey.pem -out userkeynopw.pem
-- See NOTES.txt to see which API commands have been implemented, and which have not. 
-- PLEASE ignore the various sync-attributes* and voms-replicat* scripts in scripts/. These are ad-hoc scripts to handle user attributes. This functionality will be added to the main client, but hasn't been done yet.      
  











