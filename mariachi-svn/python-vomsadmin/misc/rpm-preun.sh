RELEASE=0.2
CONFDIR=/etc/grid-security
PYVER=`python -V 2>&1 | cut --delimiter=' ' --fields=2 | cut --delimiter=. --fields=1,2`
NEWCONF=/usr/share/doc/python-vomsadmin-$RELEASE/python-vomsadmin.conf
VOMSAPP=/usr/lib/python${PYVER}/site-packages/vomsadmin/vomsutil.py


# Remove symlink to executable
rm -f /usr/sbin/vomsutil
