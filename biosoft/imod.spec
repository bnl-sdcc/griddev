%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:           imod
Version:        4.7.15
Release:        5%{?dist}
Summary:        3D image processing tools for EM
Group:          Applications/Scientific

License:        GPLv2
URL:            http://bio3d.colorado.edu/imod/
Source0:        http://dev.racf.bnl.gov/dist/src/tgz/%{name}-%{version}.rhel7-64-cuda6.5.tar.gz 

Requires:  java-1.7.0-openjdk
# Requires:  jre

#Requires:  blas64
Requires:  openmpi
Requires:  environment-modules

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#BuildRequires:   fftw-devel >= 3.3
#BuildRequires:   gsl-devel >= 1.15 
#BuildRequires:  blas64-devel >= 3.4.2
#BuildRequires:  openmpi-devel >= 0.9

#BuildRequires:  fuse-devel, curl-devel, libxml2-devel
#BuildRequires:  openssl-devel, mailcap
#Conflicts:      fuse-s3fs


AutoReqProv: no

%description
IMOD is a set of image processing, modeling and display programs used for tomographic reconstruction and for 3D reconstruction of EM serial sections and optical sections. The package contains tools for assembling and aligning data within multiple types and sizes of image stacks, viewing 3-D data from any orientation, and modeling and display of the image files.

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/usr/lib/imod


# in builddir
cp -vr * %{buildroot}/usr/lib/imod
#cp -a * %{buildroot}
#cp -v ctffind %{buildroot}/usr/bin
#cp -v ctffind_plot_results.sh %{buildroot}/usr/bin
# make install DESTDIR=%{buildroot}

%files
/usr/lib/imod
#%{_bindir}/%{name}
#%{_bindir}/ctffind_plot_results.sh

#%{_mandir}/man1/%{name}.1*
#%doc AUTHORS README passwd-s3fs

%post
cd /etc/profile.d
ln -s /usr/lib/imod/IMOD-linux.* ./
echo /usr/lib/imod/qtlib > /etc/ld.so.conf.d/imod.conf
ldconfig

%preun
rm /etc/profile.d/IMOD-linux.*
rm /etc/ld.so.conf.d/imod.conf


%changelog
* Mon Oct 19 2015 John Hover <jhover@bnl.gov>
- Initial build of 4.0.16. 
