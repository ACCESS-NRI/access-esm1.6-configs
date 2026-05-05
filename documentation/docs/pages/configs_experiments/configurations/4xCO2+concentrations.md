The 4xCO2+concentrations configuration simulates the climate under an abrupt quadrupling of atmospheric CO2 concentrations compared to the preindustrial level.

The configuration is identical to the preindustrial+concentrations configuration aside from an increased CO2 mass mixing ratio and the restart file used.
This configuration is used for the [CMIP7 abrupt-4xCO2 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/rec5WFkbODaOVdx9s).


## Inputs
The 4xCO2+concentrations configuration uses the same input files as the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations) configuration.

## Key settings
The increased CO2 concentration is set in the `atmosphere/namelists` configuration file. The following difference is shown with respect to the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations)
configuration.

#### atmosphere/namelists
```diff
 &RUN_Radiation
 ...
- CO2_MMR= 4.3189e-04,
+ CO2_MMR= 1.72756e-03,
```

The values for other greenhouse gas concentrations, volcanic forcings, and the solar constant are indentical to the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations) configuration.