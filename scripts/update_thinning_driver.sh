#!/bin/bash

set -eu

current_rst=atmosphere/restart_dump.astart

./scripts/update_thinning.py --restart-file="./work/atmosphere/restart_dump.astart" \
  --thinning-file="/g/data/p66/tfl561/thinning/harvest_frac/cable_thinning_frac_1850-2015.nc"
