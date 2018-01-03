#spec file for package altera-loader-c
#
#
# Copyright  (c)  2007 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#

Name:      altera-loader-c
Summary:   Loads program into Altera FPGA
Version:   0.1
Release:   1
License:   GPL
Vendor:    MARIACHI Project http://www-mariachi.physics.sunysb.edu
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Source0:   %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# Requires:  


%description
Loads program into Altera FPGA

%prep
%setup -q

%build
make


%install
rm -rf %\{buildroot]

mkdir -p %{buildroot}/usr/bin
cp -r alterald %{buildroot}/usr/bin/

mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp -r README.txt %{buildroot}/usr/share/doc/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%pre

%post

%preun

%postun


%files
%defattr(755,root,root,-)
/usr/bin/alterald
%defattr(-,root,root,-)
/usr/share/doc/%{name}-%{version}/README.txt

%changelog
* Fri Sep 14 2007 - jhover (at) bnl.gov
- Initial RPM-ization
