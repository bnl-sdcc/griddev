This is an automated efficiency curve measurement system. It's based on the computer controled power supply KEPCO ABC 60-2DM, KEPCO supplied LabView library to control it and improved (soon be standard) version of Lab DAQ system (with a measurement table).

The system was originally developed on mc02 computer in Desktop\Mariachi DAQ\Devel directory.

SOFTWARE INSTALLATION/CONFIGURATION
-----------------------------------

I set a NI GPIB card, downloaded its 286MB driver from NI (ni488225.exe, now unpacked to C:\National Instruments Downloads\NI-488.2) and pointed New Hardware Wizard to the above directory. It found and installed the driver successfully. kpabc.LLB (from kpabcv.zip) from KEPCO was put in C:\Program Files\...\LabView\instr.lib. The corresponding Menu showed up automatically in LabView.

FILES
-----

Kepco_Control.vi - General interface, part of kpabc.LLB, saved as a separate VI for convinience.
Eff_Meas.vi      - Main VI to conduct the measurement
DAQv2.vi	 - DAQ program (started by Eff_Meas.vi). Ideally you don't want to touch any controls in its
		   window

HOW IT WORKS
------------
You set Start Voltage, Step, Number of Points and time to conduct a measurement in the Control Panel of Eff_Meas.vi. Also for bookkeeping purposes you want to put a detector ID in the corresponding control. You start the VI, it sets the voltage and open DAQv2 VI which performs the measurement, put results to a table in its Front Panel and in the same time writes them down to a file named in the Control Panel. The content of the file is always identical to the content of the table. You can see the curent voltage readings in Eff_Meas VI Control Panel.

FUTURE IMPROVEMENTS
-------------------
1) Add the file name control to Eff_Meas Front Panel
2) Show the progress of efficiency curve measurement in the embeded graphical window


DV. Sep 1, 2007.
