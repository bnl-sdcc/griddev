#spec file for package mariachi-daq-tunnel
#
#
# Copyright  (c)  2007 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#

Name:      mariachi-daq-tunnel
Summary:   Establishes persistent reverse SSH tunnel to main server.
Version:   0.3
Release:   1
License:   GPL
Vendor:    MARIACHI Project http://www-mariachi.physics.sunysb.edu
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Source0:   %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# Requires:  


%description
Establishes persistent reverse SSH tunnel to main server.

%prep
%setup -q

%build


%install
rm -rf %\{buildroot]

mkdir -p %{buildroot}/home/daq/bin
cp -r bin/* %{buildroot}/home/daq/bin/
mkdir -p %{buildroot}/home/daq/.ssh
cp -r dotssh/* %{buildroot}/home/daq/.ssh
mkdir -p %{buildroot}/etc/cron.d
cp -r etc/tunnel-cron %{buildroot}/etc/cron.d

%clean
rm -rf %{buildroot}

%pre
useradd daq
mkdir -p ~daq/bin
mkdir -p ~daq/var/log
mkdir -p ~daq/.ssh
chown -R daq:daq ~daq

%post

%preun

%postun


%files
%defattr(755,daq,daq,-)
/home/daq/bin/ssh-tunnel-cron.sh
%defattr(-,daq,daq,-)
/home/daq/.ssh/config
%defattr(600,root,root,-)
/etc/cron.d/tunnel-cron


%changelog
* Wed Aug 1 2007 - jhover (at) bnl.gov
- Initial RPM-ization
