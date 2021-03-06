import glob
import os
import osgtest.library.core as core
import pwd
import re
import shutil
import socket
import time
import unittest

# ==========================================================================
# Note: March 2012 version, add checking prerequisites such as globus-proxy-utils,
# to avoid confusion.

class TestGlexec(unittest.TestCase):

    # Constants
    __glexec_client_cert = '/tmp/x509_client_cert'
    __grid_mapfile = core.config['system.mapfile']   # typically '/etc/grid-security/grid-mapfile'

    # attributes to be filled later
    __uid = ''
    __user_proxy_path = ''
    __good_gridmap = False

    # ==========================================================================

    def test_01_check_gridmap(self):
        if not core.rpm_is_installed('glexec'):
            core.skip('not installed')
            return

        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        user_cert_dn, user_cert_issuer = core.certificate_info(cert_path)

        key_dn = '"'+user_cert_dn+'"'+' '+core.options.username

        command = ('/bin/grep', key_dn, self.__grid_mapfile)
        status, stdout, stderr = core.system(command)
        self.assert_(status==0, 'Grid-mapfile entry for user '+core.options.username+' missing')
        TestGlexec.__good_gridmap = True

    def test_02_define_user_proxy_path(self):
        if not core.rpm_is_installed('glexec'):
            core.skip('not installed')
            return
        command = ('/usr/bin/id','-u')
        status, stdout, stderr = core.system(command, True)
        TestGlexec.__uid = stdout.rstrip()
        TestGlexec.__user_proxy_path = '/tmp/x509up_u'+self.__uid

    def test_03_create_user_proxy(self):
        # if the utils are not present, it won't work anyhow, so might as well skip the test
        if not core.rpm_is_installed('globus-proxy-utils'):
            core.skip('globus-proxy-utils not installed')
            return

        # ...and also skip if there is no glexec
        if not core.rpm_is_installed('glexec'):
            core.skip('not installed')
            return

        # OK, software is present, now just check it previous tests did create the proxy already so
        # we don't do it twice
        command = ('grid-proxy-info','-f',self.__user_proxy_path)
        status, stdout, stderr = core.system(command, True)

        if int(status)!=0: # no proxy found for some reason, try to construct a new one
            command = ('grid-proxy-init','-out',self.__user_proxy_path)
            password = core.options.password + '\n'
            status, stdout, stderr = core.system(command, True, password)
            self.assert_(status==0, 'grid-proxy-init for user '+core.options.username+' has failed even though globus-proxy-util was present')

        # we need to have the right permissions on that proxy for glexec to agree to work,
        # and the easiest way is to copy the file
        command = ('/bin/cp', self.__user_proxy_path, self.__glexec_client_cert)
        status, stdout, stderr = core.system(command)
        os.environ['GLEXEC_CLIENT_CERT']=self.__glexec_client_cert

    def test_04_glexec_switch_id(self):
        # if the utils are not present, it won't work anyhow, so might as well skip the test
        if not core.rpm_is_installed('globus-proxy-utils'):
            core.skip('globus-proxy-utils not installed')
            return

        if not core.rpm_is_installed('glexec'):
            core.skip('not installed')
            return

        command = ('grid-proxy-info','-f',self.__user_proxy_path)
        status, stdout, stderr = core.system(command, True)

        if int(status)!=0: # no proxy found even after previous checks, have to skip
            core.skip('suitable proxy not found')
            return

        command = ('/usr/sbin/glexec','/usr/bin/id','-u')

        status, stdout, stderr = core.system(command)
        switched_id = stdout.rstrip()

        self.assert_(self.__uid==switched_id, 'Glexec identity switch from root to user '+core.options.username+' failed')

    def test_05_glexec_proxy_cleanup(self):
        # if the utils are not present, it won't work anyhow, so might as well skip the test
        if not core.rpm_is_installed('globus-proxy-utils'):
            core.skip('globus-proxy-utils not installed')
            return

        if not core.rpm_is_installed('glexec'):
            core.skip('not installed')
            return
        try:
            status = os.unlink(self.__glexec_client_cert)
        except:
            pass
