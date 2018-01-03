#!/bin/bash
# Flexible script to build RPM as unprivileged user from arbitrary location. 
#

###########################################################################
# User settable variables
###########################################################################
DEBUG=0
NAME=mariachi-daq-tunnel
VER=0.3


##############################################################################
# Shouldn't need to be adjusted
##############################################################################

ARGS=""
for arg ; do
	if [ $DEBUG -eq 1 ] ; then 
		echo "[DEBUG] gums: Arg is $arg"
		echo "[DEBUG] gums: ARGS are: $ARGS"
	fi
	case $arg in
		--debug)
		DEBUG=1
		;;

		*)
		echo "Builds RPMS of this project."
		echo "Usage: $0 [--debug]."
		exit 0
		;;
	esac
done

RELEASE=$NAME-$VER
INVOKE=$0
PROG=$(basename $0)
BINDIR=$(dirname $0)
DIRPATH=`dirname $INVOKE`
OLDDIR=$PWD
cd $DIRPATH
PROJECTDIR=$PWD
cd $OLDDIR
TMPDIR=`mktemp -d`
TARFILE=$RELEASE.tgz

mkdir -p $TMPDIR/build
BUILDDIR=$TMPDIR/build

DISTDIR=$PROJECTDIR/dist
mkdir -p $PROJECTDIR/dist

#
# Set up Redhat RPM dirs
#

RPMBUILDDIR=$BUILDDIR/RPM
mkdir -p $RPMBUILDDIR
mkdir -p $RPMBUILDDIR/tmp
mkdir -p $RPMBUILDDIR/BUILD
mkdir -p $RPMBUILDDIR/RPMS/athlon
mkdir -p $RPMBUILDDIR/RPMS/i386
mkdir -p $RPMBUILDDIR/RPMS/i486
mkdir -p $RPMBUILDDIR/RPMS/i586
mkdir -p $RPMBUILDDIR/RPMS/i686
mkdir -p $RPMBUILDDIR/RPMS/noarch
mkdir -p $RPMBUILDDIR/SOURCES	
mkdir -p $RPMBUILDDIR/SPECS
mkdir -p $RPMBUILDDIR/SRPMS		


RPMMAC=$TMPDIR/rpmmacros
echo "%packager       $USER" 							>> $RPMMAC
echo "%distribution   Redhat EL"  						>> $RPMMAC
echo "%vendor         BNL"								>> $RPMMAC
echo "%_signature     gpg"  							>> $RPMMAC
echo "%_gpg_name      $USER"  							>> $RPMMAC
echo "%_topdir        $RPMBUILDDIR"  					>> $RPMMAC
echo "%_tmppath       %{_topdir}/tmp"			  		>> $RPMMAC
echo "%_builddir      %{_topdir}/BUILD"  				>> $RPMMAC
echo "%_rpmtopdir     %{_topdir}"		  				>> $RPMMAC
echo "%_sourcedir     %{_topdir}/SOURCES"  				>> $RPMMAC
echo "%_specdir       %{_topdir}/SPECS"  				>> $RPMMAC
echo "%_rpmdir        %{_topdir}/RPMS"  				>> $RPMMAC
echo "%_srcrpmdir     %{_topdir}/SRPMS"  				>> $RPMMAC
echo "%_rpmfilename   %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" >> $RPMMAC


if [ $DEBUG -eq 1 ] ; then 

	echo DIRPATH = $DIRPATH
	echo PROJECTDIR = $PROJECTDIR
	echo TMPDIR =  $TMPDIR
	echo TARFILE = $TARFILE
	echo DISTDIR = $DISTDIR
	echo BUILDDIR = $BUILDDIR
	echo RPMBUILDDIR = $RPMBUILDDIR
	echo RPMMAC = $RPMMAC

fi

#
# Create distribution tarball for SOURCES
#
mkdir $TMPDIR/$RELEASE
cp -r $PROJECTDIR/* $TMPDIR/$RELEASE

ORIGDIR=$PWD
cd $TMPDIR
if [ $DEBUG -eq 1 ] ; then
	echo "tar  -cvzf $TARFILE --exclude .svn $RELEASE" 
fi
if [ $DEBUG -eq 1 ] ; then
	tar  -cvzf $TARFILE --exclude .svn --exclude dist $RELEASE 
else
	tar  -czf $TARFILE --exclude .svn --exclude dist $RELEASE 
fi


if [ $DEBUG -eq 1 ] ; then
	echo "cp $TARFILE $RPMBUILDDIR/SOURCES/"
fi
cp $TARFILE $RPMBUILDDIR/SOURCES/
cp $TARFILE $DISTDIR
cd $ORIGDIR
cp $PROJECTDIR/$NAME.spec $RPMBUILDDIR/SPECS/

#
# Replace user's rpmmacros file, run build
#
if [ -f "~/.rpmmacros" ]; then
	mv ~/.rpmmacros ~/.rpmmacros.bak
fi
cp $RPMMAC ~/.rpmmacros

if [ $DEBUG -eq 1 ] ; then 
	echo "rpmbuild -ba $RPMBUILDDIR/SPECS/$NAME.spec"
	rpmbuild -ba $RPMBUILDDIR/SPECS/$NAME.spec
else
	rpmbuild -ba $RPMBUILDDIR/SPECS/$NAME.spec > /dev/null 2>&1
fi

rm -f ~/.rpmmacros
if [ -f "~/.rpmmacros.bak" ]; then
	mv ~/.rpmmacros.bak ~/.rpmmacros
fi

#
# Copy tarball and rpms to project dist
#
for rpm in `find $RPMBUILDDIR -name *.rpm`; do
	if [ $DEBUG -eq 1 ] ; then
		mv -v $rpm $DISTDIR
	else
		mv $rpm $DISTDIR
	fi
done

# If not debug, remove all temp areas
if [ $DEBUG -eq 1 ] ; then 
	echo "Done."
else
	echo "Done. Erasing temporary directories."
	rm -rf $TMPDIR

fi
