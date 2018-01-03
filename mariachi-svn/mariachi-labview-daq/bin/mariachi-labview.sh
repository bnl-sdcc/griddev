#!/bin/bash
LOGFILE=/var/log/mariachi-daq.log
d=`date`
echo "Mariachi Labview Initialization..." >> $LOGFILE 

echo "Loading FPGA program" >> $LOGFILE 
alterald -v /usr/lib/mariachi/altera/mariachi.RBF >> $LOGFILE 

echo "Executing LabView ..." >> $LOGFILE 
cd /usr/lib/mariachi
labview Data_logger.vi >> $LOGFILE  & 

echo "Initialization Successful: $d" >> $LOGFILE 