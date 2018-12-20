# ixbrl-parse

A python module for getting useful data out of ixbrl files. Currently in develop for a project with 
[Power to Change](https://www.powertochange.org.uk/) looking at how to extract data from 
financial documents of community businesses. The library is at an early stage

## Requirements

The module requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse the documents.

## How to use

### Run the python module

You can run the module directly to extract data from an IXBRL file.

```bash
python -m ixbrlparse example_file.html
```

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

### Use as a python module

An example of usage is shown in [`test.py`](test.py).

#### Import the `IXBRL` class which parses the file.

```python
from ixbrlparse import IXBRL
```

#### Initialise an object and parse the file

You need to pass a file handle or other object with a `.read()` method.

```python
with open('sample_ixbrl.html') as a:
  x = IXBRL(a)
```

#### Get the contexts and units used in the data

These are held in the object. The contexts are stored as a dictionary with the context
id as the key, and a `ixbrlContext` object as the value.

```python
print(x.contexts)
# {
#    "cfwd_2018_03_31": ixbrlContext(
#       _id="cfwd_2018_03_31",
#       entity="0123456", # company number
#       segment=None, # used for hypercubes
#       dimension=None, # used for hypercubes
#       instant="2018-03-31",
#       startdate=None, # used for periods
#       enddate=None, # used for periods
#    ),
#    ....
# }
```

The units are stored as key:value dictionary entries
```python
print(x.units)
# {
#    "GBP": "ISO4107:GBP"
#    "shares": "shares"
# }
```

#### Get financial facts

Numeric facts are stored in `x.numeric` as a list of `ixbrlNumeric` objects.
The `ixbrlNumeric.value` object contains the value as a parsed python number
(after the sign and scale formatting values have been applied).

`ixbrlNumeric.context` holds the context object relating to this value.
The `.name` and `.schema` values give the key of this value, according to
the applied schema.

Non-numeric facts are stored in `x.nonnumeric` as a list of `ixbrlNonnumeric`
objects, with similar `.value`, `.context`, `.name` and `.schema` values. 
The value of `.value` will be a string for non-numeric facts.

## Run tests

Tests can be run with `pytest`:

```bash
pip install -e . # install the package
pytest
```
