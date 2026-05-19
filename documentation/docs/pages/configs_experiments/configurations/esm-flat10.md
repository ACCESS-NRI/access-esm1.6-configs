The esm-flat10 configuration simulates the climate under constant anthropogenic emissions of 10PgC/year using a fully interactive carbon cycle, with preindustrial values used for all other atmospheric forcings.

This configuration is used for the [CMIP7 esm-flat10 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recwxXNVh0JIDr1B9).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs
The esm-flat10 configuration uses the same input files as the [esm-piControl](/configs_experiments/configurations/esm-piControl) configuration, with changes for specifying CO2 emissions and a different initial condition.

### Atmosphere:
The following file is used to provide the constant CO2 emissions to the atmosphere model:

* CO2_fluxes_flat10.anc

### Restart
The esm-flat10 configuration uses the restart from the end of the 200th year of the esm-piControl experiment.

## Key settings
The following settings are used to read the CO2 emissions from the input file. Differences are shown with respect to the [esm-piControl](/configs_experiments/configurations/esm-piControl) configuration:

#### atmosphere/namelists 
```diff
+ L_CO2_EMITS= .TRUE.,
...
+ &UPANCA ANC_REF_NO=78, PERIOD=4, INTERVAL=1 /
```
See the [esm-historical](/configs_experiments/configurations/esm-historical/#greenhouse-gas-emissions-and-concentrations) configuration for details on controling the linear interpolation of ancillary data.