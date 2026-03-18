#!/bin/bash

set -eu

module load nco

work_dir=$1
year=$2
month=$3
day=$4

echo "Setting restart date to ${year} ${month} ${day} (Y M D)"

## Atmosphere
# Update the date in the UM dump file
python ~access/apps/pythonlib/umfile_utils/access_cm2/change_dump_date.py ${work_dir}/atmosphere/restart_dump.astart <<< "$year $month $day"

padded_year=$(printf "%04d" $year)
padded_month=$(printf "%02d" $month)
padded_day=$(printf "%02d" $day)

# Update the date in the calendar file
sed -i "s/end_date:.*/end_date: ${padded_year}-${padded_month}-${padded_day} 00:00:00/" ${work_dir}/atmosphere/um.res.yaml

## Ocean
sed -i "s/.*Current model time.*/     ${year}     ${month}     ${day}     0     0     0        Current model time: year, month, day, hour, minute, second/" ${work_dir}/ocean/INPUT/ocean_solo.res

## Ice
new_ice_res_name=iced.${padded_year}-${padded_month}-${padded_day}-00000.nc

if [ ! -f ${work_dir}/ice/RESTART/${new_ice_res_name} ]; then
    mv ${work_dir}/ice/RESTART/iced.????-??-??-00000.nc ${work_dir}/ice/RESTART/${new_ice_res_name}
fi

echo ./RESTART/${new_ice_res_name} > ${work_dir}/ice/RESTART/ice.restart_file

ncatted -O -a year,global,o,l,$year ${work_dir}/ice/RESTART/${new_ice_res_name}
ncatted -O -a nyr,global,o,l,$year ${work_dir}/ice/RESTART/${new_ice_res_name}
ncatted -O -a month,global,o,l,$month ${work_dir}/ice/RESTART/${new_ice_res_name}
ncatted -O -a mday,global,o,l,$day ${work_dir}/ice/RESTART/${new_ice_res_name}

seconds=$(python ./scripts/set-restart-date/sec_year_1.py $year $month $day)
ncatted -O -a time,global,o,d,$seconds ${work_dir}/ice/RESTART/${new_ice_res_name}



