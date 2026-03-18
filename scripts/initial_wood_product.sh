#!/bin/bash
set -eu

# Set the size of the initial wood carbon nitrogen and phosphorous pools
# for an emissions driven historical simulation. This modifies the atmospheric
# restart file in the work directory prior to the start of the simulation.

# Wood product should only be initialised in the first simulation.
# This will only work if the Payu run number is not changed.
if [ $PAYU_CURRENT_RUN -ne 0 ]; then
    echo "Skipping restart changes"
    exit 0
fi


# Set the initial wood product
# Write to a temporary area
prep_dir=$(mktemp -d)

python ./scripts/set-initial-wood-product/insert_external_woodprod_CNP.py --restart work/atmosphere/restart_dump.astart \
                    --output $prep_dir/restart_dump.astart \
                    --woodfile /g/data/tm70/sw6175/development/esm1p6/access-esm1.6-configs/scripts/set-initial-wood-product/access-esm16_wood_prod_initial_1850_40PgC.nc \
                    --stash-base work/atmosphere/INPUT/STASHmaster/STASHmaster_A \
                    --stash-prefix ./work/atmosphere/prefix.PRESM_A

mv $prep_dir/restart_dump.astart work/atmosphere/restart_dump.astart


