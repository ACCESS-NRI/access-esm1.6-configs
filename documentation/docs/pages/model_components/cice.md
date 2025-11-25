# Sea Ice

In ACCESS-ESM1.6, the Sea Ice model component is CICE5.

This uses the zero layer thermodynamics etc ...

Arakawa B-grid

Results are very similar to CICE4. See issue

## Changing restart dates

## Diagnostics

As far as possible, the default configurations of ACCESS-ESM1.6 output diagnostics in 
the format requested for CMIP7 as native output.

### Masking over time and space

Intrinsic and extrinsic

`sitimefrac`

This has the impact that sometimes diagnostics between the sea ice and ocean may have the
same descriptions but be masked differently.

e.g. 

*Water Flux into Sea Water Due to Sea Ice Thermodynamics* 
 - siflfwbot is masked only where sea_ice (in time and space)
 - fsithem is in all wet cells
 both are reported in `kg m-2 s-1` but the areas and time they are calculated for are different

*Thickness*
- sivol is Sea-Ice Volume per Area, calculated using grid cell area
- sithick is a true Sea-Ice Thickness (alternative description would be Sea Ice Volume per Sea Ice Area)
both are repored in `m`

### Mass / Concentrations / Age

siage was reset to 0 at the start of the pi_control run ?

We use [fixed densities](https://github.com/ACCESS-NRI/cice5/blob/62dcb7ee19f6e0a71d4b8e3e548b8cece0b930cf/drivers/access/ice_constants.F90#L22-L29) for sea ice, sea water and snow:

```
    rhos      = 330.0_dbl_kind   ,&! density of snow (kg/m^3)
    rhoi      = 917.0_dbl_kind   ,&! density of ice (kg/m^3)
    rhow      = 1026.0_dbl_kind  ,&! density of seawater (kg/m^3)
```

You can also check these thorugh the diagnostics, for example

ds.simass/ds.siconc/ds.sithick = 917

Sea ice freeboad, thickness and snow thickness should balance to rounding error following Archimedes
principal of buoyancy

e.g. (in math)

sithick*rhoi+sisnthick*rhos = (sithick-sifb)*rhow

sithick, sisnthick, sifb are all weighted by siconc

Mass and volume terms should balance too: 

sivol*rhoi = simass (sivol and simass are grid cell averages)
sisnthick*rhos = sisnmass (sisnthick and sisnmass are ice area averages)
sivol = sithick*siconc <!-- I am confused about why this is true, as sithick is intrinsic-->

We use [fixed salinity](https://github.com/ACCESS-NRI/access-esm1.6-configs/blob/c150adbad53b3dc8ed4079fe2136cbb767fa0a63/ice/cice_in.nml#L46) for sea ice of 4 g/kg. Therefore: `sisalt = simass * 0.004`

$sivol*rhoi = simass $

### Temperatures

sitemptop is only available on the atmospheric grid ( UM stash code - s00i508)

sitempsnic is diagnostic only, and slightly approximate

sitempbot

### Heat Fluxes

sifswdbot is the penetrating shortwave which is zero in this model so is zero

siflcondtop and siflcondbot are equal with 0 layer themodynamics

There is heat flux no diagnostic for frazil melt potential but there is a diagnostic for
_Sea-Ice Mass Change Through Growth in Supercooled Open Water (Frazil)_ (`sidmassgrowthwat`)

We report these on the atmosphere grid as well:

```
sifllattop s03i234
sifllwdtop s02i501
sifllwutop s03i531
siflsenstop s03i533
siflswdtop s01i501
siflswutop s01i503
```

To-do:
- disable in CICE5
- check if these are masked by sea ice area


### Salt / Water Fluxes

sipr		Rainfall Rate over Sea Ice
siflfwbot		Freshwater Flux from Sea Ice

### Dynamics

As 

By convention - dynamics are reported on the native grid (e.g. velocity and speed)


On the A-grid
sidmassdyn	    Sea-Ice Mass Change from Dynamics
sidmasstranx	X-Component of Sea-Ice Mass Transport
sidmasstrany	Y-Component of Sea-Ice Mass Transport

Should all be on B-grid ?

sicompstren		compressive_strength_of_sea_ice	Compressive Sea Ice Strength
sistrxdtop		surface_downward_x_stress	X-Component of Atmospheric Stress on Sea Ice
sistrxubot		upward_x_stress_at_sea_ice_base	X-Component of Ocean Stress on Sea Ice
sistrydtop		surface_downward_y_stress	Y-Component of Atmospheric Stress on Sea Ice
sistryubot		upward_y_stress_at_sea_ice_base	Y-Component of Ocean Stress on Sea Ice

### Thermodynamics

Sea-Ice Heat Content (`sihc`)
Snow Heat Content (`sisnhc`) 

Evaporation terms are calculated within the atmosphere model, on the atmosphere grid,
these are conservatively regrid to the sea ice grid. Conservative regridding leads
to sign changes in some cells, leading to sea ice or snow mass gain due to evaporation/sublimation

Calculated for all time & wet cells
sidmassth		Sea-Ice Mass Change from Thermodynamics

is the sum of 

sidmassgrowthbot	Sea-Ice Mass Change Through Basal Growth
sidmassgrowthsi		Sea-Ice Mass Change Through Snow-to-Ice Conversion
sidmassgrowthwat	Sea-Ice Mass Change Through Growth in Supercooled Open Water (Frazil)
sidmassmeltbot		Sea-Ice Mass Change Through Bottom Melting
sidmassmeltlat		Sea-Ice Mass Change Through Lateral Melting
sidmassmelttop	    Sea-Ice Mass Change Through Surface Melting
sidmassevapsubl	Sea-Ice Mass Change Through Evaporation and Sublimation

There is no overall diagnostic for snow mass rate of change, however these should hemispherically sum to zero over a long run
if there is no snow accumulating:

sisndmassdyn		Snow Mass Rate of Change Through Advection by Sea-Ice Dynamics
sisndmassmelt		Snow Mass Rate of Change Through Melt
sisndmasssi		    Snow Mass Rate of Change Through Snow-to-Ice Conversion
sisndmasssnf		Snow Mass Change Through Snowfall
sisndmasssubl		Snow Mass Rate of Change Through Evaporation or Sublimation

Not reported as not a process in access-esm1.6:
sisndmasswind		Snow Mass Rate of Change Through Wind Drift of Snow

Variable for snow are generally masked for when there is sea ice (i.e. intrinsic)

In CICE, Snow-to-Ice conversion only occurs when the weight of the snow pushes the sea ice below the water level 
(i.e. freeboard is negative) and the mass of snow is directly converted to the mass of sea ice. The process is adiabiatic,
there is no energy exchanged in the process. However sidmassgrowthsi is greater than sisndmasssi as sidmassgrowthsi is extrinsic and sisndmasssi is intrinsic.

Similarly, `siflfwbot` doesn't balance with the relevant `sidmass` terms, as `siflwbot` is intrinsic.




### Hemispheric Scalars

Diagnostics which do not have a spatial coordinate are only available via post-processings:

siareaacrossline			sea_ice_area_transport_across_line	Sea-Ice Area Flux Through Straits
simassacrossline			sea_ice_transport_across_line	Sea-Ice Mass Flux Through Straits
siarean		sea_ice_area	Sea-Ice Area North
siareas		sea_ice_area	Sea-Ice Area South
siextentn		Sea-Ice Extent North
siextents		Sea-Ice Extent South
sisnmassn		surface_snow_mass	Snow Mass on Sea Ice North
sisnmasss		surface_snow_mass	Snow Mass on Sea Ice South
sivoln		sea_ice_volume	Sea-Ice Volume North
sivols		sea_ice_volume	Sea-Ice Volume South

