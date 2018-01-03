#
# ./configure $mpi_option $float_option prefix=$PREFIX CPPFLAGS="-I$PREFIX/include $fltk_cxx"  LDFLAGS="-L$PREFIX/lib $fltk_ld"
#
Name: relion
Version:  1.4
Release:        4%{?dist}
Summary: Program for EM

Group:          Applications/Scientific
License:        GPL
URL:            http://www2.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page
Source0:        http://dev.racf.bnl.gov/dist/src/tgz/%{name}-%{version}.tar.bz2


Requires:      fftw-libs-double
Requires:      openmpi
Requires:      environment-modules
Requires:      fltk

BuildRequires:  openmpi-devel
BuildRequires:  fftw-devel
BuildRequires:  fltk-devel

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot

AutoReqProv: no


##   fltk configure 
#export CXXFLAGS=`/usr/bin/fltk-config --cxxflags`
#export LDFLAGS=`/usr/bin/fltk-config --ldflags`

%description
Image processing tool for EM.

%prep
%setup -q

%build
export LDFLAGS=`/usr/bin/fltk-config --ldflags`
export CXXFLAGS=`/usr/bin/fltk-config --cxxflags`
export HAVE_MPI=true
export HAVE_FLTK=true
./configure --enable-mpi --prefix=/usr CPPFLAGS="-I/usr/include -I/usr/include/freetype2 -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_THREAD_SAFE -D_REENTRANT"  LDFLAGS="-L/usr/lib -Wl,-z,relro -lfltk "
make 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install DESTDIR=%{buildroot} 
mkdir -p %{buildroot}/etc/ld.so.conf.d/
echo /usr/lib64/openmpi/lib >  %{buildroot}/etc/ld.so.conf.d/openmpi.conf 


%files
/usr/bin/*
/usr/include/relion-1.4
/usr/lib/*
/etc/ld.so.conf.d/*


%doc

%post
/usr/sbin/ldconfig



%changelog

* Tue Oct 20 2015 John Hover <jhover@bnl.gov>
- Initial build of 1.4.
~                                  