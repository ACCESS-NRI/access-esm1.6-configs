!!! warning

    The ACCESS-ESM1.6 esm-flat10 experiment does not have a released and maintained configuration. These notes describe how the CMIP7 experiment was set up and are for reference only. If you would like to run an esm-flat10 experiment with the latest configuration updates, please create a *help request* on the [ACCESS Hive Forum](https://forum.access-hive.org.au/t/support-faq-frequently-asked-questions/1021).

The esm-flat10 experiment simulates the climate under constant anthropogenic emissions of 10PgC/year using a fully interactive carbon cycle, with preindustrial values used for all other atmospheric forcings. This experiment is run for the [CMIP7 esm-flat10 experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recwxXNVh0JIDr1B9).

## Inputs
The esm-flat10 experiment uses the same input files as the [esm-piControl](/configs_experiments/configurations/esm-piControl) configuration, with changes for specifying CO2 emissions and a different initial condition.

### Atmosphere:
The following file is used to provide the constant CO2 emissions to the atmosphere model:

* CO2_fluxes_flat10.anc: Constant gridded CO2 emissions in units kg(CO2) m-2 s-1, totalling 10Pg(C) year-1.

### Restart
The esm-flat10 experiment uses the restart from the end of the 200th year of the esm-piControl experiment.

## Key settings
The following settings are used to read the CO2 emissions from the input file. Differences are shown with respect to the [esm-piControl](/configs_experiments/configurations/esm-piControl) configuration:

#### um_env.yaml
````diff
+CO2EMITS: INPUT/CO2_fluxes_flat10.anc
````
The above setting points the model to the CO2 emissions ancillary file in the `payu` work directory.

#### atmosphere/namelists 
```diff
+ L_CO2_EMITS= .TRUE.,
...
+ &UPANCA ANC_REF_NO=78, PERIOD=4, INTERVAL=1 /
```
The above settings activate the CO2 emissions fluxes and control the linear interpolation of the CO2 emissions ancillary data. See the [esm-historical](/configs_experiments/configurations/esm-historical/#greenhouse-gas-emissions-and-concentrations) configuration for details on controling the linear interpolation.

