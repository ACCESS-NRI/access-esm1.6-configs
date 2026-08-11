!!! warning

    The ACCESS-ESM1.6 abrupt-4xCO2 experiment does not have a released and maintained configuration. These notes describe how the CMIP7 experiment was set up and are for reference only. If you would like to run an abrupt-4xCO2 experiment with the latest configuration updates, please create a *help request* on the [ACCESS Hive Forum](https://forum.access-hive.org.au/t/support-faq-frequently-asked-questions/1021).


The abrupt-4xCO2 experiment simulates the climate under an abrupt quadrupling of atmospheric CO2 concentrations compared to the preindustrial level, and has been run for the [CMIP7 abrupt-4xCO2 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/rec5WFkbODaOVdx9s)

The experimental setup matches commit [37d5312](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/37d5312847642f1ea574306d200449aa8b44fd39) from the [piControl](/configs_experiments/configurations/piControl) configuration with changes to the prescribed CO2 mass mixing ratio and the restart file used.

## Inputs
The abrupt-4xCO2 experiment uses the same input files as the [piControl](/configs_experiments/configurations/piControl) other than the initial conditions.

### Restart
The abrupt-4xCO2 experiment uses the restart from the piControl experiment with calendar year 201.


## Key settings
The increased CO2 concentration is set in the `atmosphere/namelists` configuration file. The following difference is shown with respect to the [piControl](/configs_experiments/configurations/piControl)
configuration.

#### atmosphere/namelists
```diff
 &RUN_Radiation
 ...
- CO2_MMR= 4.3189e-04,
+ CO2_MMR= 1.72756e-03,
```

The values for other greenhouse gas concentrations, volcanic forcings, and the solar constant are indentical to the [piControl](/configs_experiments/configurations/piControl) configuration.