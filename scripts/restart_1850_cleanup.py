#!/usr/bin/env python3

# Remove the archived 1850 ice restart at the end of the first run.

# Payu's archive step for CICE deletes previous restarts based on the files in the
# original restart directory. As the setup scripts change the name of the restart,
# it is not properly cleaned up. This script performs the extra clean up.


import os
from pathlib import Path


def main():
    current_run = int(os.environ.get("PAYU_CURRENT_RUN"))

    # Only need to clean up the restart on the first run. This will not work
    # if the run numbers are changed via "payu run -i"
    if current_run != 0:
        return

    restart_dir = Path(os.environ.get("PAYU_CURRENT_RESTART_DIR"))

    iced_1850 = restart_dir / "ice" / "iced.1850-01-01-00000.nc"

    if iced_1850.is_file():
        print(f"Removing 1850 ice restart: {iced_1850}")
        iced_1850.unlink()


if __name__ == "__main__":
    main()
