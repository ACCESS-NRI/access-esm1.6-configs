#!/usr/bin/env python3
import argparse
import cftime


parser = argparse.ArgumentParser(
    prog = "sec_year_1",
    description=(
        "Calculate seconds between 1/1/1 and input date "
        "using proleptic gregorian calendar"
    )
)
parser.add_argument("year", type=int)
parser.add_argument("month", type=int)
parser.add_argument("day", type=int)


if __name__ == "__main__":
    args = parser.parse_args()

    start = cftime.datetime(1, 1, 1, calendar="proleptic_gregorian")
    end = cftime.datetime(args.year, args.month, args.day, calendar="proleptic_gregorian")
    print((end-start).total_seconds())
