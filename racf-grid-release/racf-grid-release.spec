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

Name:      racf-grid-release
Summary:   Yum release package for RACF Grid Group repository
Version:   0.9
Release:   7
BuildArch: noarch
License:   GPL
Vendor:    RACF http://www.racf.bnl.gov/
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Requires:  yum
Provides:  racf-grid-release
Source0:   racf-grid-release-%{version}.tgz
BuildRoot: %{_tmppath}/racf-grid-release-build


%description
Yum release package for RACF Grid Group repository.  

%prep
%setup -q

%build


%install
rm -rf %\{buildroot]
mkdir -p %{buildroot}/etc/yum.repos.d
cp racf-grid-production.repo %{buildroot}/etc/yum.repos.d/
cp racf-grid-testing.repo %{buildroot}/etc/yum.repos.d/
cp racf-grid-development.repo %{buildroot}/etc/yum.repos.d/
cp racf-grid-external.repo %{buildroot}/etc/yum.repos.d/
mkdir -p %{buildroot}/etc/pki/rpm-gpg/
cp RPM-GPG-KEY-racf-grid.asc  %{buildroot}/etc/pki/rpm-gpg/


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
#/usr/share/projectname/projectfile
/etc/pki/rpm-gpg/RPM-GPG-KEY-racf-grid.asc


%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/racf-grid-testing.repo
%config(noreplace) /etc/yum.repos.d/racf-grid-development.repo
%config(noreplace) /etc/yum.repos.d/racf-grid-production.repo
%config(noreplace) /etc/yum.repos.d/racf-grid-external.repo

# secret files
%defattr(644,root,root,-)
#/root/.projectname/project.cfg

%changelog
* Fri May 13 2011 - jhover (at) bnl.gov
- Initial RPM-ization
