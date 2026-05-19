The abrupt-4xCO2 configuration simulates the climate under an abrupt quadrupling of atmospheric CO2 concentrations compared to the preindustrial level.

The configuration is identical to the [piControl](/configs_experiments/configurations/piControl) configuration aside from an increased CO2 mass mixing ratio and the restart file used.
This configuration is used for the [CMIP7 abrupt-4xCO2 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/rec5WFkbODaOVdx9s), which can be used to understand feedbacks and a model's climate equilibrium climate sensitivity.

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs
The abrupt-4xCO2 configuration uses the same input files as the [piControl](/configs_experiments/configurations/piControl) other than the initial conditions.

### Restart
The abrupt-4xCO2 configuration uses the restart from the end of the 100th year of the piControl experiment.


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