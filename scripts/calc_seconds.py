#!/usr/bin/env python3

# Calculate the number of seconds from 1/1/1 to a specified date, using
# the Proleptic Gregorian calendar
import argparse
import cftime


def parse_args():
    parser = argparse.ArgumentParser(
        description="# Calculate the number of seconds from 1/1/1 to a specified date using the Proleptic Gregorian calendar"
    )
    parser.add_argument(
        "-y",
        dest="year",
        help="restart date year",
        type=int
    )
    parser.add_argument(
        "-m",
        dest="month",
        help="restart date month",
        type=int
    )
    parser.add_argument(
        "-d",
        dest="day",
        help="restart date day of month",
        type=int
    )

    return parser.parse_args()


def main():
    args = parse_args()

    start = cftime.datetime(1, 1, 1, calendar="proleptic_gregorian")
    end = cftime.datetime(args.year, args.month, args.day, calendar="proleptic_gregorian")

    seconds = (end - start).total_seconds()

    print(seconds)


if __name__ == "__main__":
    main()
