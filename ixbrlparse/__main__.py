import argparse
import csv
import json
from .core import IXBRL


def main():

    parser = argparse.ArgumentParser(description='Extract financial data from a IXBRL file')
    parser.add_argument('infile',
                        help='file to open and convert',
                        type=argparse.FileType('r')
                        )
    parser.add_argument('--outfile',
                        default="-",
                        help='Where to output the file',
                        type=argparse.FileType('w', encoding='UTF-8')
                        )
    parser.add_argument('--format',
                        choices=['csv', 'json', 'jsonlines', 'jsonl'],
                        default="csv",
                        help='format of the output'
                        )
    parser.add_argument('--fields',
                        choices=['numeric', 'nonnumeric', 'all'],
                        default="all",
                        help='Which fields to output'
                        )

    args = parser.parse_args()

    x = IXBRL(args.infile)

    if args.format == 'csv':
        values = x.to_table(args.fields)
        writer = csv.DictWriter(args.outfile, values[0].keys())
        writer.writeheader()
        writer.writerows(values)
    elif args.format in ['jsonlines', 'jsonl']:
        values = x.to_table(args.fields)
        for v in values:
            json.dump(v, args.outfile)
            args.outfile.write("\n")
    elif args.format == "json":
        json.dump(x.to_json(), args.outfile, indent=4)


if __name__ == "__main__":
    main()
