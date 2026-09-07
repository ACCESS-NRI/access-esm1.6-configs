#!/usr/bin/env python3

import um_replace_field
import xarray
import argparse
import tempfile
import os
import shutil
import stat

def _parse_args():
    parser = argparse.ArgumentParser(
            description='Update wood thinning ancillary for current year'
            )

    parser.add_argument(
        '--restart-file',
        type=str,
        required=True,
        help='End of year restart file to modify.'
        )
    parser.add_argument(
        '--thinning-file',
        type=str,
        required=True,
        help='Wood thinning file to use as source.'
        )
    parser.add_argument(
        '--stashmaster-file',
        type=str,
        required=True,
        help='Path to base STASHMaster_A file.'
        )

    return parser.parse_args()


def insert_thinning(restart_file, thinning_file, stashmaster_file):
    um_file = um_replace_field.open_fields_file(
        restart_file,
        stashmaster_file,
        0
        )

    time_coder = xarray.coders.CFDatetimeCoder(use_cftime=True)

    thinning_file = xarray.open_dataset(thinning_file, decode_times=time_coder)

    target_year = um_file.fixed_length_header.t2_year
    time_values = thinning_file.time.dt.year.values
    matches = (time_values == target_year).nonzero()[0]

    if len(matches) == 0:
        raise ValueError(
            f"Year {target_year} not found in thinning file. "
            f"Available years: {time_values.min()} "
            f"to {time_values.max()}"
        )

    t_index = int(matches[0])
    print(f"target_year: {target_year}")
    print(f"Available years in thinning file: {time_values.min()} to {time_values.max()}")
    print(f"t_index: {t_index}")

    # Create a temporary file to write to
    tmp = tempfile.NamedTemporaryFile()
    um_replace_field.replace_fields(
        um_file,
        {"fraction": "WOOD THINNING"},
        thinning_file,
        tmp.name,
        t_index
        )

    shutil.copy(tmp.name, restart_file)

    # tempfiles only have user read+write permissions.
    # Set user read+write and group read permission
    os.chmod(restart_file, stat.S_IREAD | stat.S_IWRITE | stat.S_IRGRP)


if __name__ == "__main__":
    args = _parse_args()
    insert_thinning(args.restart_file, args.thinning_file, args.stashmaster_file)
