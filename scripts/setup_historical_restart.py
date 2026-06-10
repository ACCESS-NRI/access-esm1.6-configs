import argparse
import git
from ruamel.yaml import YAML
from pathlib import Path
import shutil
import shlex
import subprocess
import re

import insert_external_woodprod_CNP
import update_thinning

# Filepaths required for the initial wood product script
EXTERNAL_NC_PATH = "/g/data/vk83/prerelease/configurations/inputs/access-esm1p6/modern/historical/atmosphere/land/biogeochemistry/global.N96/2026.05.08/access-esm16_wood_prod_initial_1850_20PgC.nc"
STASHMASTER_BASE_PATH = "/g/data/vk83/prerelease/configurations/inputs/access-esm1p6/share/atmosphere/stash/2026.01.21/STASHmaster/STASHmaster_A"
STASHMASTER_EXT_PATH = "./atmosphere/prefix.PRESM_A"

# Filepaths required for wood thinning
THINNING_FILE = "/g/data/vk83/configurations/inputs/access-esm1p6/modern/historical/atmosphere/land/vegetation/global.N96/2026.05.08/LUH3_cable_thinning_frac_from_bioh_1850-2023_v2.nc"


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Copy and modify an ESM1.6 restart directory for use as the"
            "initial condition in a historical simulation. This includes:\n"
            " - Resetting the restart date to 1850-01-01\n"
            " - Inserting an initial wood product of 20PgC into the atmosphere restart\n"
            "The initial restart path is taken from the config.yaml, and the output restart path is specified as an argument."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--output-restart',
        help='Path for saving modified output ESM1.6 restart directory.',
        type=Path,
        required=False
        )

    return parser.parse_args()


def get_archive_path():
    """Get the archive path for the current experiment."""
    repo = git.Repo(".")
    current_branch = repo.active_branch.name

    cmd = f"payu checkout {current_branch}"
    checkout_output = subprocess.run(shlex.split(cmd), check=True, capture_output=True, text=True).stdout

    pattern = r"\nAdded archive symlink to (?P<archive>.*)\n"
    if match := re.search(pattern, checkout_output):
        archive_path = Path(match.group('archive'))
    else:
        raise RuntimeError("Unable to get experiment archive path.")

    return archive_path


def copy_restart(input, output):
    """Copy the input restart directory to the specified output location"""
    if output.exists():
        raise FileExistsError(f"Output path {output} already exists.")

    print(f"Copying {input} to {output}")
    shutil.copytree(input, output)


def set_restart_date(restart_dir, year, month, day):
    """Set the date for each component's restart files"""
    print(f"Setting restart date to {year:04d}-{month:02d}-{day:02d}")
    cmd = f"./scripts/set_restart_date.sh -r {restart_dir} -y {year} -m {month} -d {day}"
    subprocess.check_call(shlex.split(cmd))


def update_config(restart_dir, config):
    """Update the restart path in the config.yaml"""
    print("Updating config.yaml with new restart path")
    config["restart"] = str(restart_dir)
    YAML().dump(config, Path("config.yaml"))


def commit_config(input_restart, output_restart):
    """Commit changes to the config.yaml"""
    repo = git.Repo(".")
    repo.index.add("config.yaml")
    msg = (
        f"Restarts in {input_restart} copied to {output_restart} and modified\n"
        f"using {Path(__file__).name}\n"
        " * Restart date changed to 1850 01 01.\n"
        " * Initial wood product inserted into atmosphere restart.\n"
        " * 1850 wood thinning data inserted into atmosphere restart"
    )
    print(f"Commiting changes to config.yaml with message: '{msg}'")
    repo.index.commit(msg)


if __name__ == "__main__":
    args = parse_args()

    output_restart = args.output_restart
    if output_restart is None:
        output_restart = get_archive_path() / "initial_restart"

    output_restart = output_restart.resolve()

    config = YAML().load(Path("config.yaml"))
    input_restart = config["restart"]
    copy_restart(input_restart, output_restart)

    # Set restart date to 1850 01 01
    set_restart_date(output_restart, year=1850, month=1, day=1)

    # Insert initial wood product into atmosphere restart
    atm_restart = output_restart/"atmosphere"/"restart_dump.astart"
    insert_external_woodprod_CNP.insert_woodprod(
        restart_path=str(atm_restart),
        external_nc_path=EXTERNAL_NC_PATH,
        stashmaster_base_path=STASHMASTER_BASE_PATH,
        stashmaster_ext_path=STASHMASTER_EXT_PATH,
        output_path=str(atm_restart)
    )

    # Add initial wood thinning data to restart
    update_thinning.insert_thinning(
        restart_file=str(atm_restart),
        thinning_file=THINNING_FILE,
        stashmaster_file=STASHMASTER_BASE_PATH
    )
    update_config(output_restart, config)
    commit_config(input_restart, output_restart)
