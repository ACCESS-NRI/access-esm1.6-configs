#!/bin/bash
set -eu

if [ $PAYU_CURRENT_RUN -ne 0 ]; then
    # Wood product should not be initialised after the first simulation
    exit 0
fi

# Set the initial year to 1850
./scripts/set-restart-date/set_restart_date.sh ./work/ 1850 1 1


# Set the initial wood product
python ./scripts/set-initial-wood-product/insert_external_woodprod_CNP.py --restart work/atmosphere/restart_dump.astart --woodfile /g/data/tm70/sw6175/development/esm1p6/access-esm1.6-configs/scripts/set-initial-wood-product/access-esm16_wood_prod_initial_1850_40PgC.nc --stash-base work/atmosphere/INPUT/STASHmaster/STASHmaster_A --stash-prefix ./work/atmosphere/prefix.PRESM_A



