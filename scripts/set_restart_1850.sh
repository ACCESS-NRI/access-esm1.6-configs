#!/bin/bash

# This script resets any set of ESM1.6 restart files to date 1850-01-01 at runtime
# for an historical experiment.
# See https://forum.access-hive.org.au/t/change-the-date-in-an-esm1-6-restart/5615

# This is only going to work if the payu run numbers hasn't been changed
if [[ $PAYU_CURRENT_RUN != 0 ]]; then
  echo "Skipping restart changes"
  exit 0
fi

cp work/atmosphere/restart_dump.astart $TMPDIR
python ~access/apps/pythonlib/umfile_utils/access_cm2/change_dump_date.py $TMPDIR/restart_dump.astart <<< "1850 01 01"
rm work/atmosphere/restart_dump.astart
mv $TMPDIR/restart_dump.astart work/atmosphere/restart_dump.astart

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

rm work/ocean/INPUT/ocean_solo.res
cat > work/ocean/INPUT/ocean_solo.res << EOF
     3        (Calendar: no_calendar=0, thirty_day_months=1, julian=2, gregorian=3, noleap=4)
     1     1     1     0     0     0        Model start time:   year, month, day, hour, minute, second
  1850     1     1     0     0     0        Current model time: year, month, day, hour, minute, second
EOF

module load nco

# CICE files are copies rather than links, so modify directly
echo './RESTART/iced.1850-01-01-00000.nc' > work/ice/RESTART/ice.restart_file
# Keep the original file because payu archiving wants to remove it
cp work/ice/RESTART/iced*nc work/ice/RESTART/iced.1850-01-01-00000.nc
# 1850 time
ncatted -O -a year,global,o,l,1850 work/ice/RESTART/iced.1850-01-01-00000.nc
ncatted -O -a nyr,global,o,l,1850 work/ice/RESTART/iced.1850-01-01-00000.nc
ncatted -O -a time,global,o,d,58348771200 work/ice/RESTART/iced.1850-01-01-00000.nc
