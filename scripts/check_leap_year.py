import argparse
import datetime
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('calendar_file', help='Path to UM restart calendar file.')

    return parser.parse_args()


def is_leap(year):
    return (year % 4 == 0) and ((year % 400 == 0) or not (year % 100 == 0))


def get_restart_date(calendar_file):
    with open(calendar_file, 'r') as calendar:
        date_info = yaml.safe_load(calendar)

    restart_date = date_info['end_date']

    if not isinstance(restart_date, datetime.date):
        raise TypeError(
            "Failed to parse restart calendar file contents into "
            "datetime object. "
            f"Calendar file: {calendar_file}"
        )
    return restart_date


if __name__ == "__main__":
    args = parse_args()

    restart_date = get_restart_date(args.calendar_file)

    if is_leap(restart_date.year):
        raise RuntimeError(
                f"Year {restart_date.year} in restart file is a leap year. Restart date modifications will not work "
                "for leap years."
        )
