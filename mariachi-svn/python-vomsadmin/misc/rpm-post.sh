RELEASE=0.2
CONFDIR=/etc/grid-security
CONFFILE=python-vomsadmin.conf
PYVER=`python -V 2>&1 | cut --delimiter=' ' --fields=2 | cut --delimiter=. --fields=1,2`
NEWCONF=/usr/share/doc/python-vomsadmin-$RELEASE/python-vomsadmin.conf
VOMSAPP=/usr/lib/python$PYVER/site-packages/vomsadmin/vomsutil.py

#
# If conf file exists, do nothing. Else copy new conf to conf dir. 
#
if [ ! -f "$CONFDIR/$CONFFILE" ]; then 
	mkdir -p $CONFDIR
	cp $NEWCONF $CONFDIR
fi


# Set up executable utility
chmod ugo+rx $VOMSAPP
ln -s  $VOMSAPP /usr/sbin/vomsutil