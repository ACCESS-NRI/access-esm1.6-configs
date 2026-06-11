#!/g/data/vk83/apps/payu/1.1.5/bin/python

import um_replace_field
import xarray
import argparse
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

    ref_year = 1850
    model_year = um_file.fixed_length_header.t2_year
    t_index = model_year - ref_year

    thinning_file = xarray.open_dataset(thinning_file, decode_times=False)

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

    shutil.copy(tmp.name, restart_file)


if __name__ == "__main__":
    args = _parse_args()
    insert_thinning(args.restart_file, args.thinning_file, args.stashmaster_file)
