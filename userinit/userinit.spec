#spec file for package userinit
#
# Copyright  (c)  2007 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#
#

Name:      userinit
Summary:   Runs user-level init scripts on startup.
Version:   0.9
Release:   0
License:   GPL
BuildArch: noarch
Vendor:    Brookhaven National Laboratory
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Provides:  userinit
Source0:   userinit-%{PACKAGE_VERSION}.tgz
BuildRoot: %{_tmppath}/userinit-build


%description
Allows user init scripts to be run upon system startup. Looks 
in ~/<username>/etc/init.d/ and runs all init scripts therein 
upon startup and shutdown.  

%prep
%setup -q

%build

%install
rm -rf %\{buildroot]
install -D userinit.sh  %{buildroot}/etc/init.d/userinit
install -D userinit.sysconfig %{buildroot}/etc/sysconfig/userinit

%clean
rm -rf %{buildroot}

%pre
#mkdir -p /etc/sysconfig

%post
chkconfig --add userinit
chkconfig userinit on

%preun

%postun
#

%files
%defattr(755,root,root,-)
/etc/init.d/userinit

%defattr(-,root,root,-)
%config /etc/sysconfig/userinit


%changelog
* Tue Jul 29 2008 - jhover (at) bnl.gov
- Initial RPM-ization
