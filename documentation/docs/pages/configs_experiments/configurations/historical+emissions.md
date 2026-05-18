The historical+emissions configuration simulates the climate from 1850-2022 using a fully interactive carbon cycle and historical CO2 anthropogenic emissions data.

This configuration is used for the [CMIP7 esm-historical experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recIoJ9zT1p7yrD6w).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs
The same input files as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration are used to provide the model with time varying aerosol, ozone, nitrogen deposition, volcanic forcing, solar irradiance and land use change data.
An additional input file contains time varying anthropogenic CO2 emissions:

* CO2_fluxes_1849_2023_cmip7.anc

The esm-historical configuration uses a restart from the esm-piControl experiment.

## Key settings
The historical+emissions configuration uses the same settings as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration, with changes for activating the interactive carbon cycle and external emissions file. 

### Greenhouse gas emissions and concentrations
As with the [preindustrial+emissions](/configs_experiments/configurations/preindustrial+emissions) configuration, the following settings activate the interactive carbon cycle. The following differences are shown with respect to the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration:

#### atmosphere/namelists
```diff
- L_CO2_INTERACTIVE=.FALSE.,
- L_CO2_MASS=.FALSE.,
+ L_CO2_INTERACTIVE=.TRUE.,
+ L_CO2_MASS=.TRUE.,
```

To enable an external CO2 emissions file, the following lines are added:
```diff
+ L_CO2_EMITS= .TRUE.,
...
+ &UPANCA ANC_REF_NO=78, PERIOD=4, INTERVAL=1 /
```
The UM linearly interpolates input data supplied at monthly frequencies to higher frequencies for use during the simulation. The line `&UPANCA ANC_REF_NO=78, PERIOD=4, INTERVAL=1 /` controls this interpolation for the CO2 emissions ancillary file (`ANC_REF_NO=78`). The `PERIOD` setting specifies the units for the update frequency (`1`: years, `2`: months, `3`: days, `4`: hours) and the `INTERVAL` specifies the update frequency in these units. Here, the CO2 emissions data are updated in the model via linear interpolation every 1 hour.

All other greenhouse gas concentrations are prescribed and use the same values as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration. For clarity, the specification of the CO2 concentrations is removed:

#### atmosphere/namelists
```diff
&CLMCHFCG
...
- CLIM_FCG_NYEARS = 174, 174, 174, 174, 174, 174, 174, 174, 174, 174,...
+ CLIM_FCG_NYEARS = 0, 174, 174, 174, 174, 174, 174, 174, 174, 174,...
...
- CLIM_FCG_YEARS(:,1) = 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857,...
- CLIM_FCG_LEVLS(:,1) = 4.317926e-04, 4.319855e-04, 4.321797e-04, ...
```

## Configuration scripts
The historical+emissions configuration uses the same land use change userscript as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration to update surface type fractions at the end of each year:

#### config.yaml
```yaml
userscripts:
    # Apply land use changes after each run
    run: ./scripts/update_landuse_driver.sh
```
Note that this script requires the run length to be 1 year in order to work properly. 