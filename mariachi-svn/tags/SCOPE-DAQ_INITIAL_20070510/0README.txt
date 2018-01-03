Some of the files below could be moved to an Achive.
----------------------------------------------------

VIs
===

daq-v00.vi	-first working VI based on the example and directly using examples subVIs
		(and that is why not working properly: cann't wait for a trigger)
daq-b1v0.vi	-first fully functional VI (waiting for a trigger, stopping at stop button push?)
daq-b1v1.vi	-final version with fixed output file name
daq-b1v2.vi	-(current on Apr 18, 07) final VI with a file name depending on date
daq-scope.vi    -renamed daq-b1v2.vi which subsecquently doesn't exist anymore.


daq-read-vX.vi	-a line of all-in-one reading routines, that read a data file. Dead end.
daq-read.vi	-a top of the above line, handles small pulses, Uses dv-wf-fit, dv-wf-int,
		but not dv-wf-meas*. Basically dv-wf-meas* used in daq-convert2meas.vi
		were cut&paste from this VI.

---------------------------------------------------------------------------------------------

Read-MWF.vi	-developed example WF reading VI. Now it can wait for a trigger (obsolete, 
		replaced by dv-read-mwf.vi now)
dv-read-mwf.vi  - timout setting node is taken out of the loop to solve the problem of a 
		  ~1sec delay before the next readout starts. I didn't help.

daq-globals.vi	-keeps a global variable. Used with aqcuision VIs (daq-b1*.vi)

dv-wf-int.vi
dv-wf-fit.vi	-wrap around array intergration and fitting routines to be appliable to
		 WFs and to treat errors the same way as WF subVIs.

dv-wf-meas.vi
dv-wf-measN.vi	-5 measurements subVIs used in daq-convert2meas.vi (dv-wf-meas.vi, which processes
		one WF at a time). dv-wf-measN.vi processes a bunch of WFs and outputs arrays
		of measurements, probably not so useful.

-----------------------------------------------------------------------------------------------

daq-read-file.vi - standalone simple VI reading and displaying WFs with simplified measurements
		   (by oreder of MM)

daq-conv2meas-v00.vi - convert a data file to a measurement file, i.e. the ascii file with 
			4channelsX5measurements=20 values per line. It's the basic version.
		        Further development will include: adding timestamps, reading both
			formats (lvm, tdms) without recompiling and maybe saving somehow
			reduced WFs themselfs.

daq-conv2meas.vi     - current/development version of the above VI.

daq-sim.vi	-intended to simulate daq by reading and displaying prerecorded events in a fixed
		 intervals of time. Based on daq-read-file.vi

Data
====

wfdata.old{2,3}.lvm - first trails to acquire data. old2 is kept only because its small size
		otherwise data are duplicated there. old3 might keep good data, but it's
		somehow broken (perhaps contain one or more "empty" WFs).


wfdata-0{1-5}.{tdms,lvm}   - supposed to be good data. 04 is broken (cann't be read till the end)
Between 2-3 I put base lines of all channels in oscilloscope to +150mV, before base lines were
spread vertically and the lowest channel 4 sometime was cut the top of the pulse (at ~-200mV).
Somehow 2 has duplicated events (check in other files!).

wfdata-200704XX.{tdms,lvm} -supporst to be good data.

wfdata-spec-20070417.tdms is a spec.file where detectors connected to the osc. were
			   2 1 4 5 (vs 2 3 4 5 - usual connection)

wfdata-*.txt 	arec corresponding measurement files (produced by daq-convert2meas.vi)

See more on data in Notes. Shortly data starting with wfdata-20070420-2 is good.

Notes
=====

1:53 PM 4/30/2007
Live Data from Stony Brook Site

Four oscillograms represent recent signals from detectors in four different corners of a lab at the D foor of Physics bulding at SUNY. Oscilloscope is triggered by a conincidence board which detects tree- and four- fold coincidences between the signals. The top plot shows all signals together, the bottom four ones show the signals separately. Scales in the top and bottom plots are different.

11:27 AM 4/29/2007
setting of timeout is out of cycle now, timeout itself is still 5sec. I stoped the asquision for
3-4 minutes, renamed files to *-1.*, replaced the call to the fixed version of the subVI 
(dv-read-mwf.vi). Aqsquision started again at ~11:28am.

TO FIX: when stopped by a stoped button and exited by a timeout, the same event is written
twice!

11:06 AM 4/29/2007

Discovery was made that 5sec time out cycle seems to cause a 7sec structure in "Delta t"
distribution (time diff. between sequencial triggers). Extra 2 sec is probably needed to 
set the timeout again (turned to be inside the cycle in the code). That should introduce dead 
time because the osc. is armed all the time, just it is read later when an event happens
at the end of timeout and before the next attempt to read the osc...

I'm goint to get the timout setting call out of the cycle and increase the timeout to 
probably 30sec or more.

10:50 AM 4/20/2007

I found that after having wfdata-spec-20070417.tdms written I connected detectors back wrong:
3145 instead of 2345. They are the rest of the file wfdata-20070417 (the begginning is 
normal connection), wfdata-2007{18,19,20}. I'm going to rename 20 so the rest of data on Apr 20
will be in nomral format!

Start writing wfdata-ch12-20070420 (same connections as for wfdata-spec-20070417) but triggered
by output 3 of the board (doulbe conincidences). Statistics on two channels 1 and 2 is now
collected much faster (16.5/min).

!It ended up by writting only ~4/min. Likely it's a disk seek problem. The size of the file
got to >300Mb. Next time will write to multiple files.


