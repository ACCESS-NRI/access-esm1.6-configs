#!/bin/bash

# Run validate meta on all files in specified payu outputXXX directory

show_usage() {
    echo "Usage: $(basename "$0") <output_directory_name>" >&2
    echo "Error: Missing required argument <output_directory_name>." >&2
    exit 1
}

# Check if the number of arguments ($#) is less than 1
if [[ $# -lt 1 ]]; then
    show_usage
fi

ACCESS_OUTPUT_SCHEMA_URL="https://raw.githubusercontent.com/ACCESS-NRI/schema/refs/heads/main/au.org.access-nri/model/output/file-metadata/2-0-0/2-0-0.json"

# Validate
for f in  $1/{ocean,ice,atmosphere/netCDF}/*.nc
do
  echo $f
  validatemeta -v -s ${ACCESS_OUTPUT_SCHEMA_URL} $f
done
