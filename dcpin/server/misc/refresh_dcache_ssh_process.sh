#!/bin/bash

# this script is to run continuously, and check the dcache admin shell
# ssh process from this client machine. It will kill the ssh command
# if it times out (2 minute), so that the dcache_lock_file and other 
# processes can proceed.

# it can monitor multiple dcache admin shell ssh processes simultaneously
# but the ssh sessions have to use the dcache-script-admin-key key, which 
# is the key word in the "grep" command for this script 

wait_time()
{
   timelimit=30 # 1 minutes, see the sleep 2 command below
   count=0
   while :
   do 
      sleep 2
      # search for this pid
      ps -auxwww | grep xinzhao | grep blowfish | grep dcache-script-admin-key | grep $1 >/dev/null 2>&1
      if [ $? -ne 0 ]; then # no that pid found, which means the ssh session is already finished
         break
      else # there is the pid 
	 if [ $count -ge $timelimit ]; then # time out this pid
            kill $1
            echo "killed this dcache ssh process $1 at `date`"
            break
	 else
	    count=$(( count + 1 ))
         fi
      fi
   done

#   echo "exit wait_time for pid $1"
}

refreshlog=refresh_dcache_ssh_process.log

while :
do
	# initialize the array
	jobpid=()
        # sleep 10 seconds before checking the process
	sleep 10
	ps -auxwww | grep xinzhao | grep blowfish | grep -v grep > $refreshlog 2>&1
        jobpid=(`cat $refreshlog | awk -F" " '{print $2}'`)
        if [ ${#jobpid[@]} -eq 0 ]; then # no pid found
           continue
        else # there are pids
	   for thispid in ${jobpid[@]}; do
		wait_time $thispid
	   done
        fi
done



