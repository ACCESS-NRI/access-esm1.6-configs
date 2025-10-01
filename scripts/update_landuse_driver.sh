#!/bin/bash
set -eu

# Update land use fields in the end of year restart
# This file will have a name of form aiihca.da??110
year_end_restart=work/atmosphere/aiihca.da??110

if [ -f $year_end_restart ]; then
    ./scripts/update_landuse.py work/atmosphere/INPUT/LUH3.1.1_states_remap_normed_to_pfts_1850-2023_v5.nc $year_end_restart
else
    echo "Warning: No atmosphere end of year restart file found. update_landuse.py will not be run." >&2 
fi

if [[ $? != 0 ]]; then
    echo "Error from update_landuse.py" >&2
    exit 1
fi
