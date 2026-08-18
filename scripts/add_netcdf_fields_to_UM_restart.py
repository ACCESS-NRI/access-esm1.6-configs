import xarray
import mule
import six
import argparse

def _parse_args():
    """Read the command line arguments."""

    parser = argparse.ArgumentParser(
            prog="add_netcdf_fields_to_UM_restart",
            description="Take NetCDF fields and placed them in the " +
            "corresponding UM fields."
            )

    parser.add_argument(
            "-i",
            "--input",
            help="NetCDF file to merge in"
            )
    parser.add_argument(
            "-o",
            "--output",
            help="Name to write the resulting restart to"
            )
    parser.add_argument(
            "-r",
            "--restart",
            help="UM restart to use as a template"
            )
    parser.add_argument(
            "-s",
            "--stash",
            help="Comma separated list of stashmaster files to use",
            default="/g/data/access/umdir/vn7.3/ctldata/STASHmaster/STASHmaster_A,/g/data/rp23/experiments/2024-03-12_CABLE4-dev/lw5085/CABLE-as-ACCESS/prefix.PRESM_A"
            )

    return parser.parse_args()

def modify_UM_field_by_name(FieldsFile, Dataset, VarName):
    """Take the DataArray attached to Dataset[VarName] and map it to the
    equivalent field in the UM fields file."""

    # We will want to check against the original FieldsFile field, to ensure
    # matching sizes
    VariableData = Dataset[VarName].to_numpy()
    nVeg, nLat, nLon = VariableData.shape

    # Retrieve the stash code- UM does regex searching, so make sure to escape
    # any brackets
    UMName = VarName.replace('(', '\(').replace(')', '\)')
    try:
        StashCode = list(FieldsFile.stashmaster.by_regex(UMName).values())[0].item
    except:
        # A little catch for the "/" for " PER " replacement
        print(f"Finding {UMName} failed; try again replacing PER")
        UMName = UMName.replace(' PER ', '/')
        StashCode = list(FieldsFile.stashmaster.by_regex(UMName).values())[0].item

    # Check that the number of fields is the same as the vegetation dimension
    nFields = 0
    for Field in FieldsFile.fields:
        if Field.lbuser4 == StashCode:
            nFields += 1

    assert nFields == nVeg

    # Iterate through tiles
    Tile = 0
    for Field in FieldsFile.fields:
        if Field.lbuser4 == StashCode:
            NewData = VariableData[Tile, :, :]
            DataProvider = mule.ArrayDataProvider(NewData)
            Field.set_data_provider(DataProvider)
            Tile += 1

# Intercept the write function to disable validation
def to_file(self, output_file_or_path):
        """
        Write to an output file or path.

        Args:
            * output_file_or_path (string or file-like):
                An open file or filepath. If a path, it is opened and
                closed again afterwards.

        .. Note::
            As part of this the "validate" method will be called. For the
            base :class:`UMFile` class this does nothing, but sub-classes
            may override it to provide specific validation checks.

        """
        # Call validate - to ensure the file about to be written out doesn't
        # contain obvious errors.  This is done here before any new file is
        # created so that we don't create a blank file if the validation fails
        if isinstance(output_file_or_path, six.string_types):
            self.validate(filename=output_file_or_path, warn=True)
        else:
            self.validate(filename=output_file_or_path.name, warn=True)

        if isinstance(output_file_or_path, six.string_types):
            with open(output_file_or_path, 'wb') as output_file:
                self._write_to_file(output_file)
        else:
            self._write_to_file(output_file_or_path)

if __name__ == '__main__':

    args = _parse_args()

    # Process command line args
    ProcessedRestart = xarray.open_dataset(args.input)

    # Build the STASHmaster and attach it to the UM restart
    SMBase = mule.STASHmaster()
    for SM in args.stash.split(','):
        SM = mule.STASHmaster.from_file(SM)
        SMBase.update(SM)

    BaseRestart = mule.FieldsFile.from_file(args.restart)
    BaseRestart.attach_stashmaster_info(SMBase.by_section(0))

    # Drop in the variables to modify
    for Variable in ProcessedRestart.data_vars:
        modify_UM_field_by_name(BaseRestart, ProcessedRestart, Variable)

    # Write to file- since the UM7 restart doesn't match their expected format
    # for some reason, we need to override the existing to_file
    BaseRestart.to_file = to_file
    BaseRestart.to_file(BaseRestart, args.output)
