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

function run_conversion () {
    esm1p5_convert_nc $PAYU_CURRENT_OUTPUT_DIR --delete-ff
}

MAX_TRY=3
for TRY in $(seq 1 $MAX_TRY); do
    # Run the conversion. Capture stderr for error handling
    { error_msg=$(run_conversion 2>&1 1>&$out); exit_code=$?; } {out}>&1
    # Close additional file descriptor
    {out}>&-

    # Write to stderr
    echo "${error_msg}" 1>&2

    if [[ $exit_code == 0 ]]; then
        # Successful conversion
        break
    elif [[ $exit_code == 255 ]] && [[ $error_msg =~ "container creation failed" ]]; then

        # Transient container failure with error code 255: Retry
        echo "Conversion attempt ${TRY} failed."

        if [[ $TRY < $MAX_TRY ]]; then
            echo "Re-trying conversion."
        else
            echo "Maximum number of ${MAX_TRY} conversion attempts reached. Exiting."
            exit $exit_code
        fi

    else
        # Other error: Exit normally
        exit $exit_code
    fi
done
