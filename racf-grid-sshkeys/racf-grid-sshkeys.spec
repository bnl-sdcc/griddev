#spec file for package racf-grid-release
#
# Copyright  (c)  2011 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#
#
#

Name:      racf-grid-sshkeys
Summary:   Yum release package for RACF Grid Group SSH keys
Version:   0.9
Release:   1
BuildArch: noarch
License:   GPL
Vendor:    RACF http://www.racf.bnl.gov/
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Requires:  yum
Provides:  racf-grid-sshkeys
Source0:   racf-grid-sshkeys-%{version}.tgz
BuildRoot: %{_tmppath}/racf-grid-sshkeys-build


%description
Yum release package for RACF Grid Group SSH keys.

%prep
%setup -q

%build


%install
rm -rf %\{buildroot]
mkdir -p %{buildroot}/root/.ssh
chmod go-rwx %{buildroot}/root/.ssh
cp authorized_keys %{buildroot}/root/.ssh/

# E.g. create root-owned directories and copy files
#mkdir -p %{buildroot}/usr/share/projectname
#mkdir -p %{buildroot}/usr/bin
#mkdir -p %{buildroot}/root/.projectname
#cp -r share/* %{buildroot}/usr/share/projectname
#cp bin/projectbin %{buildroot}/usr/bin/
#cp cfg/project.cfg %{buildroot}/root/.projectname/

%clean
rm -rf %{buildroot}

%pre
#mkdir -p /usr/share/projectname
#mkdir -p /etc/projectname

%post

%preun

%postun
#rmdir /usr/share/projectname

%files
%defattr(755,root,root,-)
#/usr/bin/projectbin.sh

%defattr(-,root,root,-)

%defattr(-,root,root,-)

# secret files
%defattr(600,root,root,-)
/root/.ssh
/root/.ssh/authorized_keys

%changelog
* Mon Jan 30 2012 - jhover (at) bnl.gov
- Initial RPM-ization
