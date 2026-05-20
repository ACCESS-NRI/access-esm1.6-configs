The esm-piControl configuration of ESM1.6 simulates the climate prior to the industrial revolution using a fully interactive carbon cycle where 3D CO2 tracers evolve freely in the atmosphere and are exchanged with the land and ocean biogeochemistry submodels.

This configuration largely matches the [preindustrial](/configs_experiments/configurations/preindustrial) configuration, with changes to activate the interactive carbon cycle and remove the prescribed CO2 concentrations.

This configuration is used for the [CMIP7 esm-piControl experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recXseEQjRxRbwnOT).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs
The esm-piControl configuration uses the same input files as the [piControl](/configs_experiments/configurations/piControl) configuration in order to provide the model with 1850 atmospheric forcings.

### Restart
The esm-piControl configuration uses a restart from the end of the emissions driven model spinup.


## Key settings
The esm-piControl configuration uses the same settings as the [piControl](/configs_experiments/configurations/piControl) configuration, with changes for activating the interactive carbon cycle.

The following settings are changed, with respect to the [piControl](/configs_experiments/configurations/piControl) configuration, in order to switch on the interactive carbon cycle.


#### atmosphere/namelists
```diff
- L_CO2_INTERACTIVE=.FALSE.,
+ L_CO2_INTERACTIVE=.TRUE.,
+ L_CO2_MASS=.TRUE.,
```
The `L_CO2_INTERACTIVE` flag activates the interactive carbon cycle. It enables the coupling between 3D CO2 tracers in the atmosphere with the
ocean BGC and CABLE land model, and configures the radiation calculations to use the 3D CO2 tracers. When `L_CO2_interactive` is `.TRUE.`, the`CO2_MMR` option is ignored.

The `L_CO2_MASS` option applies a mass correction to the 3D CO2 tracer in the lower model levels to improve conservation of the total CO2 mass during
each model timestep.
