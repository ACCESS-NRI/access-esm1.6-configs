#!/bin/bash
#PBS -l ncpus=1
#PBS -l mem=20GB
#PBS -l jobfs=0GB
#PBS -q normal
#PBS -l walltime=00:40:00
#PBS -l wd

module use /g/data/vk83/modules
module load payu

# Command below calls https://github.com/ACCESS-NRI/um2nc-standalone/blob/main/umpost/conversion_driver_esm1p5.py
# By default UM atmosphere fields files are deleted after conversion to save space. 
# Remove --delete-ff command line option to retain original files for testing purposes
esm1p5_convert_nc $PAYU_CURRENT_OUTPUT_DIR --delete-ff
