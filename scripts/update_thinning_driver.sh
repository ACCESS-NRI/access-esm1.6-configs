#!/bin/bash

set -eu

# Update wood thinning fields in the end of year restart
# This file will have a name of form aiihca.da??110
year_end_restart=work/atmosphere/aiihca.da??110

if [ -f $year_end_restart ]; then
   ./scripts/update_thinning.py --restart-file $year_end_restart \
  --thinning-file "./work/atmosphere/INPUT/LUH3_cable_thinning_frac_from_bioh_1850-2023_v2.nc" \
  --stashmaster-file "./work/atmosphere/INPUT/STASHmaster/STASHmaster_A"
else
    echo "Warning: No atmosphere end of year restart file found. update_thinning.py will not be run." >&2
fi

if [[ $? != 0 ]]; then
    echo "Error from update_thinning.py" >&2
    exit 1
fi
