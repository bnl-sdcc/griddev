#!/bin/bash
#USER_DATA=/home/jhover/devel/mariachi-wn-config/share/users.data.txt
USER_DATA=/usr/share/mariachi-wn-config/users.data.txt
DEBUG=0

# Reset IFS to colon in order to deal with DNs and Names
IFS=:

handle_file_add() {
	while read USER ID HOME COMMENT; do
		if [ $DEBUG = 1 ]; then
		echo "USER is $USER"
		echo "ID is $ID"
		echo "HOME is $HOME"
		echo "COMMENT is $COMMENT"
		fi
		if [ `id -u` = 0 ]; then
			groupadd -g $ID $USER
			useradd -u $ID -g $USER -d $HOME -c $COMMENT $USER
		fi	
	done
}

handle_file_remove() {
	while read USER ID HOME COMMENT; do
		if [ $DEBUG = 1 ]; then
		echo "USER is $USER"
		echo "ID is $ID"
		echo "HOME is $HOME"
		echo "COMMENT is $COMMENT"
		fi
		if [ `id -u` = 0 ]; then
			userdel $USER
		fi	
	done
}



case $1 in
		--add)
		if [ -r $USER_DATA ]; then
			handle_file_add < $USER_DATA
		fi		
		
		;;
		
		--remove)
		if [ -r $USER_DATA ]; then
			handle_file_remove < $USER_DATA
		fi
		
		;;
		
		*)
		echo "Configures Mariachi Users."
		echo "Usage: $0 [--add|--remove]."
		exit 0
		;;
	esac


