This is a translation of an Kylix altera loader program to C. The idea
was also to get rid of X-windows interface. 

Original Pascal code can be found on Morph-IC software CD (?) or after
sowfware installation in C:\Program Files\Morphic_1K\Linux Examples\Morphic_kylix.tar.gz
(*.pas files).

Compilation: just "make" should work.

Usage: alterald [-vh]   [file.rbf]     [interface]
		      MariachiV2.rbf "Morphic-IC A"

The program opens a proper interface by its name "Morphic-IC A", so
that if a few boards are attached to a computer it programs a "first"
one. This can be changed, of course, in the code, e.g. by 
openning a device by its unique serial number.

DV. Aug 10, 2007.
