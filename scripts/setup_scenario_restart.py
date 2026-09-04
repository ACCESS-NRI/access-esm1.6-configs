#!/usr/bin/env python3
import argparse
import git
from ruamel.yaml import YAML
from pathlib import Path
import shutil
import shlex
import subprocess
import re
import tempfile
import xarray

from update_thinning import insert_thinning
from convert_UM_restart_to_netcdf import convert_restart
from adjust_restart_for_new_land_cover import run_vegetation_remapping
from um_replace_field import open_fields_file, replace_fields


# Filepaths required for updating a historical restart for a scenario run
REMAP_CONFIG="./scripts/remap_config_hist_to_scen_asluc.yaml"         # Config file to configure the remapping


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Copy and modify an ESM1.6 restart from a historical experiment for use as the"
            "initial condition in a ScenarioMip simulation. Apply the following modifications:\n"
            " - Adjust the land fields for compatibility with the scenario land cover\n"
            " - Insert initial scenario wood thinning data into the restart\n"
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


def input_path_from_config(config, submodel, re_pattern):
    """
    Search a submodel configuration for a filepath which contains a given pattern.
    Parameters
    ---------
    config: dict containing the config.yaml contents
    submodel: string specifying submodel configuration to search
    re_pattern: regex pattern to search for in the input file paths
    """

    submodel_config = None
    for model_config in config["submodels"]:
        if model_config["name"] == submodel:
            submodel_config = model_config

    if submodel_config is None:
        raise RuntimeError(f"Configuration for submodel {submodel} not found in config.yaml")

    submodel_inputs = submodel_config["input"]

    matches = [path for path in submodel_inputs if re.search(re_pattern, path)]

    if len(matches) == 0:
        raise RuntimeError(
            f"No input files matching {re_pattern} found for submodel {submodel} in config.yaml"
            )
    elif len(matches) > 1:
        raise RuntimeError(
            f"Multiple input files matching {re_pattern} found for submodel {submodel} in config.yaml"
            )

    return Path(matches[0])


def stashmaster_from_config(config):
    """
    Find the path to the STASHmaster_A file using the input paths in the config.yaml
    """
    # The config.yaml specifies a higher level "stash" directory. Search it for STASHmaster_A
    stash_dir = input_path_from_config(config, "atmosphere", "stash")
    stashmasters_found = list(stash_dir.rglob("STASHmaster_A"))

    if len(stashmasters_found) == 0:
        raise RuntimeError(
            f"No STASHmaster_A file found in stash directory {stash_dir}."
        )
    elif len(stashmasters_found) > 1:
        raise RuntimeError(
            f"Multiple STASHmaster_A files found in stash directory {stash_dir}."
        )

    return stashmasters_found[0]


def adjust_restart_for_landcover(input_restart,
                                 output_restart,
                                 stashmaster_file,
                                 vegetation_map,
                                 config):
    """
    Driver function for adjusting UM restart land fields for compatibility
    with a new vegetation map.

    Parameters
    ----------
    input_restart: initial restart to perform the adjustments on
    output_restart: path to write modified restart to
    stashmaster_file: path to STASHmaster file for matching variable names and codes
    config: path to configuration file for the remapping function
    """

    # Convert UM restart to netCDF
    restart_as_nc = tempfile.NamedTemporaryFile().name
    convert_restart(input_restart, restart_as_nc, stashmaster_file)

    # Adjust land fields in netCDF based on new vegetation map
    remapped_restart_nc = tempfile.NamedTemporaryFile().name
    run_vegetation_remapping(
        input=str(restart_as_nc),
        output=str(remapped_restart_nc),
        vegetation_map=vegetation_map,
        # Use time index 0 from the vegetation mapping file
        time_index=0,
        config=config,
        # Only add data for newly active tiles
        fill_all=False,
        # Keep the previous years land fractions already in the restart
        use_previous_fractions_from_restart=True
    )

    # Write the updated land data into a UM restart file
    um_file = open_fields_file(
        str(input_restart),
        stashmaster_file,
        # Modifications will be applied to section 0
        section=0
    )

    nc_data = xarray.open_dataset(remapped_restart_nc, decode_times=False)

    # The netCDF and original restart use the same variable names
    variable_map = {var: var for var in nc_data.data_vars}

    replace_fields(
        um_file=um_file,
        variable_map=variable_map,
        nc_file=nc_data,
        outfile=output_restart,
        # Use time index 0 from nc_file
        time_index=0,
    )



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


    # Step 2: Adjust restart for new land cover
    remapped_restart_um = tempfile.NamedTemporaryFile().name
    stashmaster_path = stashmaster_from_config(config)
    land_cover_file = input_path_from_config(config, "atmosphere", r"ACCESS_vegfrac_scen_(?P<scenario>\w{1,2}).nc")

    adjust_restart_for_landcover(
        input_restart=str(atm_restart),
        output_restart=str(remapped_restart_um),
        stashmaster_file=str(stashmaster_path),
        vegetation_map=land_cover_file,
        config=REMAP_CONFIG
    )


    # Step 3: Add initial scenario wood thinning data to the restart
    thinning_file = input_path_from_config(config, "atmosphere", r"ACCESS_forest_thinning_frac_scen_(?P<scenario>\w{1,2}).nc")

    insert_thinning(
        restart_file=str(remapped_restart_um),
        thinning_file=thinning_file,
        stashmaster_file=str(stashmaster_path)
    )


    # Move the modified restart to the final location
    shutil.move(remapped_restart_um, atm_restart)

    # Add the new restart path to the config.yaml
    update_config(output_restart, config)

    # Commit the changes to the runlogs
    commit_config(input_restart, output_restart)
