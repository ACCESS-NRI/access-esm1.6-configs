import os
import mule
import argparse
from textwrap import dedent

def validate_year_value(value):
    """
    Ensure the year is a non-negative integer between 0 and 9999.
    """
    if value is None:
        return None
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid year: {value}. Must be an integer between 0 and 9999.")
    if ivalue < 0 or ivalue > 9999:
        raise argparse.ArgumentTypeError(f"Invalid year: {value}. Must be between 0 and 9999.")
    return ivalue

def validate_month_value(value):
    """
    Ensure the month is between 1 and 12 (inclusive).
    """
    if value is None:
        return None
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid month: {value}. Must be an integer between 1 and 12.")
    if ivalue < 1 or ivalue > 12:
        raise argparse.ArgumentTypeError(f"Invalid month: {value}. Must be between 1 and 12.")
    return ivalue

def validate_day_value(value):
    """
    Ensure the day is between 1 and 31 (inclusive).
    """
    if value is None:
        return None
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid day: {value}. Must be an integer between 1 and 31.")
    if ivalue < 1 or ivalue > 31:
        raise argparse.ArgumentTypeError(f"Invalid month: {value}. Must be between 1 and 31.")
    return ivalue

def validate_date_value(value):
    """
    Ensures the date is in YYYYMMDD format and extract year, month, and day.
    """
    if len(value) != 8:
        raise argparse.ArgumentTypeError(f"Invalid date: {value}. Must be exactly 8 digits (YYYYMMDD).")
    year = validate_year_value(value[:4])
    month = validate_month_value(value[4:6])
    day = validate_day_value(value[6:])

    return (year,month,day)

def validate_mutually_exclusive_args(year, month, day, date):
    """
    Check that --date is not passed together with any of --year, --month or --day.
    """
    if date is not None and any(arg is not None for arg in [year, month, day]):
        raise ValueError("The arguments --date and any of --year, --month or --day are mutually exclusive.")
            
def validate_required_args(year, month, day, date):
    """
    Ensure at least one argument among -y, -m, -d or --date is specified.
    """
    if all(arg is None for arg in [date, year, month, day]):
        raise ValueError("At least one argument among --date, --year, --month or --day must be provided.")
    
def parse_args():
    """
    Parse the command line arguments.

    Returns
    ----------
    argparse.Namespace
        Argparse namespace containing the parsed command line arguments.
    """
    DESCRIPTION = dedent(
        """
        Change the time metadata of a UM restart file, without modifying its data content.
        
        Examples:
        
        1. Change date of a UM restart file to the 22nd Jan 2025
        `change_dump_date /path/to/restart.dump --date 20250122`
        """
    )
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('ifile', metavar="INPUT_PATH", help='Path to the input file.')
    parser.add_argument('-o', '--output', dest='output_path', metavar="OUTPUT_PATH",
                        help='Path to the output file. If omitted, the default output file is created by appending "_newdate" to the input path.')
    parser.add_argument('--validate', action='store_true',
        help='Validate the output fields file using mule validation.')

    parser.add_argument('--date', help='New date in YYYYMMDD format.')
    parser.add_argument('-y', '--year', type=validate_year_value, help='New year value (0-9999).')
    parser.add_argument('-m', '--month', type=validate_month_value, help='New month value (1-12).')
    parser.add_argument('-d', '--day', type=validate_day_value,  help='New day value (1-31).')

    args_parsed = parser.parse_args()

    # Ensure at least one of -y, -m, or -d is specified if --date is not used
    year, month, day, date = args_parsed.year, args_parsed.month, args_parsed.day, args_parsed.date
    validate_mutually_exclusive_args(year, month, day, date)
    validate_required_args(year, month, day, date)

    # If --date is provided, extract year, month, and day and assign them
    if date is not None:
        args_parsed.year, args_parsed.month, args_parsed.day = validate_date_value(date)

    return args_parsed

def change_header_date_file(ff, new_year, new_month, new_day):
    """
    Update the initial and valid date in the fixed-length header of a UM fields file.

    Parameters
    ----------
    ff : mule.FieldsFile
        The UM fields file object whose header will be updated.
    new_year : int
        The new year to set in the file header.
    new_month : int
        The new month to set in the file header.
    new_day : int
        The new day to set in the file header.

    Returns
    -------
    None
    """

    if new_year is not None:
        ff.fixed_length_header.t1_year = new_year
        ff.fixed_length_header.t2_year = new_year
    if new_month is not None:
        ff.fixed_length_header.t1_month = new_month
        ff.fixed_length_header.t2_month = new_month
    if new_day is not None:
        ff.fixed_length_header.t1_day = new_day
        ff.fixed_length_header.t2_day = new_day

def change_header_date_all_fields(ff, new_year, new_month, new_day):
    """
    Update the header date of each field in the  UM fields file.

    Parameters
    ----------
    ff : mule.FieldsFile
        The UM fields file object whose header will be updated.
    new_year : int
        The new year to set in the file header.
    new_month : int
        The new month to set in the file header.
    new_day : int
        The new day to set in the file header.

    Returns
    -------
    None
    """

    for field in ff.fields:
        if new_year is not None:
            field.lbyr = new_year
        if new_month is not None:
            field.lbmon = new_month
        if new_day is not None:
            field.lbdat = new_day

def create_default_outname(filename, suffix="_newdate"):
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
    
def void_validation(*args, **kwargs):
    """
    Don't perform the validation, but print a message to inform that validation has been skipped.
    """
    print('Skipping mule validation. To enable the validation, run using the "--validate" option.')

def main():
    """
    Main function to load, modify, and save the UM dump file.
    """
    args = parse_args()
    
    ff = mule.load_umfile(args.ifile)

    output_file = create_default_outname(args.ifile) if args.output_path is None else args.output_path
    
    # Skip mule validation if the "--validate" option is provided
    if not args.validate:
        ff.validate = void_validation

    change_header_date_file(ff, args.year, args.month, args.day)
    change_header_date_all_fields(ff, args.year, args.month, args.day)

    # Create the output filename

    ff.to_file(output_file)
    

if __name__== "__main__":

    main() # pragma: no cover
