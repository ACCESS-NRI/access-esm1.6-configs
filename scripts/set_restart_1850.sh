#!/bin/bash

# This script resets any set of ESM1.6 restart files to date 1850-01-01 at runtime
# for an historical experiment.
# See https://forum.access-hive.org.au/t/change-the-date-in-an-esm1-6-restart/5615

set -eu

# This is only going to work if the payu run numbers hasn't been changed
if [[ $PAYU_CURRENT_RUN != 0 ]]; then
  echo "Skipping restart changes"
  exit 0
fi

# Leap years cause issues as the run length is calculated prior to the restart modification.
# Produce an error if a leap year is being used.
python check_leap_year.py work/atmosphere/um.res.yaml


#### Atmosphere ####
cp work/atmosphere/restart_dump.astart $TMPDIR
python scripts/change_dump_date.py $TMPDIR/restart_dump.astart -o $TMPDIR/new_restart -y 1850 -m 1 -d 1
rm work/atmosphere/restart_dump.astart
mv $TMPDIR/new_restart work/atmosphere/restart_dump.astart

rm work/atmosphere/um.res.yaml
echo "end_date: 1850-01-01 00:00:00" > work/atmosphere/um.res.yaml

# The UM namelist was set using the original restart dates so basis time needs to be
# reset to 1850
ed work/atmosphere/namelists << EOF
/model_basis_time/
d
i
    model_basis_time = 1850, 1, 1, 0, 0, 0
.
/ancil_reftime/
d
i
    ancil_reftime = 1850, 1, 1, 0, 0, 0
.
w
q
EOF


#### Ocean ####
rm work/ocean/INPUT/ocean_solo.res
cat > work/ocean/INPUT/ocean_solo.res << EOF
     3        (Calendar: no_calendar=0, thirty_day_months=1, julian=2, gregorian=3, noleap=4)
     1     1     1     0     0     0        Model start time:   year, month, day, hour, minute, second
  1850     1     1     0     0     0        Current model time: year, month, day, hour, minute, second
EOF


#### Ice ####
echo './RESTART/iced.1850-01-01-00000.nc' > work/ice/RESTART/ice.restart_file
# Keep the original file because payu archiving wants to remove it
cp  work/ice/RESTART/iced*nc $TMPDIR/iced.1850-01-01-00000.nc
# 1850 time
ncatted -O -a year,global,o,l,1850 $TMPDIR/iced.1850-01-01-00000.nc
ncatted -O -a nyr,global,o,l,1850 $TMPDIR/iced.1850-01-01-00000.nc
# 58348771200 = seconds from (y m d) 1 1 1 to 1850 1 1 in proleptic Gregorian calendar
ncatted -O -a time,global,o,d,58348771200 $TMPDIR/iced.1850-01-01-00000.nc

cp -n $TMPDIR/iced.1850-01-01-00000.nc work/ice/RESTART/