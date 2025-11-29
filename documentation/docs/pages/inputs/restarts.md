

A restart file contains a complete snapshot of a model state, allowing for experiments to be 
run in smaller segments, or stopped and restarted at a later date. This page outlines the structure
of an ESM1.6 restart file and details commonly required manipulations.


## Structure of the ESM1.6 restart directory

ESM1.6 restart files are organised by component, with seperate files for the atmosphere, ocean, sea ice, and coupler:

```
$ ls /g/data/vk83/prerelease/configurations/inputs/access-esm1p6/modern/pre-industrial-emissions/restart/2025.11.28
atmosphere  coupler  ice  ocean  README
```

### atmosphere
The atmosphere restart directory contains the following files
```
restart_dump.astart  um.res.yaml
```
`restart_dump.astart` is the UM restart file, containing the model state. This also holds static information
about the lower boundary such as the land-sea mask, vegetation maps and orography.

`um.res.yaml` is a calendar file holding the date and time associated with the restart. `payu` copies the information 
in this file into the model namelists at runtime.


### Ocean
The ocean restarts are broken up into seperate groups of variables:
```
ocean_age.res.nc           ocean_density.res.nc       ocean_neutral.res.nc   ocean_sigma_transport.res.nc  ocean_thickness.res.nc           ocean_velocity.res.nc
ocean_barotropic.res.nc    ocean_frazil.res.nc        ocean_pot_temp.res.nc  ocean_solo.res                ocean_tracer.res                 ocean_wombatlite_airsea_flux.res.nc
ocean_bih_friction.res.nc  ocean_lap_friction.res.nc  ocean_sbc.res.nc       ocean_temp_salt.res.nc        ocean_velocity_advection.res.nc  ocean_wombatlite.res.nc
```


`ocean_solo.res` is a calendar file specifying the model date and time. All other files contain
snapshots of the state for different variables.

### Ice

The ice restart directory contains the following files:

```
cice_in.nml  iced.2145-01-01-00000.nc  ice.restart_file  mice.nc
```

`iced.2145-01-01-00000.nc` holds the model state and carries the model date in the global attributes. `ice.restart_file` is 
a pointer file used by CICE to find the correct restart. `mice.nc` contains ice coupling data to be sent to the ocean model
at the beginning of the next run.

### Coupler
The coupler restart directory contains the last set of coupling fields sent between the components at the termination 
of the previous run. These allow the components to start up with all the required coupling data.

```
a2i.nc  i2a.nc  o2i.nc
```




## Common restart manipulations

### Changing the date of a restart file

It's common to take a restart file from one experiment and use it in another. For example, a pre-industrial
restart might be used to start a historical experiment. This often requires changing the date in the restart files.

When changing the date, it's important to make sure that the dates for the different components match.
Otherwise analysis can be complicated by missmatched dates, and model crashes can occur when only some of the components are in a leap year. 


The following instructions outline how to modify the date for each component:

#### Atmosphere:
Navigate to the `restart/atmosphere` directory
```
module use /g/data/xp65/public/modules
module load conda/analysis3

# Update the date in the UM dump file
python ~access/apps/pythonlib/umfile_utils/access_cm2/change_dump_date.py restart_dump.astart  <<< "YYYY MM DD"
# Update the date in the calendar file
sed -i "s/end_date:.*/end_date: YYYY-MM-DD 00:00:00/" <new-restart-path>/atmosphere/um.res.yaml
```

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
Rename the `iced.YYYY-MM-DD-00000.nc` to use the new date. The year, month, and day should be zero padded. Edit the `ice.restart` pointer file to use the new file name:
```
echo ./RESTART/iced.YYYY-MM-DD-00000.nc   >  ice.restart
```

Replace the `year`, `nyr`, `month`, and `mday` global attributes using `nco` (in most cases, only the year will need to be changed):
```
module load nco
ncatted -O -a year,global,o,l,<YYYY> iced.YYYY-MM-DD-00000.nc
ncatted -O -a nyr,global,o,l,<YYYY> iced.YYYY-MM-DD-00000.nc
ncatted -O -a month,global,o,l,<MM> iced.YYYY-MM-DD-00000.nc
ncatted -O -a mday,global,o,l,<DD> iced.YYYY-MM-DD-00000.nc
```
Replace the `time` global attribute to equal the total number of seconds between 1/1/1 and the new date using the proleptic Gregorian calendar. This can be calculated using the `cftime` python library. E.g. using 2105-03-01 as the new date:
```
python 
>>> import cftime
>>> start = cftime.datetime(1,1,1, calendar="proleptic_gregorian")
>>> end = cftime.datetime(2105,3,1, calendar="proleptic_gregorian")
>>> (end-start).total_seconds()

66400905600.0
```

Then use nco to add this to the restart file:
```
ncatted -O -a time,global,o,d,66400905600 iced.YYYY-MM-DD-00000.nc
```