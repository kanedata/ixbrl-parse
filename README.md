# ixbrl-parse

![Test status](https://github.com/kanedata/ixbrl-parse/workflows/tests/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/ixbrlparse)](https://pypi.org/project/ixbrlparse/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ixbrlparse)
![PyPI - License](https://img.shields.io/pypi/l/ixbrlparse)
[![Documentation Status](https://readthedocs.org/projects/ixbrl-parse/badge/?version=latest)](https://ixbrl-parse.readthedocs.io/en/latest/?badge=latest)

A python module for getting useful data out of iXBRL™ and XBRL™ files. The library is at an early stage - feedback and improvements are very welcome.

Full documentation is available at [ixbrl-parse.readthedocs.io](https://ixbrl-parse.readthedocs.io/)

For more about the iXBRL™ and XBRL™ standards, see the [specification site](https://specifications.xbrl.org/)
and [XBRL International](https://www.xbrl.org/). This tool is not affiliated with XBRL International.

**[Changelog](https://ixbrl-parse.readthedocs.io/en/latest/changelog/)**

## Requirements

The module requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [lxml](https://lxml.de/) to parse the documents.

If you're using Python 3.13 you may need to ensure that the `libxml2-dev` and `libxslt-dev` packages have been installed.

[word2number](https://github.com/akshaynagpal/w2n) is used to process the
numeric items with the `numsenwords` format.

## How to install

You can install from pypi using pip:

```
pip install ixbrlparse
```

## How to use

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

You can also use as a python module (see [the documentation](https://ixbrl-parse.readthedocs.io/en/latest/python-module/) for more details)

## Development

The module is setup for development using [hatch](https://hatch.pypa.io/latest/). It should be possible to run tests and linting without needed hatch, however.

### Run tests

Tests can be run with `pytest`:

```bash
hatch run test
```

Without hatch, you'll need to run:

```bash
pip install -e .[test]
python -m pytest tests
```

### Test coverage

Run tests then report on coverage

```bash
hatch run cov
```

Without hatch, you'll need to run:

```bash
pip install -e .[test]
coverage run -m pytest tests
coverage report
```

Run tests then run a server showing where coverage is missing

```bash
hatch run cov-html
```

Without hatch, you'll need to run:

```bash
pip install -e .[test]
coverage run -m pytest tests
coverage report
coverage html
python -m http.server -d htmlcov
```

### Run typing checks

```bash
hatch run lint:typing
```

Without hatch, you'll need to run:

```bash
pip install -e .[lint]
mypy --install-types --non-interactive src/ixbrlparse tests
```

### Linting

Ruff should be run before committing any changes.

To check for any changes needed:

```bash
hatch run lint:style
```

Without hatch, you'll need to run:

```bash
pip install -e .[lint]
ruff check .
ruff format --check --diff .
```

To run any autoformatting possible:

```sh
hatch run lint:fmt
```

Without hatch, you'll need to run:

```bash
pip install -e .[lint]
ruff format .
ruff check --fix .
```

### Run all checks at once

```sh
hatch run lint:all
```

Without hatch, you'll need to run:

```bash
pip install -e .[lint]
ruff check .
ruff format --check --diff .
mypy --install-types --non-interactive src/ixbrlparse tests
```

## Publish to pypi

```bash
hatch build
hatch publish
git tag v<VERSION_NUMBER>
git push origin v<VERSION_NUMBER>
```

## Acknowledgements

Developed by [David Kane](https://dkane.net/) of [Kane Data Ltd](https://kanedata.co.uk/)

Originally developed for a project with
[Power to Change](https://www.powertochange.org.uk/) looking at how to extract data from
financial documents of community businesses.

Thanks to the following users for their contributions:

- [@avyfain](https://github.com/avyfain)
- [@wcollinscw](https://github.com/wcollinscw)
- [@ajmarks](https://github.com/ajmarks)
- [@adobrinevski](https://github.com/adobrinevski)
- [@JWFB](https://github.com/JWFB)
- [@vin0110](https://github.com/vin0110)

XBRL™ and iXBRL™ are trademarks of XBRL International, Inc. All rights reserved.

The XBRL™ standards are open and freely licensed by way of the XBRL International License Agreement. Our use of these trademarks is permitted by XBRL International in accordance with the XBRL International Trademark Policy.
