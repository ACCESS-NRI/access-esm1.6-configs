#!/bin/bash
#PBS -l ncpus=1
#PBS -l mem=60GB
#PBS -l jobfs=0GB
#PBS -q normal
#PBS -l walltime=02:30:00
#PBS -l wd
#PBS -W umask=027

set -e

module use /g/data/vk83/staging/modules
module load model-processing/20260805T125219-7abd909-pr90

# Convert UM atmosphere fields files to netCDF.
# By default UM atmosphere fields files are deleted after conversion to save space. 
# Remove --delete-ff command line option to retain original files for testing purposes
# Source code for the um2nc command is available at https://github.com/ACCESS-NRI/um2nc-standalone/
um2nc driver esm1p6 $PAYU_CURRENT_OUTPUT_DIR --delete-ff  --one-nc-per-stash-variable


# Split sea ice output into single variable files using the splitnc command. The splitnc command calls https://github.com/ACCESS-NRI/splitnc/blob/main/src/splitnc/splitnc.py
icefiles=($PAYU_CURRENT_OUTPUT_DIR/ice/iceh-*)

# Only run splitnc if unprocessed ice files exist to avoid errors on reruns
if [ "${#icefiles[@]}" -gt 0 ]
then
    splitnc --shared-vars uarea,tmask,tarea --excluded-vars VGRD.  --use-esm1p6-filenames --fix-cell-methods --skip-existing "${icefiles[@]}"
    if [ $? -eq 0 ]; then
      rm "${icefiles[@]}"
    fi
fi


# Clean up global metatdata to meet ACCESS-NRI dataspec standards
# https://access-output-data-specifications--2.org.readthedocs.build/en/2/

for submodel in {atmosphere,ocean,ice};
do
    addmeta \
        -v -s \
        -d metadata.yaml \
        -d $PAYU_CURRENT_OUTPUT_DIR/env.yaml \
        -m scripts/post-processing/addmeta/dataspec.yaml \
        -m scripts/post-processing/addmeta/${submodel}.yaml \
        --fnregex='access-esm1p6\.\w+(?:\.\dd)?\.(?P<var>\w+)\.(?P<freq>\w{2,4})(?:\.\w+)?(?:\.\d{4})?\.nc' \
        $PAYU_CURRENT_OUTPUT_DIR/${submodel}/*.nc
done