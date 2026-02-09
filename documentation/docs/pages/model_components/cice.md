
## CICE5

In ACCESS-ESM1.6, the sea ice component is CICE5 [@hunke2015cice] updated from CICE4 used in ACCESS-ESM1.5.

Scientifically the sea ice model is configured the same as ESM1.5 [@Ziehn2020]. The scientific configuration is summarised as follows:

- Zero-layer thermodynamics (Semtner 1976)
    - One layer of snow and one layer of ice
    - UM calculates ice surface temperature, and conductive heat flux into the sea-ice
- Ice transport - Lipscomb (2001) and ridging – Rothrock (1975)
- Internal Ice Stress follow EVP (Hunke and Dukowicz, 2002)

There are significant improvements to diagnostics to support CMIP style diagnostics [@notz_cmip6_2016][@egusphere-2025-3083] natively and error handling.

## Meltwater Runoff

Like ESM1.5, the OASIS3-MCT coupler is used and the sea ice model acts as the interface between the atmosphere and ocean models. The only significant change to this interface since ESM1.5 is changes to meltwater from Antarctica and Greenland. As there is no ice sheet model, the volume of meltwater discharge from Antarctica and Greenland is equal to the instantaneous precipitation over each continent. In ESM1.6, this is partially discharged at the coastline of each continent (to represent ice shelf basal melt) and partially spread in open ocean (to represent melt from icebergs). In ESM1.5 all meltwater is at the coastlines. In addition, the latent heat to melt this water is now taken from the ocean. Meltwater runoff is configured in the `input_ice.nml` [namelist](https://github.com/ACCESS-NRI/access-esm1.6-configs/blob/dev-preindustrial%2Bconcentrations/ice/input_ice.nml#L14-L25) with a prescribed pattern from the [ice discharge](https://github.com/ACCESS-NRI/access-esm1.6-configs/blob/13cc7d229b0d4bda193879b8b30cde3441d61bec/config.yaml#L98) input file.

## References

\bibliography
