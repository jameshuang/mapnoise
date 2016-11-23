
MapNoise is a utility to present flight path data files. It currently focuses on flights in the silicon valley sky. 

Each data file must be in a CSV format as showcased by the sample data files under directory sample-data. Flightradar24.com serves such data files.

INSTALL
=======

Download the zip files under subdirectory 'releases'. Unzip it, then in a cmd shell, cd into the directory, run:

.\mapnoise -d \<your data directory\> -m \<month\> -a \<altitude\>

e.g. .\mapnoise -d sample-data -m 2016-10

The command above should produce a plot similar to the sample plot file (sample-plot-2016-10.png).

If you do not specify altitude argument in the command line, then it will present each flight's whole path.

Your data directory should be organized into subdirectories like 2015-11 for Nov 2015 flight data files, 2015-12 for Dec 2015 flight data files and so on.


