#!/bin/bash

module use /g/data/vk83/prerelease/modules
module load payu/dev

module list
which payu
which validatemeta

ACCESS_OUTPUT_SCHEMA_URL="https://raw.githubusercontent.com/ACCESS-NRI/schema/refs/heads/main/au.org.access-nri/model/output/file-metadata/2-0-0/2-0-0.json"

# Validate
for f in  ${PAYU_CURRENT_OUTPUT_DIR}/{ocean,ice,atmosphere/netCDF}/*.nc
do
  echo $f
  validatemeta -v -s ${ACCESS_OUTPUT_SCHEMA_URL} $f
done
