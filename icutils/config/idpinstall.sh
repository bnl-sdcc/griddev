#!/bin/bash
#
# Installs working Shibboleth IdP on RHEL6
# Apache 2.2, Tomcat 6, JDK 1.6, Kerberos via JAAS. 
#

SHIBVER=2.4.3
SHIBROOT=http://shibboleth.net/downloads/identity-provider
SHIBURL=$SHIBROOT/$SHIBVER/shibboleth-identityprovider-$SHIBVER-bin.tar.gz
DEPS="java-1.6.0-sun tomcat6 ant krb5-libs"
SHIBDIR=/usr/local/shibboleth-idp
SHIBHOST=`hostname -f`

INVOKE=$0
PROG=$(basename $0)
BINDIR=$(dirname $0)
DIRPATH=`dirname $INVOKE`
OLDDIR=$PWD
cd $DIRPATH
INVOKE_DIR=$PWD
cd $OLDDIR
SRCDIR=`dirname $INVOKE_DIR`


ensure_deps() {
	yum -y install $DEPS
}

do_install() {
	mkdir -p ~/src
	cd ~/src
	rm shibboleth-identityprovider-$SHIBVER-bin.tar.gz
	rm -rf shibboleth-identityprovider-$SHIBVER
	wget $SHIBURL
	tar xvzf shibboleth-identityprovider-$SHIBVER-bin.tar.gz
	cd shibboleth-identityprovider-$SHIBVER
	# Create install.properties
	echo "idp.home = $SHIBDIR" > src/installer/resources/install.properties
	echo "idp.hostname = $SHIBHOST" >> src/installer/resources/install.properties
	./install.sh
	cd -		
}





ensure_deps
do_install


