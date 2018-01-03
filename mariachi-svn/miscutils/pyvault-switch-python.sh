#!/bin/bash
#
# Switches between pyvault python versions
#
#

go23() {
  cd /etc/alternatives/links
  rm -f \|usr\|bin\|python
  ln -s /usr/bin/python2.3 \|usr\|bin\|python
}

go24() {
  cd /etc/alternatives/links
  rm -f \|usr\|bin\|python
  ln -s /usr/bin/python2.4 \|usr\|bin\|python
}

case "$1" in
  24)
       go24 
        ;;
  23)
       go23
        ;;
  *)
        echo $"Usage: $prog {23|24}"
        exit 1
esac

exit $?

