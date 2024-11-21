import csv
import json
import logging
import sys
from datetime import date
from typing import Any

import click

from ixbrlparse.__about__ import __version__
from ixbrlparse.core import IXBRL

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(name)s:%(message)s")


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="IXBRLParse")
@click.option(
    "--format",
    "-f",
    "output_format",
    default="csv",
    help="Output format",
    type=click.Choice(["csv", "json", "jsonlines", "jsonl"]),
)
@click.option(
    "--fields", default="all", type=click.Choice(["numeric", "nonnumeric", "all"]), help="Which fields to output"
)
@click.option("--outfile", default=sys.stdout, help="Where to output the file", type=click.File("w", encoding="UTF-8"))
@click.argument("infile", type=click.File("rb"), default=sys.stdin, nargs=1)
def ixbrlparse_cli(output_format: str, fields: str, outfile, infile):
    x = IXBRL(infile)

    if output_format == "csv":
        values = x.to_table(fields)
        columns: dict[str, Any] = {}
        for r in values:
            columns = {**dict.fromkeys(r.keys()), **columns}
        writer = csv.DictWriter(outfile, columns.keys())
        writer.writeheader()
        writer.writerows(values)
    elif output_format in ["jsonlines", "jsonl"]:
        values = x.to_table(fields)
        for v in values:
            if isinstance(v["value"], date):
                v["value"] = str(v["value"])
            json.dump(v, outfile)
            outfile.write("\n")
    elif output_format == "json":
        json.dump(x.to_json(), outfile, indent=4)
