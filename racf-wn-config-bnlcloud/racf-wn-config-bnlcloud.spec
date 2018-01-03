#spec file for package racf-wn-config-bnlcloud
#
# Copyright  (c)  2012 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#
#
#

Name:      racf-wn-config-bnlcloud
Summary:   Worker node configured for BNL_CLOUD usage.
Version:   0.9
Release:   1
BuildArch: noarch
License:   GPL
Vendor:    RACF http://www.racf.bnl.gov/
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Requires:  condor
Provides:  racf-wn-config-bnlcloud
Source0:   racf-wn-config-bnlcloud-%{version}.tgz
BuildRoot: %{_tmppath}/racf-wn-config-bnlcloud-build


%description
Worker node configured for BNL_CLOUD usage.   

%prep
%setup -q

%build

%install
rm -rf %\{buildroot]

mkdir -p %{buildroot}/etc/condor/config.d
cp etc/10cloudwn.config %{buildroot}/etc/condor/config.d/


mkdir -p %{buildroot}/usr/libexec
cp libexec/configurewn.sh %{buildroot}/usr/libexec
cp libexec/jobwrapper.sh %{buildroot}/usr/libexec

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


%post
/usr/libexec/configurewn.sh

%preun

%postun


%files
%defattr(755,root,root,-)
/usr/libexec/configurewn.sh
/usr/libexec/jobwrapper.sh

%defattr(-,root,root,-)
#/usr/share/projectname/projectfile
/etc/condor/config.d/10cloudwn.config


%defattr(-,root,root,-)
# %config(noreplace) /etc/yum.repos.d/racf-grid-testing.repo


# secret files
%defattr(644,root,root,-)
#/root/.projectname/project.cfg

%changelog
* Sat May 19 2012 - jhover (at) bnl.gov
- Initial RPM-ization
