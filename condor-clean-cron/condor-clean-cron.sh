#!/bin/bash -l
#
#
#

count_gahp_fds() {
echo -n "GAHP File Descriptors: "
ps aux | grep gahp_server | grep -v grep | awk '{print $2}' | xargs lsof -p | wc -l	

}



print_info() {
echo "Condor: `condor_q | tail -n 1`"
NUNSUB=`condor_q -constraint 'GridJobStatus == "UNSUBMITTED"' | wc -l`
NPEND=`condor_q -constraint 'GridJobStatus == "PENDING"' | wc -l`
NSTGIN=`condor_q -constraint 'GridJobStatus == "STAGE_IN"' | wc -l`
NACT=`condor_q -constraint 'GridJobStatus == "ACTIVE"' | wc -l`
NSTGOUT=`condor_q -constraint 'GridJobStatus == "STAGE_OUT"' | wc -l`
NDONE=`condor_q -constraint 'GridJobStatus == "DONE"' | wc -l`
NSUSP=`condor_q -constraint 'GridJobStatus == "SUSPENDED"' | wc -l`
NUNK=`condor_q -constraint 'GridJobStatus == "UNKNOWN"' | wc -l`
NFAIL=`condor_q -constraint 'GridJobStatus == "FAILED"' | wc -l`
echo "Globus: UNSUB: $NUNSUB PEND: $NPEND STAGE_IN: $NSTGIN ACTIVE: $NACT STAGE_OUT: $NSTGOUT DONE: $NDONE SUSP: $NSUSP FAIL: $NFAIL UNKN: $NUNK"	
}

remove_unsubmitted() {
echo "Removing UNSUBMITTED jobs..."
echo "condor_rm -constraint GlobusStatus == 32"    
condor_rm -constraint 'GlobusStatus == 32'	
sleep 120	
condor_q | grep " X " | awk '{print $1}' | xargs condor_rm -forcex
sleep 60
}

remove_held() {
echo "Removing held jobs..."
condor_q | grep " H " | awk '{print $1}' | xargs condor_rm
sleep 120
condor_q | grep " X " | awk '{print $1}' | xargs condor_rm -forcex
sleep 60  
}

kill_gahp_server() {
echo "Killing all gahp_servers..."
ps aux | grep sbin/gahp_server | grep -v grep | awk '{print $2}' | xargs kill -9
	
}

echo "*******************************************"
DATE=`/bin/date`
echo "Begin: $DATE"
print_info
count_gahp_fds
#remove_unsubmitted
#remove_held
kill_gahp_server
sleep 60
print_info
count_gahp_fds
DATE=`/bin/date`
echo "Done: $DATE"
echo "*******************************************"