The flat10 configuration simulates the climate under constant anthropogenic emissions of 10PgC/year using a fully interactive carbon cycle, with preindustrial values used for all other atmospheric forcings.

This configuration is used for the CMIP7 esm-flat10 experiment.


## Inputs
The flat10 configuration uses the same input files as the [preindustrial+emissions](/configs_experiments/configurations/preindustrial+emissions) configuration, with an extra file to provide the constant CO2 emissions data:

* CO2_fluxes_flat10.anc

## Key settings
The following settings are used to read the CO2 emissions from the input file. Differences are shown with respect to the [preindustrial+emissions](/configs_experiments/configurations/preindustrial+emissions) configuration:

#### atmosphere/namelists 
```diff
+ L_CO2_EMITS= .TRUE.,
...
+ &UPANCA ANC_REF_NO=78, PERIOD=4, INTERVAL=1 /
```
See the [historical+emissions](/configs_experiments/configurations/historical+emissions/#greenhouse-gas-emissions-and-concentrations) configuration for details on controling the linear interpolation of ancillary data.