#!/bin/bash

# This script sets the start date in an ESM1.6 restart file to the specified year, month and day
# See https://forum.access-hive.org.au/t/change-the-date-in-an-esm1-6-restart/5615

set -eu

while getopts ":r:y:m:d:" opt; do
    case ${opt} in
        r)
            RESTARTDIR=${OPTARG}
        ;;
        y)
            YEAR=${OPTARG}
            printf -v zyear "%04d" $YEAR
        ;;
        m)
            MONTH=${OPTARG}
            printf -v zmonth "%02d" $MONTH
        ;;
        d)
            DAY=${OPTARG}
            printf -v zday "%02d" $DAY
        ;;
        :)
            echo "Option \"-${OPTARG}\" requires an argument." 
            exit 1 
        ;;
    esac
done


#### Atmosphere ####
python scripts/change_dump_date.py $RESTARTDIR/atmosphere/restart_dump.astart -o $RESTARTDIR/atmosphere/new_restart -y $YEAR -m $MONTH -d $DAY
mv $RESTARTDIR/atmosphere/new_restart $RESTARTDIR/atmosphere/restart_dump.astart

echo "end_date: $zyear-$zmonth-$zday 00:00:00" > $RESTARTDIR/atmosphere/um.res.yaml


#### Ocean ####
sed -i "s/.*Current model time:.*/$YEAR     $MONTH     $DAY     0     0     0        Current model time: year, month, day, hour, minute, second/" $RESTARTDIR/ocean/ocean_solo.res


#### Ice ####
iced_file="iced.${zyear}-${zmonth}-${zday}-00000.nc"

mv $RESTARTDIR/ice/iced.????-??-??-00000.nc $RESTARTDIR/ice/$iced_file

echo "./RESTART/$iced_file" > $RESTARTDIR/ice/ice.restart_file

ncatted -h -O -a year,global,o,l,$YEAR $RESTARTDIR/ice/$iced_file
ncatted -h -O -a nyr,global,o,l,$YEAR $RESTARTDIR/ice/$iced_file
ncatted -h -O -a month,global,o,l,$MONTH $RESTARTDIR/ice/$iced_file
ncatted -h -O -a mday,global,o,l,$DAY $RESTARTDIR/ice/$iced_file

# Calculate total seconds from 1/1/1 to specified date
seconds=$( python scripts/calc_seconds.py -y $YEAR -m $MONTH -d $DAY)
ncatted -h -O -a time,global,o,d,$seconds $RESTARTDIR/ice/$iced_file
