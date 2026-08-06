#!/g/data/vk83/apps/payu/1.1.5/bin/python

import um_replace_field
import xarray
import argparse
import mule
import tempfile
import shutil

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

    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()

    um_file = um_replace_field.open_fields_file(
        args.restart_file,
        "work/atmosphere/INPUT/STASHmaster/STASHmaster_A",
        0
        )

    time_coder = xarray.coders.CFDatetimeCoder(use_cftime=True)

    thinning_file = xarray.open_dataset(args.thinning_file, decode_times=time_coder)

    target_year = um_file.fixed_length_header.t2_year
    time_values = thinning_file.time.dt.year.values
    matches = (time_values == target_year).nonzero()[0]

    if len(matches) == 0:
        raise ValueError(
            f"Year {target_year} not found in thinning file. "
            f"Available years: {time_values.min()} to {time_values.max()}"
        )

    t_index = int(matches[0])

    # Create a temporary file to write to
    tmp = tempfile.NamedTemporaryFile()
    um_replace_field.replace_field(
        um_file,
        "WOOD THINNING",
        thinning_file,
        "fraction",
        tmp.name,
        t_index
        )

    shutil.move(args.restart_file, args.restart_file + "_orig")
    shutil.copy(tmp.name, args.restart_file)
