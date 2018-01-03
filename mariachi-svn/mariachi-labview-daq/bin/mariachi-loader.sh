#!/bin/bash
d=`date`

echo "$d Loading FPGA program" 
alterald -v /usr/lib/mariachi/altera/mariachi.RBF
