ESM1.6 restart files contain copies of complete model states, allowing for experiments to be stopped and restarted at a later time. This page outlines their structure and details basic procedures for manipulating them.


## Structure of the ESM1.6 restart directory

An ESM1.6 restart directory contains separate restart files for each component. These are are organised into the following directories:
```
atmosphere  coupler  ice  ocean  README
```

### Atmosphere
The atmosphere restart directory contains the following files
```
restart_dump.astart  um.res.yaml
```
`restart_dump.astart` is the main UM restart file, containing the atmospheric state in addition to static boundary information such as the land-sea mask, vegetation maps and orography.

`um.res.yaml` is a separate calendar file which holds the date and time associated with the restart. Information in this file is copied by `payu` into the model namelist files at runtime.


### Ocean
The ocean restart files are organised into seperate groups of variables:
```
ocean_age.res.nc  ocean_density.res.nc  ...  ocean_solo.res
```

The netCDF files contain snapshots of the model state while `ocean_solo.res` is a text file specifying the model date and time.

### Ice

The ice restart directory contains the following files:

```
cice_in.nml  iced.2145-01-01-00000.nc  ice.restart_file  mice.nc
```

The `iced.YYYY-MM-DD-00000.nc` holds the model state and also carries the date and time in the global attributes. `ice.restart_file` is 
a pointer file used by CICE when finding the correct restart file to read. `mice.nc` contains ice coupling data to be sent to the ocean model
at the beginning of the next run.

### Coupler
The coupler restart directory contains data sent from each component at the termination of the previous run, allowing for the submodels to access the required boundary conditions at the beginning of the next run.

```
a2i.nc  i2a.nc  o2i.nc
```



## Common restart manipulations

### Changing the date of a restart file

It's commonly required to change the date for a restart file. For example when setting up a historical experiment, a restart might be taken from a pre-industrial simulation and the date changed to 1850.

The following instructions outline how to modify the date for each component. It's important to apply the updates to all components consistently, as inconsistencies in the model dates can cause crashes.

#### Atmosphere:
Navigate to the `restart/atmosphere` directory:

<terminal-window static>
<terminal-line>module use /g/data/xp65/public/modules</terminal-line>
<terminal-line>module load conda/analysis3</terminal-line>
<terminal-line><span style='color:#009933'>&#35 Update the date in the UM dump file</span></terminal-line>
<terminal-line>python ~access/apps/pythonlib/umfile_utils/access_cm2/change_dump_date.py restart_dump.astart  <<< <span style='color:red'>"YYYY MM DD",</span></terminal-line>
<terminal-line><span style='color:#009933'># Update the date in the calendar file</span></terminal-line>
<terminal-line>sed -i "s/end_date:.*/end_date: <span style='color:red'>YYYY-MM-DD</span> 00:00:00/" <new-restart-path>/atmosphere/um.res.yaml</terminal-line>
</terminal-window>

#### Ocean:
In the `restart/ocean` directory, edit `ocean_solo.res`:

```
     3        (Calendar: no_calendar=0, thirty_day_months=1, julian=2, gregorian=3, noleap=4)
     1     1     1     0     0     0        Model start time:   year, month, day, hour, minute, second
  2145     1     1     0     0     0        Current model time: year, month, day, hour, minute, second
```

Replace the date in the 3rd line, taking care to preserve the column alignment. The entries should not be zero-padded.

#### Ice:
In the `restart/ice` directory:

Rename the `iced.YYYY-MM-DD-00000.nc` with new date. The year, month, and day should be zero padded. 

Edit the `ice.restart` pointer file to use the new file name:
<terminal-window static>
<terminal-line>echo ./RESTART/iced.YYYY-MM-DD-00000.nc   >  ice.restart_file</terminal-line>
</terminal-window>

Replace the `year`, `nyr`, `month`, and `mday` global attributes using `nco` (in most cases, only the year will need to be changed):
<terminal-window static>
<terminal-line>module load nco</terminal-line>
<terminal-line>ncatted -O -a year,global,o,l,<span style="color:red">YYYY</span> iced.YYYY-MM-DD-00000.nc</terminal-line>
<terminal-line>ncatted -O -a nyr,global,o,l,<span style="color:red">YYYY</span> iced.YYYY-MM-DD-00000.nc</terminal-line>
<terminal-line>ncatted -O -a month,global,o,l,<span style="color:red">MM</span> iced.YYYY-MM-DD-00000.nc</terminal-line>
<terminal-line>ncatted -O -a mday,global,o,l,<span style="color:red">DD</span> iced.YYYY-MM-DD-00000.nc</terminal-line>
</terminal-window>


Replace the `time` global attribute to equal the total number of seconds between 1/1/1 and the new date using the proleptic Gregorian calendar. This can be calculated using the `cftime` python library. E.g. using 2105-03-01 as the new date:
<terminal-window static>
<terminal-line>python</terminal-line>
<terminal-line>>>> import cftime</terminal-line>
<terminal-line>>>> start = cftime.datetime(1,1,1, calendar="proleptic_gregorian")</terminal-line>
<terminal-line>>>> end = cftime.datetime(2105,3,1, calendar="proleptic_gregorian")</terminal-line>
<terminal-line>>>> (end-start).total_seconds()</terminal-line>
<terminal-line>66400905600.0</terminal-line>
</terminal-window>

Then add this to the restart file using `nco`:
<terminal-window static>
<terminal-line>ncatted -O -a time,global,o,d,66400905600 iced.YYYY-MM-DD-00000.nc</terminal-line>
</terminal-window>