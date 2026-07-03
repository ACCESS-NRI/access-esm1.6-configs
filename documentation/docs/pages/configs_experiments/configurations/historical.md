The historical configuration simulates the climate from 1850-2022 using prescribed atmospheric CO2 concentrations and forcings.

This configuration is used for the [CMIP7 historical experiment](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7/viwUXPlXGkKPiFTgB/recssLjHtzInmosrl).

Please note that the settings described below are implemented in the configuration and no further changes are required to run it. The descriptions below are included to aid in understanding of the configuration and to assist with making modifications.

## Inputs

### Atmosphere

The following input files provide time varying external conditions to the atmosphere model for years 1850-2022:

* OCFF_1849_2023_cmip7.anc: Organic carbon (OC) anthropogenic emissions in kg(C) m-2 s-1.
* BC_1849_2023_cmip7.anc: Black carbon (BC) anthropogenic emissions in kg(C) m-2 s-1.
* scycl_1849_2023_cmip7.anc: SO2 anthropogenic emissions, reported in kg(S) m-2 s-1. Split into emissions for low and high model levels. Contains a separate variable for climatological anthropogenic DMS emissions in kg(S) m-2 s-1.
* Bio_1849_2023_cmip7.anc: Fire emissions of OC and BC in kg(C) m-2 s-1. Split into emissions for low and high model levels.
* ozone_1849_2023_cmip7.anc: Zonal mean ozone mass mixing ratio used in atmosphere radiation calculations.
* volcts_cmip7.dat: Volcanic forcing given as optical depths for 550nm, multiplied by 10000.
* TSI_CMIP7_ESM: Yearly mean total solar irradiance at 1 AU in units W m-2.

The following files are carried over from the [piControl](/configs_experiments/configurations/piControl) configuration and provide 12 months of data which
are repeated in the model:

* biogenic_351sm.N96L38: Climatological mass mixing ratios of biogenic aerosols.
* sulpc_oxidants_N96_L38: Climatological OH, HO2, H2O2, and Ozone MMRs, used in sulphur cycle chemistry calculations.
* DMS_conc.N96: Dimethyl sulphide concentration in seawater given in nmol l-1.

### Land
The following input files provide time varying conditions to the land model for years 1850-2022:

* Ndep_1849_2023_cmip7.anc: Nitrogen deposition in g(N) m-2 day-1.
* ACCESS_vegfrac_LUH3_states_withAusPFTs_1850-2023_v7-transposed.nc: Land surface type fractions derived from the LUH3 dataset.

### Restart
The historical configuration uses the restart from the piControl experiment with calendar year 201. The year in the restart has been changed to 1850 for use in the historical configuration.


## Key settings

The following differences are shown with respect to the [piControl](/configs_experiments/configurations/piControl) configuration

### Greenhouse gas concentrations
To implement time varying greenhouse gas concentrations, the constant concentrations in the *&RUN_Radiation* section are replaced with unused placeholder values. 
#### atmosphere/namelists
```diff
&RUN_Radiation
- CO2_MMR= 4.3189e-04,
 O2MMR=    0.2314,
- N2OMMR= 4.1256e-07,
- CH4MMR= 4.4228e-07,
- C11MMR= 0.000000e+00,
- C12MMR= 0.000000e+00,
- C113MMR= 0.000000e+00,
- HCFC22MMR= 0.000000e+00,
- HFC125MMR= 0.000000e+00,
- HFC134AMMR= 0.000000e+00,
+ CO2_MMR= -99999,
+ N2OMMR= -99999,
+ CH4MMR= -99999,
+ C11MMR= -99999,
+ C12MMR= -99999,
+ C113MMR= -99999,
+ HCFC22MMR= -99999,
+ HFC125MMR= -99999,
+ HFC134AMMR= -99999,
```

In the *&CLMCHFCG* section, the time varying GHG concentrations are activated
```diff
- L_CLMCHFCG = .FALSE.,
+ L_CLMCHFCG = .TRUE.,
```
and arrays are filled in for the number of years of data provided for each species (`CLIM_FCG_NYEARS`), the years provided for each species (`CLIM_FCG_YEARS`), and the prescribed mass mixing ratios for each species in each year (`CLIM_FCG_LEVLS`):

```diff
+ CLIM_FCG_NYEARS = 174, 174, 174, 174, 174, 174, 174, 174, 174, 174, 174,
...
+ CLIM_FCG_YEARS(:,1) = 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, ...
+ CLIM_FCG_YEARS(:,11) = 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, ...
...
+ CLIM_FCG_LEVLS(:,1) = 4.317926e-04, 4.319855e-04, 4.321797e-04, 4.323746e-04, ...
+ CLIM_FCG_LEVLS(:,11) = 0.000000e+00, 0.000000e+00, 0.000000e+00, ...
```

The 11 species are:

* `1`: CO2
* `2`: CH4
* `3`: N2O
* `4`: CFC-11
* `5`: CFC-12
* `6`: Unused
* `7`: Unused
* `8`: CFC-113
* `9`: HCFC-22
* `10`: HFC-125
* `11`: HFC-134A

Rates of increase (`CLIM_FCG_RATES`) for each greenhouse gas need to be set to a negative number. This ensures that the model uses the prescribed concentrations set in `CLIM_FCG_LEVLS` as negative rates are ignored.
```diff
+ CLIM_FCG_RATES(:,1) = -3.276800e+04, -3.276800e+04, -3.276800e+04, -3.276800e+04,...
+ CLIM_FCG_RATES(:,11) = -3.276800e+04, -3.276800e+04, -3.276800e+04, ...
```

## Solar and volcanic forcings
Time varying solar and volcanic forcings are activated in the `&NLSTCATM` section of the `atmosphere/namelists` file:

#### atmosphere/namelists
```diff
- L_SCVARY=.false.,
- L_VOLCTS_VARY=.false.,
+ L_SCVARY=.true.,
+ L_VOLCTS_VARY=.true.,
```
and paths to the input files (relative to the atmosphere work directory) are set in the `&FILENATFORCE` section:
```diff
- FILE_SCVARY  = '',
- FILE_VOLCTS  = ''
+ FILE_SCVARY  = 'INPUT/TSI_CMIP7_ESM',
+ FILE_VOLCTS  = 'INPUT/volcts_cmip7.dat'
```

### Land use change
The historical configuration includes a land use change (LUC) scheme, where land surface type fractions in the model are updated each year with data based on the LUH3 dataset. This is activated in the CABLE model namelist `atmosphere/cable.nml`:

#### atmosphere/cable.nml
```diff
! CASA-CNP flags
- l_luc = .FALSE.
+ l_luc = .TRUE.
```

The land use change scheme also requires a userscript to update the land surface type fractions for each year (see [below](#Configuration scripts)).

## Configuration scripts

Land use change data is not directly read by the model during simulations. Instead, new surface type fractions need to be inserted into the atmospheric restart produced at the end of each year. The historical configuration applies this using the following payu userscript:

#### config.yaml
```yaml
userscripts:
    # Apply land use changes after each run
    run: ./scripts/update_landuse_driver.sh
```

!!! warning

    This script requires the run length to be 1 year in order to work properly. 

