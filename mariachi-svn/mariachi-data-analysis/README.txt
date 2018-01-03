Mariachi Data Analysis
======================

This project contains code and libraries needed to select, transform, merge, 
and analyze various types of MARIACHI data. 



Radio/SD Correlation Analysis
-----------------------------
Pipeline:
1) Pull all SD data from sites for given interval (1 hour? 1 day?)
Use web interface to do this. 

2) Select 5-fold events only. Merge from all sites. Order by time. 

3) For each 5-fold, pull slice from .WAV Radio files for +/- X seconds  ( 1 second?)

4) Process slice for time of largest peak(s). Write these times to file. 

5) Create histogram of all 5-folds with any associated radio peaks plotted into .05 second bins.

 