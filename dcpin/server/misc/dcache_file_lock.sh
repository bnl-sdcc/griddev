#!/bin/bash

old_filename=$1
current_time=`date +%s`
expired_files=$1.expired
number_days_to_keep=90
owner=xin

# before doing anything, save a copy of the original table file
cp $1 $1.orig

# construct the "original" lock_files_table

# firstly get rid of the comment lines
# can't redirect the output of grep to the file with the same name,
# somehow it will be corrupted
cat ${old_filename} | grep -v "#" > ${old_filename}.tmp 
mv ${old_filename}.tmp ${old_filename}

rm -rf new_file
grep LOCKED ${old_filename} >/dev/null 2>&1
if [ $? -ne 0 ]; then # this is a rough input file, need to convert it to a "table" format  
   new_filename=$1_table
   rm -rf new_file
   touch new_file
   while read line1
   do
  	if [ "X$line1" != "X" ]; then
     	   echo "$line1 & ${current_time} & ${number_days_to_keep} & $owner & NOTLOCKED & UNKNOWN & UNKNOWN">>new_file
  	fi
   done < ${old_filename}
else 
   cat ${old_filename} > new_file
   new_filename=${old_filename}
fi

# try to lock each of the files in this table

#lockfiles=(`cat new_file | awk -F"&" '{print $1}'`)
#for thisfile in ${lockfiles[@]}; do

echo "# file names  & lock_time(in seconds starting from 1970)  & lock_length (in days) & owner & status (locked or not) & poolnode & pnfsid" > ${new_filename}_tmp   # this is a tmp file that keeps the updated records of the locking process
                       # and will be copied to the ${new_filename} at the end

#cat new_file

touch ${expired_files}

while read line2
do

    col1=`echo $line2 | awk -F"&" '{print $1}'`
    col2=`echo $line2 | awk -F"&" '{print $2}'`
    col3=`echo $line2 | awk -F"&" '{print $3}'`
    col4=`echo $line2 | awk -F"&" '{print $4}'`
    col5=`echo $line2 | awk -F"&" '{print $5}'`
    col6=`echo $line2 | awk -F"&" '{print $6}'`
    col7=`echo $line2 | awk -F"&" '{print $7}'`	

    # some initial judgement on what needs to be done on this file
    thisfile=`echo $line2 | awk -F"&" '{print $1}'`
    #echo "This lock file is " $thisfile

    lock=0 # tag for locking or unlocking, =0 means to lock, =1 means to unlock
    expire=0 # tag for expiring files, =0 means not expired, =1 means expired    

    # firstly get rid of the expired files
    in_time=`echo $line2 | awk -F"&" '{print $2}'`
    lifetime1=`echo $line2 | awk -F"&" '{print $3}'` # in days
    lifetime=`echo "$lifetime1*24*3600" | bc` # in seconds
    let "age = `date +%s` - ${in_time} "
    if [ $age -ge $lifetime ]; then
       expire=1 # expired
    fi

    echo $line2 | awk -F"&" '{print $5}' | grep NOTLOCKED >/dev/null 2>&1
    if [ $? -ne 0 ]; then # already locked
       if [ $expire -eq 1 ]; then
          lock=1 # mark it for to-be-unlocked
       else # not expired file but already locked
          echo $line2 >> ${new_filename}_tmp
          continue
       fi
    else # not locked files
       if [ $expire -eq 1 ]; then
          echo $line2 >> ${expired_files} # move the record to the expired files table
          continue
       else # not locked and not expired
          lock=0 # mark it for to-be-locked
       fi
    fi

    # now do the unlock firstly since it's easy
    if [ $lock -eq 1 ]; then
	# here I use a specifically named key "dcache-script-admin-key" in order for the 
        # refresh_dcache_ssh_process script to catch the specific ssh process, w/o interrupting
        # other users' interactive ssh session
        ssh -l admin -i ~xinzhao/dcache_tools/dcache-script-admin-key -c blowfish -p 22223 dcache01.usatlas.bnl.gov >unlock.log 2>&1 <<EOF
        set unsticky $thisfile
        logoff
EOF
        cat unlock.log | col -b > unlock.log
        cat unlock.log | grep " ok " >/dev/null 2>&1
        if [ $? -eq 0 ]; then # unlock succeeded
           echo $line2 >> ${expired_files} # move the record to the expired files table
           continue
        else # failed to unlock it, do nothing, leave it in the table, so next time it will be re-tried
           echo $line2 >> ${new_filename}_tmp
           continue
        fi
    fi

    # now it's time to lock the unexpired files
    cached=1 # tag if the file is cached in any pools or not
    checknum=0 # count the number of pool-search re-tries
    while [ $checknum -lt 3 -a $cached -eq 1 ]; do  
 		# give it three chances since sometimes Pnfs Server might be busy and can't return
                # results immediately
        echo "checknum is $checknum"
        checknum=$(( checknum + 1 ))	
        sleep 2
        # check which pools this file is in
        ssh -l admin -i ~xinzhao/dcache_tools/dcache-script-admin-key -c blowfish -p 22223 dcache01.usatlas.bnl.gov >poolname 2>&1 <<EOF
	cd PnfsManager
	cacheinfoof $thisfile
	pnfsidof $thisfile
	..
	logoff
EOF

        # this is to remove the CTRL-M character in the file
        cat poolname | col -b > poolname
	
        # now try to find the pool to use
        # the machnism is to remove the write pools, then randomly select one readpool from the list
        # the following many greps is to make sure the acasXXX is a real poolname, nothing else
        poollist=(`fgrep -B 1 "PnfsManager" poolname | grep -v PnfsManager | grep -v admin | grep acas`)
        #echo "poollist is " ${poollist[@]}
        # check if there is pool that holds this file
        if [ ${#poollist[@]} -eq 0 ]; then
	   cached=1 # no pool that holds this file
	   #echo "No pool holds this file, go to the next" 
           #cat poolname
	   #   continue
        else
	   cached=0 # there are pools that hold this file
        fi
    done
		 
    if [ $cached -eq 1 ]; then
	echo "No pool holds this file, go to the next"
	echo $line2 >> ${new_filename}_tmp
	continue
    fi	 

    # get the pnfsid (pnfsid is the first element of the following array)
    pnfs_id=`fgrep -B 1 ".." poolname | grep -v Pnfs`

    count=-1
    newpoollist=()	
    for thispool in ${poollist[@]}; do
	pool=`echo $thispool | grep acas`
	if [ "X$pool" != "X" ]; then # a valid pool name
	   pool_prefix=`echo $pool | awk -F"_" '{print $1}'`	
	   #exclude the write pools
	   if [ "${pool_prefix}" != "dcwr01" -a "${pool_prefix}" != "dcwr02" -a "${pool_prefix}" != "dcwr03" -a "${pool_prefix}" != "dcwr04" -a "${pool_prefix}" != "dcwr05" -a "${pool_prefix}" != "dcwr06" -a "${pool_prefix}" != "dcwr07" -a "${pool_prefix}" != "dcwr08" ]; then 
		count=$(( count + 1 ))
		newpoollist[$count]=$pool
	   fi
	fi
    done

    # break out if no readpool is selected
    if [ $count -eq -1 ]; then 
	echo "This file is not available in read pools"
	continue
    fi  
 
    # randomly choose one pool from this list in the range of (count+1) elements
    rannum=$RANDOM
    let "rannum %= $((count+1))"

    # now it's time to lock the file
    echo "The pool is ${newpoollist[$rannum]}"
    echo "and the pnfsid is ${pnfs_id}"
    echo ""

    ssh -l admin -i ~xinzhao/dcache_tools/dcache-script-admin-key -c blowfish -p 22223 dcache01.usatlas.bnl.gov >poolname2 2>&1 <<EOF
	cd ${newpoollist[$rannum]}
	rep set sticky ${pnfs_id} on
	..
	logoff
EOF

    # update the records of the table file
     echo "$col1 & $col2 & $col3 & $col4 & LOCKED & ${newpoollist[$rannum]} & ${pnfs_id}" >> ${new_filename}_tmp	
#    echo $line2 | sed 's/NOTLOCKED/LOCKED/g' >> ${new_filename}_tmp     
done < new_file

cat ${new_filename}_tmp | grep -v "#" > this_tmp_test
if [ -s this_tmp_test ]; then # good new table file
   # ls -lrt ${new_filename}_tmp
   mv ${new_filename}_tmp ${new_filename}
else
   echo "This lock operation appears to fail, please try again later"
   cp $1.orig $1
   rm -rf ${new_filename}_tmp
fi

#clean up
rm -rf this_tmp_test new_file poolname poolname2 unlock.log
