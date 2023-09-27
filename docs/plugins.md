# Plugins

The module allows for plugins to customize functionality, using the [pluggy](https://pluggy.readthedocs.io/en/stable/) framework.

The only current plugin endpoint is to add more Formatters. A formatter takes a value from a ixbrl item and converts it into the appropriate python value. For example, the `ixtNumWordsEn` formatter would take a value like "eighty-five" and turn it into 85.

The formats used within ixbrl files can vary between schemas and countries. Rather than try to cover everything in this module, you can write a plugin to support the format that you need.

## Creating a plugin

### Create a custom format class

To create a plugin, you first need to create a new format class that subclasses `ixbrlparse.ixbrlFormat`. This has two key components:

- a `format_names` attribute which consists of a tuple of possible names for the format. These are the values that will be checked against the ixbrl items. These names must not clash with other formats that have already been defined.
- a `parse_value` function which takes the original text value and returns the processed value.

An example class might look like (in the file `ixbrlparse-dateplugin/ixbrlparse_dateplugin.py`):

```python
import ixbrlparse

class ixtParseIsoDate(ixbrlparse.ixbrlFormat):
    format_names = ("isodateformat")

    def parse_value(self, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d").astimezone().date()
```

### Hook into ixbrlparse

Next you need to add a function which will hook into ixbrlparse at the right point. This function needs to be called `ixbrl_add_formats`, and returns a list of new format classes (added to the bottom of `ixbrlparse-dateplugin/ixbrlparse_dateplugin.py`):

```python
@ixbrlparse.hookimpl
def ixbrl_add_formats():
    return [ixtParseIsoDate]
```

or

```python
@ixbrlparse.hookimpl(specname="ixbrl_add_formats")
def add_new_ixbrl_formats():
    return [ixtParseIsoDate]
```

You then need to add an entrypoint to `setup.py` or to `pyproject.toml` which will be activated when your project is installed. This should look something like (using an example `ixbrlparse-dateplugin/setup.py`):

```python
from setuptools import setup

setup(
    name="ixbrlparse-dateplugin",
    install_requires="ixbrlparse",
    entry_points={"ixbrlparse": ["dateplugin = ixbrlparse_dateplugin"]},
    py_modules=["ixbrlparse_dateplugin"],
)
```

### Install the plugin

If you then install the plugin it should be picked up by ixbrlparse and will also include the additional formats when checking.

## Acknowledgements

The implementation of pluggy used here draws heavily on [pluggy's own tutorial](https://pluggy.readthedocs.io/en/stable/#a-complete-example) and @simonw's [implementation of plugins for datasette](https://docs.datasette.io/en/stable/plugins.html).
