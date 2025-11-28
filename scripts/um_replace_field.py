import xarray
import mule
import argparse
import numpy

def _parse_args():
    parser = argparse.ArgumentParser(
            description='Replace UM field with field from NetCDF file'
            )

    parser.add_argument(
            '--um-file',
            type=str,
            required=True,
            help='UM field containing field to replace.'
            )
    parser.add_argument(
            '--field',
            required=True,
            help='Name of field to replace.'
            )
    parser.add_argument(
            '--nc-file',
            type=str,
            required=True,
            help='NetCDF file to take the new field from.'
            )
    parser.add_argument(
            '--nc-var',
            type=str,
            required=True,
            help='NetCDF variable name of the desired variable.'
            )
    parser.add_argument(
            '-o',
            '--output',
            required=True,
            help='Name to write the new UM file to.'
            )
    parser.add_argument(
            '-t',
            '--time-index',
            required=False,
            default=None,
            help='Time index in the NetCDF field to take.'
            )
    parser.add_argument(
            '--stash',
            required=False,
            default=None,
            help='Stash files to use.'
            )
    parser.add_argument(
            '--stash-section',
            required=False,
            default=0,
            help='Which stash section to select.'
            )

    return parser.parse_args()

def replace_field(
        um_file,
        um_field,
        nc_file,
        nc_var,
        outfile,
        time_index
        ):
    """Replace the field with name "um_field" in the UM file with the specified
    variable from the NetCDF file, at the given time index."""

    # Work out the shape of the field to replace
    field_shape = determine_shape(um_file, um_field)

    nc_var = nc_file[nc_var]

    # Take the time dimension if necessary
    if time_index:
        nc_var = nc_var.isel(
                time=int(time_index),
                drop=True,
                missing_dims="ignore"
                )
    
    # Work out whether the shape of the NetCDF is compliant with the specified
    # shape
    nc_var = make_consistent(nc_var, field_shape)

    # Now we can replace the field
    swap_field(um_file, um_field, nc_var)

    to_file(um_file, outfile)

def to_file(um_file, output_name):
    um_file.validate(filename=output_name, warn=True)

    with open(output_name, 'wb') as name:
        um_file._write_to_file(name)

def swap_field(um_file, field, nc_var):
    """Replace the specified field in the u]m_file with the NetCDF variable."""

    stash_code = get_code(um_file, field)

    for field in um_file.fields:
        if field.lbuser4 == stash_code:
            new_data = nc_var.isel(
                    pseudo=field.lbuser5-1,
                    time=field.lbtim-1,
                    drop=True,
                    missing_dims="ignore"
                    ).to_numpy()

            # Assign NaN data to fill
            new_data = numpy.where(numpy.isnan(new_data), 1e20, new_data)
            data_prov = mule.ArrayDataProvider(new_data)
            field.set_data_provider(data_prov)

def make_consistent(nc_var, field_shape):
    """Make sure a DataArray is of consistent shape with the UM field."""
    # Make sure that lat, lon are the first 2 dimensions.
    dim_order = {}

    # Since dict ordering is guaranteed in python3.7+
    for um_dim, um_L in field_shape.items():
        for dim, length in nc_var.sizes.items():
            if length == um_L and dim not in dim_order:
                dim_order[dim] = um_dim
                break

    # Transpose the data
    nc_var = nc_var.transpose(*dim_order.keys(), transpose_coords=True)
    
    # Rename the dimensions so we can index them later
    nc_var = nc_var.rename(dim_order)

    return nc_var

def get_code(um_file, field):
    """Get the stash code associated with a given field."""
    stash_item = um_file.stashmaster.by_regex(field)

    assert len(stash_item) == 1, "Field name is not unique in the section."

    stash_code = list(stash_item.values())[0].item

    return stash_code

def determine_shape(um_file, field):
    """Try to determine the size of a UM field."""

    stash_code = get_code(um_file, field)

    # Build up dictionary of its shape
    shape = {
            "time": 1,
            "pseudo": 1,
            "lat": um_file.integer_constants.num_rows,
            "lon": um_file.integer_constants.num_cols,
            }

    for field in um_file.fields:
        if field.lbuser4 == stash_code:
            shape["pseudo"] = max(shape["pseudo"], field.lbuser5)
            shape["time"] = max(shape["time"], field.lbuser6)

    return shape

def open_fields_file(um_file, stash, section):
    """Open a UM file and attach the relevant stash file(s)."""

    um_file = mule.FieldsFile.from_file(um_file)

    base_stash = mule.STASHmaster()
    for supp_stash in stash.split(","):
        print(f"Opening {supp_stash} as Stashmaster")
        sm = mule.STASHmaster.from_file(supp_stash.strip())
        base_stash.update(sm)

    um_file.attach_stashmaster_info(base_stash.by_section(section))

    return um_file

if __name__ == "__main__":
    parser = _parse_args()

    um_file = open_fields_file(
            parser.um_file,
            parser.stash,
            parser.stash_section
            )

    nc_file = xarray.open_dataset(parser.nc_file, decode_times=False)

    replace_field(
            um_file,
            parser.field,
            nc_file,
            parser.nc_var,
            parser.output,
            parser.time_index
            )
