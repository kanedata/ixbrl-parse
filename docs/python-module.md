# Python module

## Import the `IXBRL` class which parses the file.

```python
from ixbrlparse import IXBRL
```

## Initialise an object and parse the file

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


## Get the contexts and units used in the data

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

## Get financial facts

Numeric facts are stored in `x.numeric` as a list of `ixbrlNumeric` objects.
The `ixbrlNumeric.value` object contains the value as a parsed python number
(after the sign and scale formatting values have been applied).

`ixbrlNumeric.context` holds the context object relating to this value.
The `.name` and `.schema` values give the key of this value, according to
the applied schema.

Non-numeric facts are stored in `x.nonnumeric` as a list of `ixbrlNonnumeric`
objects, with similar `.value`, `.context`, `.name` and `.schema` values. 
The value of `.value` will be a string for non-numeric facts.

## Check for any parsing errors

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
  #   ixbrlError(
  #     error=<NotImplementedError>,
  #     element=<BeautifulSoupElement>
  #   )
  # ]
```

Note that the error catching is only available for parsing of `.nonnumeric`
and `numeric` items in the document, as well as context items.
Any other errors with parsing will be thrown as normal no matter what
`raise_on_error` is set to. Errors in `context` items may make it more difficult
to use the resulting data. 
