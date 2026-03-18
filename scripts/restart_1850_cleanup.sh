#!/bin/bash

# Remove the CICE initial restart file. Name has been changed so it won't be removed
# by the usual payu archiving

# This is only going to work if the payu run numbers hasn't been changed
if [[ $PAYU_CURRENT_RUN == 0 ]]; then
  rm work/ice/RESTART/iced.1850-01-01-00000.nc
fi
