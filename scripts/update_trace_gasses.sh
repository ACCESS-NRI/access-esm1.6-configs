#!/bin/bash

source /etc/profile.d/modules.sh
module purge
module use /g/data/hh5/public/modules
module load conda

python3 $(dirname $0)/update_trace_gasses.py
