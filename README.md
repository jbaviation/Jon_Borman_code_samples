# Jon Borman Code Samples
The following files are coding samples that were created throughout my academic and
professional career.  All code was generated and maintained by me.

### Convert_Files
This program is run in Matlab and utilizes a self created Java Archive file in order to 
convert NASA data system (Escort) files into Matlab code.  The purpose is to allow for easy
verification of programmed calculations before deployment into facility data system.

### DA40_Performance_Calcs.m
This is a simple script to evaluate and visualize the coefficient of lift vs coefficient of 
drag in a Diamond DA40.  This file was generated while taking a aircraft performance course 
out of personal interest in performance aspects of an airplane that I've flown.

### Potential_Flow_Solver.m
This script was created for an assignment for a Computational Fluid Dynamics (CFD) course
in graduate school.  It is used to calculate the 2D coefficient of pressure field of an 
incompressible, laminar, and steady fluid flow about a circular cylinder.

### REFPROP_STPROPS.for
A Fortran function that was created as a generic means to calculate air properties at a 
location downstream from a measurement.  This code utilizes the NIST REFPROP tables to correct
measurements humidity.

### VCONEFLOW.for
A Fortran function for calculation of airflow rate across a calibrated v-cone based on an
ISO standard and corrected for humidity.

### Humidity_Cart
A Python program that was created as a means to validate data measured from a hygrometer by
comparing it with a humidity generator.  Components of this program include:
 - reading, deducing and streaming data from an Analog to Digital (AtoD) USB device
 - transform thermocouple voltages into engineering units
 - allow for creation of a data record for postprocessing
 - convert between various units and humidity properties during runtime
 - GUIs were created for ease of use and visualization (NOTE: this was my first attempt at GUIs
   and admit they are a bit rudimentary but very functional)
