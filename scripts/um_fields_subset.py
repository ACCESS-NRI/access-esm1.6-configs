#!/usr/bin/env python
# Select a subset from a UM fieldsfile
# -p option will select only the prognostic fields required for an initial
# dump and will also check some header fields.

# Output word size and endianness match input.

# This doesn't change the "written" date in a dump header.
# Martin Dix martin.dix@csiro.au

import mule
import os
import argparse
import warnings
from textwrap import dedent
from itertools import chain

PROGNOSTIC_STASH_CODES = tuple(chain(range(1,999+1), range(33001,34999+1)))

def convert_to_list(value: str):
    """
    Convert a comma-separated string into a list of positive integers.
    
    Parameters
    __________
    value: str
    A string of comma-separated positive integers

    Returns
        list
        A list of STASH codes to be excluded or included
    
    """
    msg = "All values must be positive integers."
    try:
        values = [int(v) for v in value.split(",")]
        if any(v <= 0 for v in values):
            raise ValueError(msg)
        return values
    except ValueError:
        raise argparse.ArgumentTypeError(msg)
        
def parse_args():
    """
    Parse command-line arguments.

    Parameters
    ----------
    None

    Returns
    ----------
    args_parsed : argsparse.Namespace
        Argparse namespace containing the parsed command line arguments.
    """
    DESCRIPTION = dedent(
        """
        Subset a UM file to generate an output containing only selected fields. 
        
        Examples:
        
        1. Subset UM file only including STASH codes 155, 156, 3100 and 3101
        `um_fields_subset /path/to/um/file --include 155,156,3100,3101`
        
        2. Subset UM file excluding the STASH codes 132 and 14020
        `um_fields_subset /path/to/um/file --exclude 132,14020`
        
        2. Subset UM file only including prognostic STASH codes
        `um_fields_subset /path/to/um/file -p`
        """
    )
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)

    # Positional arguments
    parser.add_argument(dest='ifile', metavar="INPUT_PATH", help='Path to the input file.')
    # Optional arguments
    parser.add_argument('-o', '--output', dest = 'output_path', metavar="OUTPUT_PATH", help='Path to the output file. If omitted, the default output file is created by appending "_subset" to the input path.')
    meg = parser.add_mutually_exclusive_group(required=True)
    meg.add_argument('-p', '--prognostic', dest='prognostic',  action='store_true',
                        help="Only include prognostic variables (sections 0, 33 and 34). Cannot be used together with --include or --exclude.")
    meg.add_argument('--include', dest='include_list',  type=convert_to_list, metavar="STASH_CODES",
                        help="Comma-separated list of STASH codes to include in the output file. Any STASH code present in the input file but not contained in this STASH code list will not be present in the output file. Cannot be used together with --prognostic or --exclude.")
    meg.add_argument('--exclude', dest='exclude_list',  type=convert_to_list, metavar="STASH_CODES",
                        help="Comma-separated list of STASH codes to exclude from the output file. All STASH codes present in the input file but not contained in this STASH code list will be present in the output file. Cannot be used together with --prognostic or --include.")
    parser.add_argument('--validate', action='store_true',
                        help='Validate the output fields file using mule validation.')
    # Parse arguments
    args_parsed = parser.parse_args()
    
    # Return arguments
    return args_parsed


def void_validation(*args, **kwargs):
    """
    Don't perform the validation, but print a message to inform that validation has been skipped.
    """

    print('Skipping mule validation. To enable the validation, run using the "--validate" option.')


def create_default_outname(filename, suffix="_subset"):
    """
    Create a default output filename by appending a suffix to the input filename.
    If an output filename already exists, a number will be appended to produce a unique output filename.

    Parameters
    ----------
    filename: str
         The input filename.
    suffix: str, optional
        The suffix to append to the filename.

    Returns
    ----------
    output_filename: str
        The default output filename.
    """

    output_filename = f"{filename}{suffix}"
    num=""
    if os.path.exists(output_filename):
        num = 1
        while os.path.exists(f"{output_filename}{num}"):
            num += 1
    return f"{output_filename}{num}"
    
def warn_if_stash_not_present(fields, stash_list):
    """
    Raise a warning for any stash codes included in the input stash_list that are not present within the input fields.
    
    Parameters
    __________

    fields : mule.ff.FieldsFile.fields
        All the fields from the fields file.

    stash_list :  set of int
    Returns
    _______
        None

    """

    existing_codes = {f.lbuser4 for f in fields}
    missing_codes = set(stash_list) - existing_codes

    if missing_codes:
        warnings.warn(f"The following STASH codes are not found in the input file: {missing_codes}")


def include_fields(fields, stash_list):
    """
    Return a subset of the input fields, containing only the ones having a stash code included in stash_list. Raise a warning if a stash code included in stash_list is not present in the input fields.

    Parameters
    __________
    fields : mule.ff.FieldsFile.fields 
        All the fields from the fields file.
    stash_list : list of int
        A list of STASH item codes to include.
    
    Returns
    -------
        list of mule.ff.FieldsFile.fields
        The subset of fields only containing the ones to be included.
    """

    warn_if_stash_not_present(fields, stash_list)
    return [f.copy() for f in fields if f.lbuser4 in stash_list]

def exclude_fields(fields, stash_list):
    """
    Return a subset of the input fields, containing only the ones having a stash code not included in stash_list. Raise a warning if a stash code included in stash_list is not present in the input fields.

    Parameters
    __________
    fields : mule.ff.FieldsFile.fields 
        All the fields from the fields file.
    stash_list : list of int
        A list of STASH item codes to exclude.
    
    Returns
    -------
        list of mule.ff.FieldsFile.fields
        The subset of fields not containing the ones to be excluded.
    """

    warn_if_stash_not_present(fields, stash_list)
    return [f.copy() for f in fields if f.lbuser4 not in stash_list]

def filter_fieldsfile(input_file, prognostic, include_list, exclude_list):
    """
    Creates a new mule fieldsfile from the input_file, by filtering its fields based on the values of prognostic, include_list and eclude_list.

    Parameters
    ----------
    input_file : mule.ff.FieldsFile
        The mule fieldsfile to be filtered.
    prognostic : bool
        A boolean flag indicating if only prognostic fields should be included.
    include_list : list of int or None
        A list of STASH item codes to include.
    exclude_list : list of int or None
        A list of STASH item codes to exclude.

    Returns
    -------
    filtered_file : mule.ff.FieldsFile
        The filtered mule fieldsfile.
    """

    filtered_file = input_file.copy()
    if prognostic:
        include_list = PROGNOSTIC_STASH_CODES

    filtered_file.fields = include_fields(input_file.fields, include_list) if include_list is not None else exclude_fields(input_file.fields, exclude_list)
    return filtered_file
    
def main():

    # Parse the inputs and validate that they do not xlist or vlist are given.
    args = parse_args()

    # Create the output filename.
    output_filename = create_default_outname(args.ifile) if args.output_path is None else args.output_path
    
    ff = mule.DumpFile.from_file(args.ifile)

    # filter the fieldsfile
    filtered_file = filter_fieldsfile(ff, args.prognostic, args.include_list, args.exclude_list)

    # Skip mule validation if the "--validate" option is not provided
    if not args.validate:
        filtered_file.validate = void_validation

    filtered_file.to_file(output_filename)

if __name__== "__main__":
    main() # pragma: no cover
