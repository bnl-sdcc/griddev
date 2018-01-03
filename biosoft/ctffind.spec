# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:           ctffind
Version:        4.0.16
Release:        1%{?dist}
Summary:        Bio program for EM
Group:          System Environment/Base

License:        GPLv2
URL:            http://grigoriefflab.janelia.org/ctf
Source0:        http://dev.racf.bnl.gov/dist/src/tgz/%{name}-%{version}-linux64.tar.gz

Requires:  fftw >= 3.3
Requires:  gsl
Requires:  blas64
Requires:  openmpi

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#BuildRequires:  fftw-devel >= 3.3
#BuildRequires:  gsl-devel >= 1.15 
#BuildRequires:  blas64-devel >= 3.4.2
#BuildRequires:  openmpi-devel >= 0.9

%description
CTFFIND3 and CTFTILT are two programs for finding CTFs of electron micrographs

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/usr/bin

# in builddir
cp -v ctffind %{buildroot}/usr/bin
cp -v ctffind_plot_results.sh %{buildroot}/usr/bin

%files
%{_bindir}/%{name}
%{_bindir}/ctffind_plot_results.sh


%changelog
* Mon Oct 19 2015 John Hover <jhover@bnl.gov>
- Initial build of 4.0.16. 