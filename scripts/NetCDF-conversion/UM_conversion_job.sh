#!/bin/bash
#PBS -l ncpus=1
#PBS -l mem=20GB
#PBS -l jobfs=0GB
#PBS -q express
#PBS -l walltime=00:10:00
#PBS -l wd
#PBS -l storage=gdata/vk83
#PBS -W umask=027

module use /g/data/vk83/prerelease/modules
module load payu/dev

module list
which payu
which addmeta

# Command below calls https://github.com/ACCESS-NRI/um2nc-standalone/blob/main/umpost/conversion_driver_esm1p5.py
# By default UM atmosphere fields files are deleted after conversion to save space. 
# Remove --delete-ff command line option to retain original files for testing purposes
# esm1p5_convert_nc $PAYU_CURRENT_OUTPUT_DIR --delete-ff

# Clean up global metatdata to meet ACCESS-NRI dataspec standards
# https://access-output-data-specifications--2.org.readthedocs.build/en/2/
for cmdfile in addmeta/{ocean,ice,atmosphere}/addmeta*.args
do
  addmeta -v -c ${cmdfile}
done

# Validate
for f in  ${PAYU_CURRENT_OUTPUT_DIR}/{ocean,ice,atmosphere/netCDF}/*.nc
do
  echo $f
  validatemeta -v -s testing/2-0-0/2-0-0.json $f
done
