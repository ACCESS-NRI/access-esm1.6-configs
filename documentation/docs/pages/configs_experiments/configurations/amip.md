The amip configuraton is an atmosphere-land configuration of ESM1.6, used to simulate atmospheric conditions between 1979-2022 using prescribed sea surface temperatures, sea ice concentrations, and atmospheric forcings. This configuration does not include interactive ocean and sea ice models.

The amip configuration is set up from the [historical](/configs_experiments/configurations/historical) configuration by deactivating ocean and sea ice models and disabling the coupler.

This configuration is used for the [CMIP7 amip experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recPovziGiiALZQUj).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.


## Inputs
The amip configuration uses the same atmosphere and land input files as the [historical](/configs_experiments/configurations/historical) configuration to provide time varying forcings to the atmosphere and land models for years 1979-2022.

### Atmosphere
Two additional files provide observed sea surface temperatures and sea ice concentrations to the atmosphere model:

* sst_amip_n96_gregorian.anc: Sea surface temperatures in units K, with values adjusted via the [Karl Taylor procedure](https://pcmdi.llnl.gov/report/pdf/60.pdf).
* seaice_amip_n96_gregorian.anc : Sea ice concentrations in units [0,1], with values adjusted via the [Karl Taylor procedure](https://pcmdi.llnl.gov/report/pdf/60.pdf).

### Restart
The amip configuration uses the 1978 atmosphere restart file produced by the historical experiment after removal of the coupling related fields. Ocean, sea ice, and coupler restart files are removed.

## Key settings

Settings are copied from the [historical](/configs_experiments/configurations/historical) configuration with changes to deactivate the coupling, to add prescribed SSTs and sea ice concentrations, and to deactivate the coupled CO2 tracers.


The following differences are shown with respect to the [historical](/configs_experiments/configurations/historical) configuration.

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
The `L_SICE/L_SSICE` options control how the sea ice albedo is calculated in the atmosphere model. The `&UPANCA` lines set the frequency at which the atmosphere model updates its sea ice fraction (`ANC_REF_NO=27`) and sea surface temperature (`ANC_REF_NO=28`) via linear interpolation (see details on the linear interpolation in the [esm-historical](/configs_experiments/configurations/esm-historical/#greenhouse-gas-emissions-and-concentrations) configuration). Sea ice depth (`ANC_REF_NO=29`) is calculated in the model, at the frequency specified here, based on the prescribed concentration. 


#### atmosphere/um_env.yaml
```diff
+ SSTIN: INPUT/sst_amip_n96_gregorian.anc
+ SICEIN: INPUT/seaice_amip_n96_gregorian.anc
```
The above settings point the model to the SST and sea ice concentration ancillary files in the `payu` work directory.

### Deactivating tracers
Coupled ESM1.6 configurations include two 3D atmospheric tracers which track atmospheric CO2 originating from the land and ocean respectively.
These tracers aren't used in the amip configuration and are deactivated with the following changes:

#### atmosphere/namelists
```diff
&NLSIZES
...
-TR_VARS=0,
+TR_VARS=2,

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
The following settings relate to the OASIS coupler used to couple the atmosphere, ocean, and sea ice submodels. As the coupling isn't used in the amip configuration, they are either deactivated or removed:

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

The amip configuration uses the same land use change userscript as the [historical](/configs_experiments/configurations/historical) configuration to update surface type fractions at the end of each year.