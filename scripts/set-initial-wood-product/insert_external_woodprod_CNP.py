#!/usr/bin/env python3
import argparse
import mule
import xarray as xr
import six
import shutil
import tempfile
import os




def parse_args():
    parser = argparse.ArgumentParser(
        prog="insert_external_woodprod_CNP",
        description= ( 
            """
            Script to modify specific fields in a UM7 restart file using data from an external NetCDF dataset.Fields modified:  
            - 'WOOD HARVEST CARBON3(CASA-CNP)'  
            - 'WOOD HARVEST NITROG3(CASA-CNP)'
            - 'WOOD HARVEST PHOSPH3(CASA-CNP)'
            Each field has multiple PFTs (vegtypes) indexed by lbuser5. The NetCDF variables for the wood product 
            pools have the shape (lat, lon, vegtype).
            """
        )
    )

    parser.add_argument(
        "--restart",
        required=True,
        help="Path to source UM restart file"
    )
    parser.add_argument(
        "--woodfile",
        required=True,
        help="Path to external wood product netCDF"
    )
    parser.add_argument(
        "--stash-base",
        required=True,
        help="Path to base STASHMaster_A file"
    )
    parser.add_argument(
        "--stash-prefix",
        required=True,
        help="Path to prefix.PRESM_A stash file"
    )

    return parser.parse_args()


# Custom write function to bypass validation issues when saving the file
def to_file(self, output_file_or_path):
    if isinstance(output_file_or_path, six.string_types):        
        with open(output_file_or_path, 'wb') as output_file:
            self._write_to_file(output_file)    
    else:        
        self._write_to_file(output_file_or_path)


if __name__ == "__main__":

    args = parse_args()

    restart_path = args.restart
    external_nc_path = args.woodfile
    stashmaster_base_path = args.stash_base
    stashmaster_ext_path = args.stash_prefix



    print("Starting UM restart file modification...")
    # Load UM restart file
    ff = mule.FieldsFile.from_file(restart_path)
    
    print("Loading STASHmaster base file")
    # Load and attach STASHmaster files
    stash_base = mule.STASHmaster.from_file(stashmaster_base_path)
    print("Loading STASHmaster ext file")
    stash_ext = mule.STASHmaster.from_file(stashmaster_ext_path)
    print("Updating stash_base with stash_ext")
    stash_base.update(stash_ext)
    print("Attaching STASHmaster info")
    ff.attach_stashmaster_info(stash_base.by_section(0))  # Section 0 = prognostic
    
    print("Loading external netcdf data")
    # Load external NetCDF data
    external_nc = xr.open_dataset(external_nc_path)
    
    # Mapping of restart/STASH field names to external netcdf file variable names 
    var_targets = {"WOOD HARVEST CARBON3(CASA-CNP)": "wood_product_c",
            "WOOD HARVEST NITROG3(CASA-CNP)": "wood_product_n",
            "WOOD HARVEST PHOSPH3(CASA-CNP)": "wood_product_p",
            }

    for target_name, ext_nc_var in var_targets.items():
        # 1)
        external_data = external_nc[ext_nc_var].values

        # 1) find stash_code from the actual file contents
        stash_code = None
        for f in ff.fields:
            if f.stash and f.stash.name and target_name in f.stash.name:
                stash_code = f.lbuser4
                break
        
        if stash_code is None:
            raise RuntimeError(f"Couldn't find any field named like {target_name}")
        
        print("Using stash_code from file:", stash_code)
        
        # 2) now update all matching tiles
        for pft_index in range(external_data.shape[2]):
            data_slice = external_data[:, :, pft_index]
            matched = False
            for f in ff.fields:
                if f.lbuser4 == stash_code and f.lbuser5 == pft_index + 1:
                    f.set_data_provider(mule.ArrayDataProvider(data_slice))
                    matched = True
            if not matched:
                print("No matching field for tile", pft_index + 1)

    # Save modified restart
    print(f"\nSaving modified restart file to: {restart_path}")
    ff.to_file = to_file

    temp = tempfile.NamedTemporaryFile()
    ff.to_file(ff, temp.name)
    os.unlink(restart_path)
    shutil.copy(temp.name, restart_path)
    print(f"Modified restart file written to '{restart_path}'")
