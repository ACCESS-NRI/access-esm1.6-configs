import argparse
import mule
import xarray
import numpy

def _parse_args():
    """Read the command line arguments."""

    parser = argparse.ArgumentParser(
            prog="convert_UM_restart_to_netcdf",
            description="Convert the CABLE fields in a UM7 restart to netcdf."
            )

    parser.add_argument(
            "-i",
            "--input",
            help="Reference UM7 restart to convert"
            )
    parser.add_argument(
            "-o",
            "--output",
            help="Name to write the NetCDF file to"
            )
    parser.add_argument(
            "-s",
            "--stash",
            help="Comma separated list of stashmaster files to use",
            default="/g/data/access/umdir/vn7.3/ctldata/STASHmaster/STASHmaster_A,/g/data/rp23/experiments/2024-03-12_CABLE4-dev/lw5085/CABLE-as-ACCESS/prefix.PRESM_A"
            )

    return parser.parse_args()
    
def convert_restart(RestartFile, OutputFile):
    """
    Convert the UM restart to NetCDF
    """

    # We know the latitude and longitude
    Longitudes = numpy.linspace(0.0, 360.0, 192)
    Latitudes = numpy.linspace(-90.0, 90.0, 145, endpoint=True)

    # We can set the vegetation dimension- just 1-17
    VegTypes = numpy.arange(1, 18)

    # Set up the xarray dataset
    RestartDataset = xarray.Dataset(
            coords={
                "lon": ("longitude", Longitudes),
                "lat": ("latitude", Latitudes),
                "nVeg": ("nVeg", VegTypes)
                }
            )

    # Build the land mask by inspecting the LAND MASK (no halo) field
    LandMaskStash = RestartFile.stashmaster.by_regex("LAND MASK")
    MaskStashCode = list(LandMaskStash.values())[0].item

    for Field in RestartFile.fields:
        if Field.lbuser4 == MaskStashCode:
            Mask = Field.get_data() == 0.0
            break

    # We'll just iterate through the entries in the stash, and pull the stash
    # codes and get the relevant field
    for StashEntry in RestartFile.stashmaster.values():
        # Useful entry in the stash are item (the stash code) and name.
        FieldName = StashEntry.name
        StashCode = StashEntry.item

        # Remove disallowed characters in field names
        FieldName = FieldName.replace('/', ' PER ')

        # Count the number of fields with the given stash code
        NFields = 0
        for (i, Field) in enumerate(RestartFile.fields):
            if Field.lbuser4 == StashCode:
                NFields += 1

        # It should either be 1, for grid cell values, or 17 for values on
        # tiles
        if NFields == 1:
            # A grid cell field, not per vegetation type
            try:
                for Field in RestartFile.fields:
                    if Field.lbuser4 == StashCode:
                        FieldData = numpy.ma.masked_array(
                                Field.get_data(),
                                mask=Mask
                                )
                if FieldData.size == (145, 192):
                    RestartDataset[FieldName] = (('lat', 'lon'), FieldData)
            except:
                print(f"Failed to convert field {FieldName}")
                pass

        elif NFields == 17:
            # A per tile field
            FieldData = numpy.ndarray((17, 145, 192), dtype = numpy.float32)
            Veg = 0
            for Field in RestartFile.fields:
                if Field.lbuser4 == StashCode:
                    FieldData[Veg, :, :] = Field.get_data()
                    Veg += 1
            
            RestartDataset[FieldName] = (
                    ('nVeg', 'lat', 'lon'),
                    numpy.ma.masked_where(
                        numpy.repeat(Mask[numpy.newaxis, :, :], 17, axis=0),
                        FieldData,
                        1e20)
                    )

    RestartDataset.to_netcdf(OutputFile)

if __name__ == '__main__':

    args = _parse_args()
    
    # Process the command line args
    FF = mule.FieldsFile.from_file(args.input)
    SMBase = mule.STASHmaster()
    for SM in args.stash.split(","):
        SM = mule.STASHmaster.from_file(SM)
        SMBase.update(SM)

    FF.attach_stashmaster_info(SMBase.by_section(0))

    convert_restart(FF, args.output)
