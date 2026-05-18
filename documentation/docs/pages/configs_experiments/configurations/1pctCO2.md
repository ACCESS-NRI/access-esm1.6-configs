The 1pctCO2 configuration simulates the climate under a yearly 1% increase in CO2 concentrations, starting from preindustrial conditions.

The configuration matches the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations) configuration with changes for prescribing the yearly CO2 increase and changes to the initial conditions.

This configuration is used for the [CMIP7 1pctCO2 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recdrTGc9OOrRF1rU).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs
The 1pctCO2 configuration uses the same input files as the preindustrial+concentrations configuration other than the initial conditions, which are taken from the 100th restart from the piControl experiment.

## Key settings
The yearly 1% increase in atmospheric CO2 concentrations is configured in the `atmosphere/namelists` file. Under the `&CLIMCHFG` section, an initial concentration and year are specified along with a rate of increase to apply for the following years.

The following differences are shown with respect to the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations) configuration:

#### atmosphere/namelists
```diff
 &CLMCHFCG
- L_CLMCHFCG=.FALSE.,
+ L_CLMCHFCG=.TRUE.,
+ CLIM_FCG_NYEARS(1)= 1,
+ CLIM_FCG_YEARS(1,1)=200,
+ CLIM_FCG_LEVLS(1,1)=4.3189e-04,
+ CLIM_FCG_RATES(1,1)= 1.00000,
+ CLIM_FCG_NYEARS(2:11)=10*0,
 /
```
In the above:

* `L_CLMCHFCG=.TRUE.` enables time varying prescribed greenhouse gas concentrations.
* `CLIM_FCG_NYEARS(1)= 1` indicates that one year of prescribed CO2 concentrations will be provided.
* `CLIM_FCG_YEARS(1,1)=200` indicates that the CO2 concentrations are provided for calendar year 200.
* `CLIM_FCG_LEVLS(1,1)=4.3189e-04` sets the CO2 mass mixing ratio for calendar year 200.
* `CLIM_FCG_RATES(1,1)= 1.00000` tells the model to apply a 1% increase to the CO2 concentration for each year after the last provided prescribed value.
* `CLIM_FCG_NYEARS(2:11)=10*0` tells the model that time varying values are not being provided for the other greenhouse gasses. Their values are instead taken from the `&RUN_Radiation` section.

With these settings, the model applies a 1% increase in CO2 concentrations for each year following the calendar year set in `CLIM_FCG_YEARS(1,1)=200`, so that calendar year 201 uses a concentration of `4.3189e-04*1.01=4.362089e-04`, calendar year 202 uses `4.3189e-04*1.01^2=4.4057098e-04` and so on. The year in the namelist has been set to 200, as the initial restart files used by the configuration have a calendar year of 201. It's important for the dates in the initial restart to be one year greater than the value set for `CLIM_FCG_YEARS(1,1)`, otherwise the incorrect increases in CO2 concentrations will be applied.

The values for other greenhouse gas concentrations, volcanic forcings, and the solar constant are indentical to the [preindustrial+concentrations](/configs_experiments/configurations/preindustrial+concentrations) configuration.

## Configuration scripts
The 1pctCO2 configuration includes a `check_co2_year.py` userscript which is run during the payu setup stage. This checks during the first run that the restart year is one year greater than the value set for `CLIM_FCG_YEARS(1,1)`, and produces an error otherwise. 

!!! warning

    This check will not work properly if the payu run index is customised with the `payu run -i` option.