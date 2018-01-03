#spec file for package natinst-kernel-mod
#
#
# Copyright  (c)  2007 Akshay Athalye <athalye@ece.sunysb.edu>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to athalye@ece.sunysb.edu
#

%define KernelVer %(uname -r)

Name:      natinst-kernel-mod-%{KernelVer}
Summary:   Pre-compiled kernel modules for Labview
Version:   1.0
Release:   1
License:   GPL
Vendor:    MARIACHI Project http://www-mariachi.physics.sunysb.edu
Packager:  Akshay Athalye <athalye@ece.sunysb.edu>
Group:     Scientific/Engineering
Source0:   natinst-kernel-mod-1.0.tar.gz
BuildRoot: %{_tmppath}/natinst-kernel-mod
Requires: gcc


%description
Pre-compiled kernel modules for labview and NIVISA

%prep
%setup -n natinst-kernel-mod-1.0


%build


%install
rm -rf %{buildroot}
install -d -o 0 -g 0 %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r ni4882 %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r nicore %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r nikal  %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r nipal %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r nipxi %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst
cp -r nivisa %{buildroot}/lib/modules/%{KernelVer}/kernel/natinst


%clean
rm -rf %{buildroot}

%pre


%post
depmod
/etc/init.d/nipal start

%preun


%postun


%files
%defattr(-,root,root,-)
/lib/modules/%KernelVer/kernel/natinst/ni4882/*
/lib/modules/%KernelVer/kernel/natinst/nicore/*
/lib/modules/%KernelVer/kernel/natinst/nikal/*
/lib/modules/%KernelVer/kernel/natinst/nipal/*
/lib/modules/%KernelVer/kernel/natinst/nipxi/*
/lib/modules/%KernelVer/kernel/natinst/nivisa/*


%changelog
