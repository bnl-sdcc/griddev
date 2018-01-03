#spec file for package mariachi-labview-daq
#
#
# Copyright  (c)  2007 Jonn R. Hover <jhover@bnl.gov>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to jhover@bnl.gov
#

Name:      mariachi-labview-daq
Summary:   All custom materials (libs, scripts, config) for MARIACHI data acquisition using Labview.
Version:   1.4
Release:   3
License:   GPL
Vendor:    MARIACHI Project http://www-mariachi.physics.sunysb.edu
Packager:  John R. Hover <jhover@bnl.gov>
Group:     Scientific/Engineering
Source0:   mariachi-labview-daq-1.4.tgz
BuildRoot: %{_tmppath}/mariachi-labview-daq-build
Requires:  labview82-core, labview82-rte, nicvirte, nikali, niorbi, nipali, nirpci, nivisa, nivisa-config, niwebpipeline20_dep, vnc, vnc-server, openmotif, altera-loader-c

%description
All custom materials (libs, scripts, config) for MARIACHI data acquisition using Labview.

%prep
%setup -q

%build


%install
rm -rf %\{buildroot]

install -d -o 0 -g 0 %{buildroot}/usr/lib/mariachi
cp -r lib/* %{buildroot}/usr/lib/mariachi

cp -r bin %{buildroot}/usr

install -d -o 0 -g 0 %{buildroot}/root/.vnc
cp dotvnc/* %{buildroot}/root/.vnc
chmod +x %{buildroot}/root/.vnc/xstartup
chmod go-rwx %{buildroot}/root/.vnc/passwd

install -d -o 0 -g 0 %{buildroot}/etc/sysconfig
cp etc/vncservers.mariachi %{buildroot}/etc/sysconfig


%clean
rm -rf %{buildroot}

%pre

%post
ln -s -f /usr/local/natinst/LabVIEW-8.2/labview /usr/local/bin/labview
chkconfig vncserver on
if [ -f /etc/sysconfig/vncservers ]; then
	mv /etc/sysconfig/vncservers /etc/sysconfig/vncservers.rpmsave
fi
cp -f /etc/sysconfig/vncservers.mariachi /etc/sysconfig/vncservers

%preun
rm -f /usr/local/bin/labview

%postun
if [ -f /etc/sysconfig/vncservers.rpmsave ] ; then
	mv /etc/sysconfig/vncservers.rpmsave /etc/sysconfig/vncservers
fi


%files
%defattr(755,root,root,-)
/usr/bin

%defattr(-,root,root,-)
/usr/lib/mariachi
/root/.vnc/passwd
/root/.vnc/xstartup

%defattr(644,root,root,-)
/etc/sysconfig/vncservers.mariachi



%changelog
* Fri Nov 02 2007 - vavilov (at) bnl.gov
- mariachi-loader.sh is added
- minor cleanups

* Fri Sep 14 2007 - jhover (at) bnl.gov
- Various cleanups. 
- Switch to mkrpm.

* Fri Mar 23 2007 - jhover (at) bnl.gov
- Initial RPM-ization
