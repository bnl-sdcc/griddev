#!/bin/sh

echo ""
echo "CPU usage at BNL condor cluster at `date -Is`"
echo ""

echo ""
echo "Overall condor status : `condor_q | tail -1`"
echo ""

echo "                       Total Owner Claimed Unclaimed Matched Preempting Backfill"
echo "BNL_ATLAS_1 (prod) " 
condor_status -constraint 'Turn_Off == False && CPU_Type == "prod"' | tail -1
echo "ANALY_BNL_ATLAS_1 (short) "
condor_status -constraint 'Turn_Off == False && CPU_Type == "short"' | tail -1
echo "ANALY_LONG_BNL_ATLAS (long) " 
condor_status -constraint 'Turn_Off == False && CPU_Type == "long"' | tail -1
echo "BNL_ATLAS_2 (prodtest) " 
condor_status -constraint 'Turn_Off == False && CPU_Type == "prodtest"' | tail -1
echo "BNL_ATLAS_DDM (dq2test) " 
condor_status -constraint 'Turn_Off == False && CPU_Type == "dq2test"' | tail -1
echo "ANALY_LONG_BNL_LOCAL/ANALY_BNL_LOCAL (bnl-local) " 
condor_status -constraint 'Turn_Off == False && CPU_Type == "bnl-local"' | tail -1
#echo "OSG ITB queue (osgitb) " 
#condor_status -constraint 'Turn_Off == False && CPU_Type == "osgitb"' | tail -1

