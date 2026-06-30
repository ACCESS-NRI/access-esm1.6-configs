import argparse
import git
from ruamel.yaml import YAML
from pathlib import Path
import shutil
import shlex
import subprocess
import re
import tempfile


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Copy and modify a 1978 ESM1.6 historical experiment restart directory for use as the"
            "initial condition in an amip simulation. This includes:\n"
            " - Removing the ocean, ice, and coupler restart files\n"
            " - Removing coupling fields from the atmosphere restart dump\n"
            "The initial restart path is taken from the config.yaml, and the output restart path is specified as an argument."
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


def remove_non_atm_restarts(restart_dir):
    """Remove restart files for the ocean, ice and coupler."""
    shutil.rmtree(restart_dir / "ocean")
    shutil.rmtree(restart_dir / "ice")
    shutil.rmtree(restart_dir / "coupler")


def subset_atmosphere_restart(restart_dump):
    """Remove coupling fields from a UM restart. Changes file in place."""
    # See https://forum.access-hive.org.au/t/create-an-amip-restart-from-a-coupled-restart/5261 for backround
    exclude_list = "95,171,172,173,174,176,177,178,179,180,181,184,185,186,187,188,189,192,250,413,414,415,416,33001,33002"
    tmp = tempfile.NamedTemporaryFile()
    cmd = f"python scripts/um_fields_subset.py {restart_dump} --exclude {exclude_list} --output {tmp.name}"
    print(cmd)
    subprocess.check_call(shlex.split(cmd))
    shutil.copy(tmp.name, restart_dump)


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
        " * Ocean, sea ice and coupler restart files removed.\n"
        " * Coupling fields removed from atmosphere restart file."
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

    remove_non_atm_restarts(output_restart)
    subset_atmosphere_restart(output_restart / "atmosphere" / "restart_dump.astart")

    update_config(output_restart, config)
    commit_config(input_restart, output_restart)
