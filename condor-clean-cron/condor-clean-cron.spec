#spec file for package condor-clean-cron
#
# Copyright  (c)  2008 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#
#

Name:      condor-clean-cron
Summary:   Cleans up held and idle Condor-G jobs, restarts gahp_server
Version:   0.6
Release:   2
License:   GPL
BuildArch: noarch
Vendor:    Brookhaven National Laboratory
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Provides:  condor-clean-cron
Source0:   condor-clean-cron-%{PACKAGE_VERSION}.tgz
BuildRoot: %{_tmppath}/condor-clean-cron-build


%description
Cleans up held and idle Condor-G jobs, restarts gahp_server  

%prep
%setup -q

%build

%install
rm -rf %\{buildroot]
install -D condor-clean.cron  %{buildroot}/etc/cron.d/condor-clean
install -D condor-clean-cron.sh %{buildroot}/usr/libexec/condor-clean-cron.sh
install -D condor-clean.logrotate %{buildroot}/etc/logrotate.d/condor-clean

%clean
rm -rf %{buildroot}

%pre
#mkdir -p /var/l

%post
#chkconfig --add userinit
#chkconfig userinit on

%preun

%postun
#

%files
%defattr(-,root,root,-)
/etc/logrotate.d/condor-clean

%defattr(755,root,root,-)
/usr/libexec/condor-clean-cron.sh

%defattr(644,root,root,-)
/etc/cron.d/condor-clean


#%defattr(-,root,root,-)
#%config /etc/sysconfig/userinit


%changelog
* Mon Sep 29 2008 - jhover (at) bnl.gov
- Initial RPM-ization
