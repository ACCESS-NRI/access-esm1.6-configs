import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

_ = xr.set_options(keep_attrs=True)

restart_path = "/g/data/tm70/ds0092/model/inputs/access-esm1.5/modern/pre-industrial/restart/ocean/"

rho = 1035
mmol_to_mol = 1e-3
mmol_m3_to_mol_kg = mmol_to_mol / rho
umol_m3_to_mol_kg = mmol_to_mol * mmol_m3_to_mol_kg

unit_convert = {
    "adic": mmol_m3_to_mol_kg,
    "caco3": mmol_m3_to_mol_kg,
    "alk": mmol_m3_to_mol_kg,
    "dic": mmol_m3_to_mol_kg,
    "no3": mmol_m3_to_mol_kg,
    "phy": mmol_m3_to_mol_kg,
    "o2": mmol_m3_to_mol_kg,
    "fe": umol_m3_to_mol_kg,
    "zoo": mmol_m3_to_mol_kg,
    "det": mmol_m3_to_mol_kg,
    "caco3_sediment": mmol_to_mol,
    "det_sediment": mmol_to_mol
}

old_res = xr.open_mfdataset(
    f"{restart_path}/csiro_bgc*.nc",
    decode_cf=False,
    decode_times=False,
    decode_timedelta=False,
    decode_coords=False
)

zero_array = 0 * old_res["adic"]

wombatlite_res = []
for var in old_res:
    da_old = old_res[var]
    da_new = da_old * unit_convert[var]
    da_new.encoding = da_old.encoding
    del da_new.attrs["checksum"]
    if var in ["caco3_sediment", "det_sediment"]:
        # Make 3D
        da_new = da_new + zero_array.rename(var)
        da_new = da_new.transpose(*list(zero_array.dims))
        da_new = da_new.where(da_new.zaxis_1 < 1.5, 0)
    da_new.encoding['_FillValue'] = None
    wombatlite_res.append(da_new)

wombatlite_res = xr.merge(wombatlite_res)
wombatlite_res.attrs = old_res.attrs

for coord in wombatlite_res.coords:
    wombatlite_res[coord].encoding['_FillValue'] = None

wombatlite_res.to_netcdf(
    f"{restart_path}/ocean_wombatlite.res.nc",
    format="NETCDF3_CLASSIC",
    unlimited_dims=["Time"],
)
