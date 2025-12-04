# 1pctCO2
Test configuration for a coupled CO<sub>2</sub> concentration driven [ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6)  with 1% year CO2 increase.

Note that `CLIM_FCG_YEARS(1,1)` in `atmosphere/namelists` must be set to one year less than the initial year of the run
(e.g. the year number in `atmosphere/um_res.yaml` in the restart directory) so that the first increase is applied at the start of the new run.

When set correctly the output file `atm.fort6.pe0` for the first year should have
```
GHG concentrations (mmr) for model year  YYYY
CO2     0.43621E-03
```
i.e. 1.01 * initial value of 4.3189e-04.

For usage instructions, see the [ACCESS-Hive docs](https://access-hive.org.au/models/run-a-model/run-access-esm/)

## Conditions of use

`<TO DO>`
