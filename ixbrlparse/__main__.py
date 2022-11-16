import argparse
import csv
import json
import sys
from typing import Any

from ixbrlparse import __version__
from ixbrlparse.core import IXBRL


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Extract financial data from a IXBRL file"
    )
    parser.add_argument(
        "infile",
        help="file to open and convert",
        type=argparse.FileType("rb"),
        nargs="?",
        default=sys.stdin,
    )
    parser.add_argument(
        "--outfile",
        default="-",
        help="Where to output the file",
        type=argparse.FileType("w", encoding="UTF-8"),
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "jsonlines", "jsonl"],
        default="csv",
        help="format of the output",
    )
    parser.add_argument(
        "--fields",
        choices=["numeric", "nonnumeric", "all"],
        default="all",
        help="Which fields to output",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        action="store_true",
    )

    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    x = IXBRL(args.infile)

    if args.format == "csv":
        values = x.to_table(args.fields)
        columns: dict[str, Any] = {}
        for r in values:
            columns = {**dict.fromkeys(r.keys()), **columns}
        writer = csv.DictWriter(args.outfile, columns.keys())
        writer.writeheader()
        writer.writerows(values)
    elif args.format in ["jsonlines", "jsonl"]:
        values = x.to_table(args.fields)
        for v in values:
            json.dump(v, args.outfile)
            args.outfile.write("\n")
    elif args.format == "json":
        json.dump(x.to_json(), args.outfile, indent=4)


if __name__ == "__main__":
    main()
