#!/bin/bash

set -eu

current_rst=atmosphere/restart_dump.astart

python ./scripts/update_thinning.py --restart-file="./atmosphere/restart_dump.astart" \
  --thinning-file="/g/data/p66/tfl561/thinning/harvest_frac/cable_thinning_frac_1850-2015.nc"
