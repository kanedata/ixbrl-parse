# ixbrl-parse


![Test status](https://github.com/drkane/ixbrl-parse/workflows/tests/badge.svg)
[![PyPI version](https://badge.fury.io/py/ixbrlparse.svg)](https://pypi.org/project/ixbrlparse/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ixbrlparse)
![PyPI - License](https://img.shields.io/pypi/l/ixbrlparse)

A python module for getting useful data out of ixbrl files. The library is at an early stage - feedback and improvements are very welcome.

**New in version 0.4**: I've added initial support for pure XBRL files as well as tagged HTML iXBRL files. Feedback on this feature is welcome - particularly around getting values out of numeric items.

## Requirements

The module requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [lxml](https://lxml.de/) to parse the documents.

[word2number](https://github.com/akshaynagpal/w2n) is used to process the
numeric items with the `numsenwords` format.

## How to install

You can install from pypi using pip:

```
pip install ixbrlparse
```

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
with open('sample_ixbrl.html', encoding="utf8") as a:
  x = IXBRL(a)
```

If your IXBRL data comes as a string then use a `io.StringIO` wrapper to
pass it to the class:

```python
import io
from ixbrlparse import IXBRL

content = '''<some ixbrl content>'''
x = IXBRL(io.StringIO(content))
```


#### Get the contexts and units used in the data

These are held in the object. The contexts are stored as a dictionary with the context
id as the key, and a `ixbrlContext` object as the value.

```python
print(x.contexts)
# {
#    "cfwd_2018_03_31": ixbrlContext(
#       id="cfwd_2018_03_31",
#       entity="0123456", # company number
#       segments=[], # used for hypercubes
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

#### Check for any parsing errors

By default, the parser will throw an exception if it encounters an error
when processing the document.

You can parse `raise_on_error=False` to the initial object to suppress
these exceptions. You can then access a list of the errors (and the element)
that created them through the `.errors` attribute. For example:

```python
with open('sample_ixbrl.html', encoding="utf8") as a:
  x = IXBRL(a, raise_on_error=False)
  print(x.errors) # populated with any exceptions found
  # [ eg...
  #   {
  #     "error": <NotImplementedError>,
  #     "element": <BeautifulSoupElement>
  #   }
  # ]
```

Note that the error catching is only available for parsing of `.nonnumeric`
and `numeric` items in the document. Any other errors with parsing will be
thrown as normal no matter what `raise_on_error` is set to.

## Run tests

Tests can be run with `pytest`:

```bash
pip install -e . # install the package
pytest tests
```

## Linting

Black and isort should be run before committing any changes.

```bash
isort ixbrlparse tests
black ixbrlparse tests
```

## Publish to pypi

```bash
python -m build
twine upload dist/*
```

## Install development version

The development requirements are installed using `pip install -r dev-requirements.txt`.

Any additional requirements for the module itself must be added to
`install_requires` in `setup.py`. You should then generate a new 
`requirements.txt` using using [`pip-tools`](https://github.com/jazzband/pip-tools) (`pip-compile`). You can then run `pip-sync` to install the 
requirement.

Any additional development requirements must be added to `dev-requirements.in`
and then the `dev-requirements.txt` should be generated using `pip-compile dev-requirements.in`. You can then install the development requirements using
`pip-sync dev-requirements.txt`.

## Acknowledgements

Originally developed for a project with 
[Power to Change](https://www.powertochange.org.uk/) looking at how to extract data from 
financial documents of community businesses.
