import argparse
import git
from ruamel.yaml import YAML
from pathlib import Path
import shutil
import shlex
import subprocess
import re
import tempfile

from update_thinning_scenario import insert_thinning
from convert_UM_restart_to_netcdf import convert_restart
from adjust_restart_for_new_land_cover import run_vegetation_remapping
from add_netcdf_fields_to_UM_restart import insert_fields_to_restart

STASHMASTER_PATH = "/g/data/vk83/prerelease/configurations/inputs/access-esm1p6/share/atmosphere/stash/2026.01.21/STASHmaster/STASHmaster_A"


# Filepaths required for updating a historical restart for a scenario run
THINNING_FILE="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/luh3-1-1/scenarios/VL-Scenario/LUH3_cable_thinning_frac_from_bioh_rampnewtiles_scen_vl_2022-2101.nc"
LAND_COVER_FILE="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/luh3-1-1/scenarios/VL-Scenario/ACCESS_vegfrac_scen_vl_rampnewtiles_dims.nc"   # New vegetation distribution to substitute in
REMAP_CONFIG="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/remap_config_hist_to_scen_asluc.yaml"         # Config file to configure the remapping

# Filepaths for outputs
# RESTART_AS_NETCDF="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_original.nc"    # Intermediate NetCDF file to hold the CABLE relevant fields
# REMAPPED_RESTART_AS_NETCDF="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_updated.nc"  # Remapped CABLE fields
# OUTPUT_RESTART="/g/data/p66/ajn563/ACCESS-ESM/ESM1.6/configs/restarts/scenarios/setup_scen_restart/restart_dump.astart.update"       # Name to write the new restart to

# Filepaths required for wood thinning


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Copy and modify a ESM1.6 historical restart directory for use as the"
            "initial condition in a ScenarioMip simulation. This includes:\n"
            " - Adjusting the land fields for compatibility with the scenario land cover\n"
            " - Inserting scenarion wood thinning data into the restart\n"
            "The initial restart path is taken from the config.yaml, and the output restart path can be specified as an argument."
            "This script should be run from the payu control directory"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--output-restart',
        help='Path for saving modified output ESM1.6 restart directory. Defaults to archive/initial_restart.',
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
        " * Land fields adjusted for compatibility with scenario vegetation fractions.\n"
        " * Initial scenario wood thinning data inserted into the restart."
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

    
    atm_restart = output_restart/"atmosphere"/"restart_dump.astart"

    # Convert UM restart to netCDF
    restart_as_nc = tempfile.NamedTemporaryFile().name
    convert_restart(atm_restart, restart_as_nc, STASHMASTER_PATH)

    remapped_restart_nc = tempfile.NamedTemporaryFile().name
    # Step 2: Adjust restart for new land cover
    run_vegetation_remapping(
        input=restart_as_nc,
        output=remapped_restart_nc,
        vegetation_map=LAND_COVER_FILE,
        time_index=0,
        fill_all=False,
        use_previous_fractions_from_restart=True
    )

    # Step 3: Add remapped data from netCDF bank into the original restart
    remapped_restart_um = tempfile.NamedTemporaryFile().name
    insert_fields_to_restart(
        processed_restart=remapped_restart_nc,
        output=remapped_restart_um,
        base_restart=atm_restart,
        stash_list=STASHMASTER_PATH       
    )

    # Step 4: Add initial scenario wood thinning data to the restart
    insert_thinning(
        restart_file=remapped_restart_um,
        thinning_file=THINNING_FILE,
        stashmaster_file=STASHMASTER_PATH
    )

    # Move the modified restart to the final location
    shutil.move(remapped_restart_um, atm_restart)

    # Add the new restart path to the config.yaml
    update_config(output_restart, config)

    # Commit the changes to the runlogs
    commit_config(input_restart, output_restart)
