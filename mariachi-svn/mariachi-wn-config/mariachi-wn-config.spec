#spec file for package mariachi-wn-config
#
# Copyright  (c)  2007 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#
# NFS
# Condor
# SSH keys
# Yum repo config
#
#

Name:      mariachi-wn-config
Summary:   Config and meta-package for Worker Node setup.
Version:   1.1
Release:   2
License:   GPL
Vendor:    MARIACHI Project http://www-mariachi.physics.sunysb.edu
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Requires:  condor nfs-utils portmap
Provides:  mariachi-wn-config
Source0:   mariachi-wn-config-%{PACKAGE_VERSION}.tgz
BuildRoot: %{_tmppath}/mariachi-wn-config-build


%description
Sets up all specialized config for Mariachi cluster worker nodes. 

%prep
%setup -q

%build


%install
rm -rf %\{buildroot]
install -d -o 0 -g 0 %{buildroot}/root/.ssh
install -d -o 0 -g 0 %{buildroot}/usr/share/mariachi-wn-config
install -d -o 0 -g 0 %{buildroot}/usr/sbin
cp root/authorized_keys %{buildroot}/root/.ssh/
cp -r share/* %{buildroot}/usr/share/mariachi-wn-config
cp sbin/* %{buildroot}/usr/sbin

%clean
rm -rf %{buildroot}

%pre
mkdir -p /nfs/mariachi.stonybrook.edu

%post
/usr/sbin/config-nfs-client.sh --on
/usr/sbin/config-nfs-client.sh --fstabadd
/usr/sbin/config-nfs-client.sh --setidmapd
mount -a
/usr/sbin/config-mariachi-users.sh --add

%preun
/usr/sbin/config-mariachi-users.sh --remove
umount -fl /nfs/mariachi.stonybrook.edu
/usr/sbin/config-nfs-client.sh --off
/usr/sbin/config-nfs-client.sh --fstabremove
/usr/sbin/config-nfs-client.sh --unsetidmapd


%postun
rmdir /nfs/mariachi.stonybrook.edu


%files
%defattr(755,root,root,-)
/usr/sbin/config-nfs-client.sh
/usr/sbin/config-mariachi-users.sh

%defattr(-,root,root,-)
/usr/share/mariachi-wn-config/fstab.template
/usr/share/mariachi-wn-config/hosts.allow.template
/usr/share/mariachi-wn-config/idmapd.conf.template
/usr/share/mariachi-wn-config/users.data.txt

%defattr(644,root,root,-)
/root/.ssh/authorized_keys


%changelog
* Fri Feb 29 2008 - jhover (at) bnl.gov
- Initial RPM-ization
