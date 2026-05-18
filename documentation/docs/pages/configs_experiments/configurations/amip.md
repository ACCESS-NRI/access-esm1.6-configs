The amip configuraton is an atmosphere only configuration of ESM1.6, used to simulate atmospheric conditions between 1979-2022 using prescribed sea surface temperatures, sea ice concentrations, and atmospheric forcings. This configuration does not include interactive ocean and sea ice models.

The amip configuration is set up from the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration by deactivating ocean and sea ice models and disabling the coupler.

This configuration is used for the [CMIP7 amip experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recPovziGiiALZQUj).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.


## Inputs
The amip configuration uses the same atmosphere and land input files as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration to provide time varying forcings to the the atmosphere and land models for years 1979-2022. Two additional files prescribe observed sea surface temperatures and sea ice concentrations:

* amip_sst_n96_greg.pp: Sea surface temperatures
* amip_seaice_n96_greg.pp: Sea ice concentrations

The amip configuration uses a restart from the historical+concentrations experiment.

## Key settings

Settings are copied from the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration with changes to deactivate the coupling, to add prescribed SSTs and sea ice concentrations, and to deactivate the coupled CO2 tracers.


The following differences are shown with respect to the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration:

### Prescribed SSTs and sea ice

The following settings configure the atmospheric model to use prescribed SSTs and sea ice concentrations from the input files:

#### atmosphere/namelists
```diff
&NLSIZES
...
- NICE=5,
+ NICE=1,

&NLSTCATM
- L_SSICE_ALBEDO=.TRUE.,
- L_SICE_MELTPONDS=.TRUE.,
- L_SICE_SCATTERING=.TRUE.,
- L_SICE_HADGEM1A=.TRUE.,
+ L_SSICE_ALBEDO=.FALSE.,
+ L_SICE_MELTPONDS=.FALSE.,
+ L_SICE_SCATTERING=.FALSE., 
+ L_SICE_HADGEM1A=.FALSE.,

&ANCILCTA
+ LAMIPII=.TRUE.,
...
+ &UPANCA ANC_REF_NO=27, PERIOD=3, INTERVAL=1 /
+ &UPANCA ANC_REF_NO=28, PERIOD=3, INTERVAL=1 /
+ &UPANCA ANC_REF_NO=29, PERIOD=3, INTERVAL=1 /
```
The `L_SICE/L_SSICE` options control how the sea ice albedo is calculated in the atmosphere model. The `&UPANCA` lines set the frequency at which the atmosphere model updates its sea ice fraction (`ANC_REF_NO=27`) and sea surface temperature (`ANC_REF_NO=28`) via linear interpolation. Sea ice depth (`ANC_REF_NO=29`) is calculated in the model based on the prescribed concentration, and is also updated at the frequency specified here. See the [historical+emissions](/configs_experiments/configurations/historical+emissions/#greenhouse-gas-emissions-and-concentrations) configuration for details on controling the linear interpolation.


#### atmosphere/um_env.yaml
```diff
+ SSTIN: INPUT/amip_sst_n96_greg.pp
+ SICEIN: INPUT/amip_seaice_n96_greg.pp
```
The above settings point the model to the SST and sea ice concentration ancillary files in the `payu` work directory.

### Deactivating tracers
Coupled ESM1.6 configurations include two 3D atmospheric tracers which track atmospheric CO2 originating from the land and ocean respectively.
These tracers aren't used in the amip configuration and are deactivated with the following changes:

#### atmosphere/namelists
```diff
&STSHCOMP
...
-TCA=2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
+TCA=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,

&NLSTCATM
- L_BL_TRACER_MIX=.TRUE.,
+ L_BL_TRACER_MIX=.FALSE.,

- L_CO2_TRACER=.TRUE.,
- L_TRACER_MASS=.TRUE.,
+ L_CO2_TRACER=.FALSE.,
+ L_TRACER_MASS=.FALSE.,
```


### Deactivating coupling
The following settings relate to the oasis coupling used to couple the atmosphere, ocean, and sea ice submodels. As the coupling isn't used in the amip configuration, they are either deactivated or removed:

#### atmosphere/um_env.yaml
```diff
- AUSCOM_CPL: 'true'
+ AUSCOM_CPL: 'false'
```

#### atmosphere/namelists
```diff
- L_OASIS=.TRUE.,
+ L_OASIS=.FALSE.,
```

#### atmosphere/input_atm.nml
```diff
&coupling
- access_tfs=-1.8
- xfactor=1.0
- ocn_sss=.false.
- sdump_enable=.false.
- rdump_enable=.false.
 ocean_albedo_factor=0.92
```


## Configuration scripts

The amip configuration uses the same land use change userscript as the [historical+concentrations](/configs_experiments/configurations/historical+concentrations) configuration to update surface type fractions at the end of each year:

#### config.yaml
```yaml
userscripts:
    # Apply land use changes after each run
    run: ./scripts/update_landuse_driver.sh
```
Note that this script requires the run length to be 1 year in order to work properly. 

