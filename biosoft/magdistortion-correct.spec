Name: magdistortion-correct
Version:  1.4
Release:        1%{?dist}
Summary: Program for EM

Group:          Applications/Scientific
License:        GPL
URL:            http://www2.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page
Source0:        http://dev.racf.bnl.gov/dist/src/tgz/%{name}-%{version}.tar.bz2


#Requires:      jbigkit-libs

BuildRequires:  jbigkit-devel

%description
Image processing tool for EM.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
/usr/bin/*
/usr/include/relion-1.4
/usr/lib64/*



%doc

%changelog

* Tue Oct 20 2015 John Hover <jhover@bnl.gov>
- Initial build of 1.4.
~                                  