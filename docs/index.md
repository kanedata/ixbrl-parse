# ixbrlParse

![Test status](https://github.com/kanedata/ixbrl-parse/workflows/tests/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/ixbrlparse)](https://pypi.org/project/ixbrlparse/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ixbrlparse)
![PyPI - License](https://img.shields.io/pypi/l/ixbrlparse)
[![Documentation Status](https://readthedocs.org/projects/ixbrl-parse/badge/?version=latest)](https://ixbrl-parse.readthedocs.io/en/latest/?badge=latest)

A python module for getting useful data out of iXBRL™ and XBRL™ files. The library is at an early stage - feedback and improvements are very welcome.

For more about the iXBRL™ and XBRL™ standards, see the [specification site](https://specifications.xbrl.org/)
and [XBRL International](https://www.xbrl.org/). This tool is not affiliated with XBRL International.

## Requirements

The module requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [lxml](https://lxml.de/) to parse the documents.

[word2number](https://github.com/akshaynagpal/w2n) is used to process the
numeric items with the `numsenwords` format.

## How to install

You can install from pypi using pip:

```
pip install ixbrlparse
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

XBRL™ and iXBRL™ are trademarks of XBRL International, Inc. All rights reserved.

The XBRL™ standards are open and freely licensed by way of the XBRL International License Agreement. Our use of these trademarks is permitted by XBRL International in accordance with the XBRL International Trademark Policy.
