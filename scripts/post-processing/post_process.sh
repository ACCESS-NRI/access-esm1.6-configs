#!/bin/bash
#PBS -l ncpus=1
#PBS -l mem=60GB
#PBS -l jobfs=0GB
#PBS -q normal
#PBS -l walltime=02:30:00
#PBS -l wd
#PBS -W umask=027

set -e

module use /g/data/vk83/modules
module load model-processing/1.0.0_0

# Convert UM atmosphere fields files to netCDF.
# By default UM atmosphere fields files are deleted after conversion to save space. 
# Remove --delete-ff command line option to retain original files for testing purposes
# Source code for the um2nc command is available at https://github.com/ACCESS-NRI/um2nc-standalone/
um2nc driver esm1p6 $PAYU_CURRENT_OUTPUT_DIR --delete-ff  --one-nc-per-stash-variable


# Clean up global metatdata to meet ACCESS-NRI dataspec standards
# https://access-output-data-specifications.readthedocs.io/en/latest/specification/

for submodel in {atmosphere};
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