#!/bin/bash
echo "wrapper..."
newstr=""
for arg in "$@" ; do
	echo \"$arg\"
	newstr="$newstr \"$arg\""
done	
echo "newstring: $newstr"

echo ./quotescript.sh $newstr
eval ./quotescript.sh $newstr
