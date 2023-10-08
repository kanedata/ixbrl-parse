# Command line

You can run the module directly to extract data from an iXBRL™ file.

```bash
ixbrlparse example_file.html
# or
python -m ixbrlparse example_file.html
```

While primarily designed for iXBRL™ files, the parser should also work
for XBRL™ files.

The various options for using this can be found through:

```bash
python -m ixbrlparse -h
# optional arguments:
#   -h, --help            show this help message and exit
#   --outfile OUTFILE     Where to output the file
#   --format {csv,json,jsonlines,jsonl}
#                         format of the output
#   --fields {numeric,nonnumeric,all}
#                         Which fields to output
```
