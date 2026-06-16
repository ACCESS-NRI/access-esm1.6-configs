!!! warning

    The ACCESS-ESM1.6 abrupt-4xCO2 experiment does not have a released and maintained configuration. These notes describe how the CMIP7 experiment was set up and are for reference only. If you would like to run an abrupt-4xCO2 experiment with the latest configuration updates, please create a *help request* on the [ACCESS Hive Forum](https://forum.access-hive.org.au/t/support-faq-frequently-asked-questions/1021).


The abrupt-4xCO2 experiment simulates the climate under an abrupt quadrupling of atmospheric CO2 concentrations compared to the preindustrial level, and has been run for the [CMIP7 abrupt-4xCO2 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/rec5WFkbODaOVdx9s)

The experiment uses the same settings as the [piControl](/configs_experiments/configurations/piControl) configuration aside from an increased CO2 mass mixing ratio and the restart file used.

## Inputs
The abrupt-4xCO2 experiment uses the same input files as the [piControl](/configs_experiments/configurations/piControl) other than the initial conditions.

### Restart
The abrupt-4xCO2 experiment uses the restart from the end of the 100th year of the piControl experiment.


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