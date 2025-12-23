# Check that base year for CO2 increase is consistent with the UM restart year

import os, f90nml, yaml

if int(os.environ['PAYU_CURRENT_RUN']) == 0:
    # Only check on the first run
    nml = f90nml.read('work/atmosphere/namelists')
    co2_year = nml['clmchfcg']['clim_fcg_years'][0][0]

    with open('work/atmosphere/um.res.yaml', 'r') as calendar_file:
        date_info = yaml.safe_load(calendar_file)
    restart_year = date_info['end_date'].year
    print("Restart year", restart_year)

    # Want first year to have a 1% increase, so co2_year should be restart_year - 1
    if co2_year != (restart_year - 1):
        raise ValueError(
            f"ERROR: clim_fcg_years in atmosphere/namelists is {co2_year}. "
            f"For consistency with restart year use {restart_year-1}"
        )
