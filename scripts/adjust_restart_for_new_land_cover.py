import argparse
import yaml
import numpy
import xarray

def _parse_args():
    """Read the command line arguments."""

    parser = argparse.ArgumentParser(
            prog="remap_vegetation",
            description="Process the CABLE section of a UM7 restart " +\
                    "for a new vegetation map"
            )

    parser.add_argument(
            "-i",
            "--input",
            help="Reference CABLE section of UM7 restart to convert"
            )
    parser.add_argument(
            "-o",
            "--output",
            help="Name to write the new restart to"
            )
    parser.add_argument(
            "-m",
            "--vegetation_map",
            help="New vegetation map to use"
            )
    parser.add_argument(
            "-t",
            "--time-index",
            type=int,
            default=0,
            help="Index in vegetations fractions to use as current year"
            )
    parser.add_argument(
            "--use-previous-fractions-from-restart",
            default=False,
            action="store_true",
            help="Choose to take the previous fractions from the input restart."
            )
    parser.add_argument(
            "--fill-all",
            default=False,
            action="store_true",
            help="Whether to fill all tiles, or just new active tiles."
            )
    parser.add_argument(
            "-c",
            "--config",
            help="Config file to use for the remapping",
            )

    return parser.parse_args()
    
def prepare_mapping(nVeg, ConfigFile):
    """Read the configuration yaml file, validate it and apply defaults where
    necessary."""

    with open(ConfigFile, 'r') as conf:
        MappingConf = yaml.safe_load(conf)

    # By default, the vegetation maps in a 1-to-1 manner, i.e.
    # vegetation type 1 in the old vegetation map maps to vegetation type 1 in
    # the new vegetation map.
    VegetationMapping = {i: [i] for i in range(nVeg)}

    # It may be that the user removes either per_tile or per_cell entries in
    # the config- apply default values (empty list) that are iterable in that
    # case. Also, ensure that it's a list instance
    MappingConf['per_cell'] = MappingConf.get('per_cell') or []
    if not isinstance(MappingConf['per_cell'], list):
        MappingConf['per_cell'] = [MappingConf['per_cell']]

    MappingConf['per_tile'] = MappingConf.get('per_tile') or []
    if not isinstance(MappingConf['per_tile'], list):
        MappingConf['per_tile'] = [MappingConf['per_tile']]

    # Apply the supplied mappings
    if 'vegetation_map' in MappingConf:
        for OutVegType, InVegTypes in MappingConf['vegetation_map'].items():
            # The user specified mappings are going to offset by -1, since in 
            # the Fortran world we use 1 based indexing and that's how people 
            # think about the vegetation types.
            VegetationMapping[OutVegType-1] = [InVeg-1 for InVeg in InVegTypes]
    
    MappingConf['vegetation_map'] = VegetationMapping

    # Apply the search defaults
    MappingConf['search_radius'] = MappingConf.get('search_radius', 2)
    MappingConf['latitude_band'] = MappingConf.get('latitude_band', 8)
    MappingConf['minimum_points'] = MappingConf.get('minimum_points', 1)
    
    return MappingConf

def setup_output_dataset(OutputVegetation):
    """Use the OutputVegetation as a template to set up the Dataset that will
    contain the new restart information. Use the list of variable names
    contained in the Config to set the NetCDF variable names."""

    # Get the shape of the output data to perform validation
    nOutputVeg, nLat, nLon = OutputVegetation.shape

    # Set up the new xarray dataset to write to
    Longitudes = numpy.linspace(0.0, 360.0, nLon, endpoint=False)
    Latitudes = numpy.linspace(-90.0, 90.0, nLat, endpoint=True)
    VegTypes = numpy.arange(1, nOutputVeg+1)

    # I couldn't make the xarray.Dataset call accept a dictionary generator as
    # an argument for data_vars. So initialise the Dataset, then add variables
    # to it later.
    OutDataset = xarray.Dataset(
            coords={
                'lon': Longitudes,
                'lat': Latitudes,
                'veg': VegTypes
                }
            )

    return OutDataset
                    
def modify_mask_for_cell(SearchMask, GridCell, Coord):
    """Modify the input search mask to only include the current grid cell at
    Coord."""

    Lon, Lat = Coord
    SearchMask[Lat, Lon] = True

def modify_mask_for_nearest(SearchMask, SearchRadius, Coord):
    """Modify the input search mask to only include the specified 'radius' of
    points around the given Coord. In this instance, radius is just a block of
    points with index +-SearchRadius around the original Coord."""
    
    # Destructure for more readable usage later
    Lon, Lat = Coord
    nLat, nLon = SearchMask.shape

    # Create the set of coordinates to unmask
    SearchInds = numpy.arange(-SearchRadius, SearchRadius+1)

    # Clip the latitude indices, since they aren't periodic
    LatInds = numpy.clip(Lat + SearchInds, 0, nLat-1)

    # Apply mod to longitude indices, since they are periodic
    LonInds = numpy.mod(Lon + SearchInds, nLon)

    # Modify the mask in place
    for LatSearch in LatInds:
        for LonSearch in LonInds:
            SearchMask[LatSearch, LonSearch] = True

def modify_mask_for_latitude_band(SearchMask, LatitudeBand, Coord):
    """Modify the input search mask to only include the specifed band of
    latitudes around the given Coord."""

    # Destructure for more readable usage later
    Lon, Lat = Coord
    nLat, nLon = SearchMask.shape

    # Create the set of coordinates to unmask
    SearchInds = numpy.arange(-LatitudeBand, LatitudeBand+1)

    # Clip the latitude indices, since they aren't periodic
    LatInds = numpy.clip(Lat + SearchInds, 0, nLat-1)

    # Modify the mask in place
    for LatSearch in LatInds:
        SearchMask[LatSearch, :] = True

def modify_mask_for_global(SearchMask, Global, Coord):
    """Modify the input search mask to include the whole globe. Include
    arguments for consistency with the other masking methods."""

    # Nothing interesing to do here
    SearchMask[:] = True

def find_active_tiles(
        SearchMask,
        InputVegetation,
        VegetationMapping,
        ):
    """Using the supplied search mask, generate a set of masks which are an OR
    of the original search mask and a mask describing the active tiles, defined
    as a tile with an area fraction of greater than 0.0. Generates a mask for
    each of the vegetation types used to construct the new vegetation type."""

    # Make it a list, because there are instances where more than 1 input
    # vegetation type maps to a single output vegetation type
    ActiveTileMasks = []

    for VegType in VegetationMapping:
        # The search mask should then be a logical and of:
        # * The land points (where the vegetation is non nan)
        # * The supplied search mask
        # * The tiles which have a vegetation type greater than 0.0
        # Note that the minimum area threshold is chosen carefully to be
        # greater than 0.0, which is the value used for tiles that will become
        # active in future due to land use change
        TileSearchMap = ~numpy.isnan(InputVegetation[VegType, :, :]) &\
                SearchMask &\
                (InputVegetation[VegType, :, :] > 0.0)

        ActiveTileMasks.append(TileSearchMap)

    return ActiveTileMasks

def remap_vegetation(
        InputDataset,
        InputVegetation,
        OutputVegetation,
        FillAll,
        Config
        ):
    """Map the input vegetation to the output vegetation."""

    # Read in the variable mappings- needs number of vegetation types for map
    nOutputVeg, nLat, nLon = OutputVegetation.shape
    MappingConf = prepare_mapping(nOutputVeg, Config)

    # Destructure the configuration variables
    PerCellVariables = MappingConf['per_cell']
    PerTileVariables = MappingConf['per_tile']
    VegMapping = MappingConf['vegetation_map']
    SearchRadius = MappingConf['search_radius']
    LatitudeBand = MappingConf['latitude_band']
    MinPointsFound = MappingConf['minimum_points']
    
    # Set up the Dataset we're going to write to
    OutDataset = setup_output_dataset(OutputVegetation)

    # Set the fill value that we will use for all variables
    FillVal = 1e20

    # Add the land fractions- also include previous year as same for LUC
    OutDataset['FRACTIONS OF SURFACE TYPES'] = (('veg', 'lat', 'lon'),
                                               OutputVegetation)

    # We need to know which tiles to fill, and which to empty. This depends on
    # what mode we're in: if --fill-all is passed, then we fill all empty relevant
    # tiles, otherwise only the new active tiles. Likewise, we need to which
    # tiles to empty in the case where --fill-all is not passed.
    if FillAll:
        # Everywhere not already filled by the existing tiles
        TilesToFill = InputVegetation <= 0.0

        # Don't need to empty anything
        TilesToEmpty = numpy.full_like(InputVegetation, False, dtype=bool)

    else:
        # Only new tiles that have come into existence
        TilesToFill = numpy.logical_and(
                InputVegetation <= 0.0,
                OutputVegetation > 0.0
                )

        # Tiles that have left existence
        #TilesToEmpty = numpy.logical_and(
        #        InputVegetation > 0.0,
        #        OutputVegetation <= 0.0
        #        )
        TilesToEmpty = OutputVegetation <= 0.0

    # Perform the per-cell averaging
    # Apply a mask to the array, so we don't mess up our summations with
    # near-zero vegetation fractions
    MaskedInputVegetation = numpy.ma.masked_where(
            numpy.logical_or(
                InputVegetation <= 0.0,
                numpy.isnan(InputVegetation)
                ),
            InputVegetation)

    # And create 
    for Variable in PerCellVariables:
        AreaWeightedMean = numpy.stack(
                [numpy.sum(
                    InputDataset[Variable].to_numpy() * MaskedInputVegetation,
                    axis=0
                    )] * nOutputVeg,
                axis=0
                )
        
        # Only apply the averaging process to tiles that don't already exist-
        # do this by initially copying over the original fields, then writing
        # over the tiles to fill
        OutData = InputDataset[Variable].to_numpy()
        OutData[TilesToFill] = AreaWeightedMean[TilesToFill]
        OutData[TilesToEmpty] = 0

        OutDataset[Variable] = (('veg', 'lat', 'lon'), OutData)
        OutDataset[Variable].encoding['_FillValue'] = FillVal
        
    # For the per tile variables, start by initialising with the old data, then
    # removing the tiles that have left existence
    for Variable in PerTileVariables:
        OutData = InputDataset[Variable].to_numpy()
        OutData[TilesToEmpty] = 0

        OutDataset[Variable] = (('veg', 'lat', 'lon'), OutData)
        OutDataset[Variable].encoding['_FillValue'] = FillVal

    # Perform the per-tile averaging
    # To only iterate over desired points, we can mask the array where so that
    # only TilesToFill are unmasked.
    MaskedOutputVeg = numpy.ma.masked_array(OutputVegetation, mask=~(TilesToFill))

    # At each point, we're going to use a new mask to assist the search. But we
    # don't want to allocate a new array every point- initialise a mask here,
    # and then modify the mask in place.
    SearchMask = numpy.full((nLat, nLon), False, dtype=bool)

    # Set up the set of search methods and search parameters to walk through
    SearchMethods = [
            modify_mask_for_cell,
            modify_mask_for_nearest,
            modify_mask_for_latitude_band,
            modify_mask_for_global
            ]

    # The cell and global searches take no parameters
    SearchParams = [None, SearchRadius, LatitudeBand, None]

    # The minimum number of points permitted for a search to be successful
    PointsThreshold = [1, MinPointsFound, MinPointsFound, 1]

    # Start by iterating through each output vegetation type
    counter = 0
    for (OutVeg, Lat, Lon), _ in numpy.ma.ndenumerate(MaskedOutputVeg):
        
        # Iterate through the search methods until a success
        for Method, Param, MinPoints in zip(SearchMethods, SearchParams,
                                            PointsThreshold):
            Method(SearchMask, Param, (Lon, Lat))

            # Further refine the mask to only include the active tiles
            ActiveTileMasks = find_active_tiles(
                    SearchMask,
                    InputVegetation,
                    VegMapping[OutVeg]
                    )

            # Check how many valid points there are in the mask
            PointsFound = sum([ActiveTileMask.sum() for ActiveTileMask in
                              ActiveTileMasks])

            if PointsFound >= MinPoints:
                # Search was successful
                break

        # Now we can continue with a generic masked find and average
        # There are some veg types that don't have any values anywhere
        # In that case, just use zeros everywhere.
        if PointsFound < MinPointsFound:
            for Variable in PerTileVariables:
                OutDataset[Variable][OutVeg, Lat, Lon] = 0.0
        else:
            for Variable in PerTileVariables:
                # Set incrementing value to 0
                Total = 0.0

                # We want to summate over all active tiles then average by the
                # number of active tiles. In most cases, this only involves one
                # vegetation type, but sometimes there are more.
                for (InVeg, TileMask) in \
                        zip(VegMapping[OutVeg], ActiveTileMasks):
                    # Turn the data into a numpy array, then index it with the
                    # generated mask.
                    VarData = InputDataset[Variable][InVeg, :, :].to_numpy()
                    TotalForVegType = VarData[TileMask].sum()
                    Total += TotalForVegType

                # Average and set the index in the dataarray.
                OutDataset[Variable][OutVeg, Lat, Lon] =\
                        Total / PointsFound

        # Reset the search mask to false
        SearchMask[:] = False

    return OutDataset

def run_vegetation_remapping(input, output, vegetation_map, time_index, fill_all, config, use_previous_fractions_from_restart):
    """
    Wrapper function to load the files, run the remapping, and save the output file
    """
    OrigDataset = xarray.open_dataset(input)
    OrigVegetation = OrigDataset['FRACTIONS OF SURFACE TYPES'].to_numpy()

    Vegetation = xarray.open_dataset(vegetation_map)
    # Allow the file to contain a time series (as might be prepared for a LUC
    # dataset) or a snapshot.
    NewVegetation = Vegetation['fraction'][time_index, :, :, :].to_numpy()

    OutDataset = remap_vegetation(
            OrigDataset,
            OrigVegetation,
            NewVegetation,
            fill_all,
            config
            )

    # Decide what to do about the previous year's fractions in the restart. It
    # can either come from what is already in the restart, or from the previous
    # year in the land use change dataset (or a copy of the first year's 
    # fractions, if the first index is requested).
    # If the user wants to take previous fractions from the restart, don't need
    # to do anything.
    if not use_previous_fractions_from_restart:
        if time_index == 0:
            prev_index = 0
        else:
            prev_index = args.time_index - 1

        PrevVegetation = Vegetation['fraction'][prev_index, :, :, :].to_numpy()
        OutDataset["PREVIOUS YEAR SURF FRACTIONS (TILES)"] = \
                (('veg', 'lat', 'lon'), PrevVegetation)
        
    OutDataset.to_netcdf(output)


if __name__ == '__main__':

    # Process command line args
    args = _parse_args()

    # Run the remapping
    run_vegetation_remapping(args.input,
                             args.output, 
                             args.vegetetation_map,
                             args.time_index,
                             args.fill_all,
                             args.use_previous_fractions_from_restart
                             )