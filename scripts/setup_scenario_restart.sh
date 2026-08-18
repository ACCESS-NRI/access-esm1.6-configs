#PBS -P p66
#PBS -N restart_update
#PBS -q normal
#PBS -l walltime=00:10:00
#PBS -l mem=8GB
#PBS -l ncpus=1
#PBS -l storage=gdata/xp65+gdata/p66+gdata/vk83+gdata/access+gdata/p73
#PBS -l wd

set -euo pipefail

module use /g/data/xp65/public/modules
module load conda/analysis3-25.08

# Filepaths required for updating a historical restart for a scenario run
#REFERENCE_RESTART="/g/data/p66/rml599/scenarios/test-scen7-h/restart171/atmosphere/restart_dump.astart.orig"
REFERENCE_RESTART="/g/data/p73/archive/CMIP7/ACCESS-ESM1-6/production/ensemble-concentrations-historical/historical-historical-1.1-r1i1p1f1-01409bc3/historical-historical-1.1-r1i1p1f1-01409bc3/restart171/atmosphere/restart_dump.astart"
STASHMASTER_BASE_PATH="/g/data/vk83/prerelease/configurations/inputs/access-esm1p6/share/atmosphere/stash/2026.01.21/STASHmaster/STASHmaster_A"
#STASHMASTER_EXT_PATH="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/prefix.PRESM_A"
STASHMASTER_EXT_PATH="/g/data/p73/archive/CMIP7/ACCESS-ESM1-6/production/ensemble-concentrations-historical/historical-historical-1.1-r1i1p1f1-01409bc3/historical-historical-1.1-r1i1p1f1-01409bc3/output171/atmosphere/prefix.PRESM_A"
THINNING_FILE="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/luh3-1-1/scenarios/VL-Scenario/LUH3_cable_thinning_frac_from_bioh_rampnewtiles_scen_vl_2022-2101.nc"
LAND_COVER_FILE="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/luh3-1-1/scenarios/VL-Scenario/ACCESS_vegfrac_scen_vl_rampnewtiles_dims.nc"   # New vegetation distribution to substitute in
REMAP_CONFIG="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/remap_config_hist_to_scen_asluc.yaml"         # Config file to configure the remapping

# Filepaths for outputs
RESTART_AS_NETCDF="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_original.nc"    # Intermediate NetCDF file to hold the CABLE relevant fields
REMAPPED_RESTART_AS_NETCDF="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_updated.nc"  # Remapped CABLE fields
OUTPUT_RESTART="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_dump.astart.update"       # Name to write the new restart to

# Verify inputs upfront
[[ -f "${REFERENCE_RESTART}" ]]
[[ -f "${THINNING_FILE}" ]]
[[ -f "${LAND_COVER_FILE}" ]]
[[ -f "${STASHMASTER_BASE_PATH}" ]]
[[ -f "${STASHMASTER_EXT_PATH}" ]]

# Adjust the restart for scenario land cover
python convert_UM_restart_to_netcdf.py \
    -i "${REFERENCE_RESTART}" \
    -o "${RESTART_AS_NETCDF}" \
    -s "${STASHMASTER_BASE_PATH},${STASHMASTER_EXT_PATH}"

python adjust_restart_for_new_land_cover.py \
	-i "${RESTART_AS_NETCDF}" \
	-o "${REMAPPED_RESTART_AS_NETCDF}" \
	-m "${LAND_COVER_FILE}" \
	-c "${REMAP_CONFIG}" \
	--use-previous-fractions-from-restart

python add_netcdf_fields_to_UM_restart.py \
    -i "${REMAPPED_RESTART_AS_NETCDF}" \
    -o "${OUTPUT_RESTART}" \
    -r "${REFERENCE_RESTART}" \
    -s "${STASHMASTER_BASE_PATH},${STASHMASTER_EXT_PATH}"


# Add scenario wood thinning data to restart
# - this output is just used for testing purposes
#   as the script update_thinning_scenario.py overwrites 
#   the existing file
RESTART_BACKUP="${OUTPUT_RESTART}.pre_thinning"

printf "Copying restart ${OUTPUT_RESTART} to ${RESTART_BACKUP}\n" "before over-writing with new thinning field"
cp "${OUTPUT_RESTART}" "${RESTART_BACKUP}"

python update_thinning_scenario.py \
    --restart-file "${OUTPUT_RESTART}" \
    --thinning-file "${THINNING_FILE}" \
    --stashmaster-file "${STASHMASTER_BASE_PATH}"

# Write out additional outputs for testing purposes
echo "Converting modified restart (with thinning) to netcdf"
RESTART_AS_NETCDF_THIN="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_w_thinning.nc"
python convert_UM_restart_to_netcdf.py -i "${OUTPUT_RESTART}" -o "${RESTART_AS_NETCDF_THIN}" -s "${STASHMASTER_BASE_PATH},${STASHMASTER_EXT_PATH}"

echo "Converting modified restart (without thinning) to netcdf"
RESTART_AS_NETCDF_PRETHIN="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_wout_thinning.nc"
python convert_UM_restart_to_netcdf.py -i "${RESTART_BACKUP}" -o "${RESTART_AS_NETCDF_PRETHIN}" -s "${STASHMASTER_BASE_PATH},${STASHMASTER_EXT_PATH}"
