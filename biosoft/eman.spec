# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing
#
# http://blake.bcm.edu/emanwiki/EMAN2/COMPILE_EMAN2_LINUX#CentOS_7
#
#%define        __spec_install_post %{nil}
#%define          debug_package %{nil}
#%define        __os_install_post %{_dbpath}/brp-compress
#
#
#  /usr/include/freetype -> /usr/include/freetype2/freetype
#
#


Name:           eman
Version:        2.12
Release:        2%{?dist}
Summary:        Image processing program for EM
Group:          System Environment/Base

License:        GPLv2
URL:            http://blake.bcm.edu/emanwiki/EMAN2/Install
Source0:        http://dev.racf.bnl.gov/dist/src/tgz/%{name}-%{version}.source.tar.gz


Requires:  boost-python
#Requires:  fftw, fftw-libs-double, fftw-libs-long, fftw-libs-single
Requires:  ftgl 
Requires:  freeglut
Requires:  freetype   
Requires:  fftw2  
Requires:  gsl
Requires:  hdf5
Requires:  h5py 
Requires:  hdf5     
Requires:  libdb
Requires:  libjpeg-turbo
Requires:  libpng
Requires:  libtiff, libtiff-tools
Requires:  mesa-libGLU   
Requires:  numpy, numpy-f2py
Requires:  openssl, openssl-libs

Requires:  python >= 2.7
Requires:  python-ipython
Requires:  python-jsonrpclib
Requires:  python-matplotlib, python-matplotlib-qt4
Requires:  python-twisted-core
Requires:  python-zope-component, python-zope-configuration, python-zope-deprecation
Requires:  python-zope-event, python-zope-exceptions, python-zope-i18nmessageid, python-zope-interface
Requires:  python-zope-schema, python-zope-sqlalchemy, python-zope-testing
Requires:  PyOpenGL
Requires:  PyQt4
Requires:  pytz  

Requires:  qt, qt-x11, qt-config, qt-devel
Requires:  sip
Requires:  scipy

 
BuildRequires: boost-devel
BuildRequires: boost-openmpi-devel
BuildRequires: fftw2-devel
BuildRequires: freetype-devel
BuildRequires: ftgl-devel
BuildRequires: fftw-devel
BuildRequires: gsl-devel
BuildRequires: hdf5-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng12-devel
BuildRequires: libtiff-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: PyQt4-devel
BuildRequires: python-devel
BuildRequires: sip-devel
#

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

AutoReqProv: no

%description
It is a broadly based greyscale scientific image processing suite with a primary focus on 
processing data from transmission electron microscopes. EMAN's original purpose was 
performing single particle reconstructions (3-D volumetric models from 2-D cryo-EM images) 
at the highest possible resolution, but the suite now also offers support for single 
particle cryo-ET, and tools useful in many other subdisciplines such as helical 
reconstruction, 2-D crystallography and whole-cell tomography. 

%description
%{summary}

%prep
%setup -q

%build
cd build
%cmake  ../eman2/
make DESTDIR=%{buildroot}
# make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{_builddir}/%{name}-%{version}/build
make install DESTDIR=%{buildroot}

# Create EMAN2DIR
mkdir -v -p %{buildroot}/usr/lib64/eman2/lib

# Handle pmconfig
mv -v %{buildroot}/usr/lib/pmconfig  %{buildroot}/usr/lib64/eman2/lib/

# Handle lib and test
mkdir -v -p %{buildroot}/usr/lib64/python2.7/site-packages/eman2
cp -v %{buildroot}/usr/lib/*.so  %{buildroot}/usr/lib64
mv -v %{buildroot}/usr/lib/* %{buildroot}/usr/lib64/python2.7/site-packages
mv -v %{buildroot}/usr/test %{buildroot}/usr/lib64/python2.7/site-packages/eman2
rmdir %{buildroot}/usr/lib

# Handle fonts
mkdir -v -p %{buildroot}/usr/share/fonts
mv -v %{buildroot}/usr/fonts/* %{buildroot}/usr/share/fonts

# Handle docs/examples
mkdir -v -p %{buildroot}/usr/share/doc/%{name}-%{version}/
mv -v %{buildroot}/usr/doc/* %{buildroot}/usr/share/doc/%{name}-%{version}/
mv -v %{buildroot}/usr/examples %{buildroot}/usr/share/doc/%{name}-%{version}/
rmdir %{buildroot}/usr/doc

# Handle images (and font?)
mv -v %{buildroot}/usr/images %{buildroot}/usr/lib64/eman2/
## mv -v %{buildroot}/usr/fonts %{buildroot}/usr/lib64/eman2
rmdir %{buildroot}/usr/fonts


%files
/usr/bin/*
/usr/include/*
/usr/lib64/python2.7/site-packages/*
/usr/lib64/eman2
/usr/lib64/*.so
/usr/share/doc/*
/usr/share/fonts/*


%post
echo "export EMAN2DIR=/usr/lib64/eman2" > /etc/profile.d/eman2.sh
echo "setenv EMAN2DIR /usr/lib64/eman2" > /etc/profile.d/eman2.csh
ldconfig

%preun
rm /etc/profile.d/eman2.sh
rm /etc/profile.d/eman2.csh


%changelog
* Thu Oct 22 2015 John Hover <jhover@bnl.gov>
- Initial build of 2.12. 