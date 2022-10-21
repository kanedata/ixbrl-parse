# Core

[Ixbrl-parse Index](../README.md#ixbrl-parse-index) /
[Ixbrlparse](./index.md#ixbrlparse) /
Core

> Auto-generated documentation for [ixbrlparse.core](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py) module.

- [Core](#core)
  - [IXBRL](#ixbrl)
    - [IXBRL.open](#ixbrlopen)
    - [IXBRL().to_json](#ixbrl()to_json)
    - [IXBRL().to_table](#ixbrl()to_table)
  - [IXBRLParser](#ixbrlparser)
    - [IXBRLParser().parse](#ixbrlparser()parse)
  - [XBRLParser](#xbrlparser)

## IXBRL

[Show source in core.py:248](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L248)

Class to parse and store the results of an IXBRL file

This class wraps around the IXBRLParser or XBRLParser classes to parse the file and store the results

#### Signature

```python
class IXBRL:
    def __init__(self, f, raise_on_error=True):
        ...
```

### IXBRL.open

[Show source in core.py:259](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L259)

Open an IXBRL file from a filename and return an IXBRL object

#### Signature

```python
@classmethod
def open(cls, filename, raise_on_error=True):
    ...
```

### IXBRL().to_json

[Show source in core.py:283](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L283)

Return the results as a JSON string

#### Signature

```python
def to_json(self):
    ...
```

### IXBRL().to_table

[Show source in core.py:295](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L295)

Return the results as a list of dicts

The fields argument can be "numeric", "nonnumeric" or "all" to return the numeric, non-numeric or all elements

The fields included are:

- schema (str)
- name (str) -- the name of the element
- value -- the value of the element. Can be number, str, None, or boolean
- unit (str) -- the unit of the element if present
- instant (date) -- the instant date of the element context if present
- startdate (date) -- the start date of the element context if present
- enddate (date) -- the end date of the element context if present
- segment:N (str) -- the Nth segment of the element context if present (can be repeated)

#### Signature

```python
def to_table(self, fields="numeric"):
    ...
```



## IXBRLParser

[Show source in core.py:9](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L9)

Core class for parsing XBRL and iXBRL files

Takes a BeautifulSoup object created from an XBRL or iXBRL file

#### Arguments

- `soup` *BeautifulSoup* - BeautifulSoup object created from an XBRL or iXBRL file
- `raise_on_error` *bool* - Raise an error if an error is encountered (default: {True})

Public attributes:
    - `soup` *BeautifulSoup* - BeautifulSoup object created from an XBRL or iXBRL file
    - `raise_on_error` *bool* - Raise an error if an error is encountered
    - `errors` *list* - List of errors encountered
    - `schema` *str* - XBRL schema
    - `namespaces` *dict* - Namespaces used in the file
    - `contexts` *dict* - Contexts used in the file (uses the ixbrlContext class)
    - `units` *dict* - Units used in the file (as a dictionary of strings)
    - `nonnumeric` *list* - Non-numeric elements (uses the ixbrlNonNumeric class)
    - `numerics` *list* - Numeric elements (uses the ixbrlNumeric class)

#### Methods

- `parse` - Parse the file

#### Signature

```python
class IXBRLParser:
    def __init__(self, soup, raise_on_error=True):
        ...
```

### IXBRLParser().parse

[Show source in core.py:40](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L40)

Run all the parsing methods in the correct order

#### Signature

```python
def parse(self):
    ...
```



## XBRLParser

[Show source in core.py:168](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/core.py#L168)

Class to parse XBRL files

Extends the IXBRLParser class to use different methods for parsing XBRL files

#### Signature

```python
class XBRLParser(IXBRLParser):
    ...
```

#### See also

- [IXBRLParser](#ixbrlparser)


