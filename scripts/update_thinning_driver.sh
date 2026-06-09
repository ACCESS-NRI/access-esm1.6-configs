#!/bin/bash

set -eu

./scripts/update_thinning.py --restart-file="./work/atmosphere/restart_dump.astart" \
  --thinning-file="./work/atmosphere/INPUT/LUH3_cable_thinning_frac_from_bioh_1850-2023_v2.nc" \
  --stashmaster-file "./work/atmosphere/INPUT/STASHmaster/STASHmaster_A"
