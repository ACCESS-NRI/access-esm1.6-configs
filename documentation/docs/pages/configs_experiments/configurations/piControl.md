The piControl configuration simulates the climate prior to the industrial revolution using prescribed CO2 concentrations and atmospheric forcings
estimated for the year 1850.

This configuration is used for the [CMIP7 piControl experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/rec2OC1Xh1nh4lsNB).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.


## Inputs

### Atmosphere
The following input files provide external forcings for 1850 to the atmosphere model. Each file contains 12 months of data which are repeated each year in the model:

* OCFF_1850_cmip7.anc: Organic carbon? **TO CHECK**
* BC_1850_cmip7.anc: Black carbon ? **TO CHECK**
* scycl_1850_cmip7.anc: SO2 concentrations given as the max mixing ratio of of S **TO CHECK**
* Bio_1850_cmip7.anc: Biomass burning emissions **TO CHECK**
* biogenic_351sm.N96L38: Biogenic aerosols? **TO CHECK**
* sulpc_oxidants_N96_L38:  ? **TO CHECK**
* DMS_conc.N96: ? **TO CHECK**
* ozone_1850_cmip7.anc: Zonal mean ozone mass mixing ratios

### Land
The following input files provide data to the CABLE land surface model:

* Ndep_1850_cmip7.anc: Nitrogen deposition **TO CHECK**

Land surface type mappings for 1850 are derived from the LUH3 dataset and are included directly in the UM restart file.

### Restart file
The piControl configuration uses a restart file from the end of the model spin up.

## Key settings
Values for greenhouse gas concentrations, volcanic forcings, and the solar constant are set in the following atmosphere configuration files. Each value is treated as a global constant in the model.

#### atmosphere/namelists
```
 CO2_MMR= 4.3189e-04,
 O2MMR=    0.2314,
 N2OMMR= 4.1256e-07,
 CH4MMR= 4.4228e-07,
 C11MMR= 0.000000e+00,
 C12MMR= 0.000000e+00,
 C113MMR= 0.000000e+00,
 HCFC22MMR= 0.000000e+00,
 HFC125MMR= 0.000000e+00,
 HFC134AMMR= 0.000000e+00,
```

#### atmosphere/input_atm.nml
```
 SC=1361.617
 VOLCTS_val=135.2
```
