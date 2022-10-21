# Transform

[Ixbrl-parse Index](../../README.md#ixbrl-parse-index) /
[Ixbrlparse](../index.md#ixbrlparse) /
[Components](./index.md#components) /
Transform

> Auto-generated documentation for [ixbrlparse.components.transform](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py) module.

- [Transform](#transform)
  - [ixbrlFormat](#ixbrlformat)
    - [ixbrlFormat().parse_value](#ixbrlformat()parse_value)
    - [ixbrlFormat().to_json](#ixbrlformat()to_json)
  - [ixtFixedFalse](#ixtfixedfalse)
    - [ixtFixedFalse().parse_value](#ixtfixedfalse()parse_value)
  - [ixtFixedTrue](#ixtfixedtrue)
    - [ixtFixedTrue().parse_value](#ixtfixedtrue()parse_value)
  - [ixtNoContent](#ixtnocontent)
    - [ixtNoContent().parse_value](#ixtnocontent()parse_value)
  - [ixtNumComma](#ixtnumcomma)
    - [ixtNumComma().parse_value](#ixtnumcomma()parse_value)
  - [ixtNumWordsEn](#ixtnumwordsen)
    - [ixtNumWordsEn().parse_value](#ixtnumwordsen()parse_value)
  - [ixtZeroDash](#ixtzerodash)
    - [ixtZeroDash().parse_value](#ixtzerodash()parse_value)
  - [get_format](#get_format)

## ixbrlFormat

[Show source in transform.py:4](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L4)

Base class for all iXBRL formats

By default it attempts to convert a string to numbers by removing
commas and spaces, and then converting to a float. It also supports
negative numbers and scaling.

#### Attributes

- `format` *str* - The name of the format of the numeric element
- `decimals` *int* - The number of decimal places of the numeric element
- `scale` *int* - The scale of the numeric element. The scale is represented
    as a power of 10. For example, a scale of 3 would mean that the
    value should be multiplied by 1000.
- `sign` *str* - The sign of the numeric element. If sign is "-", then
    the value is multiplied by -1

#### Signature

```python
class ixbrlFormat:
    def __init__(self, format_, decimals, scale, sign):
        ...
```

### ixbrlFormat().parse_value

[Show source in transform.py:44](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L44)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `float` - The converted value

#### Signature

```python
def parse_value(self, value):
    ...
```

### ixbrlFormat().to_json

[Show source in transform.py:41](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L41)

#### Signature

```python
def to_json(self):
    ...
```



## ixtFixedFalse

[Show source in transform.py:127](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L127)

Models a fixed false numeric element in an iXBRL document

Always returns False

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtFixedFalse(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtFixedFalse().parse_value

[Show source in transform.py:142](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L142)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `bool` - The converted value (always False)

#### Signature

```python
def parse_value(self, value):
    ...
```



## ixtFixedTrue

[Show source in transform.py:154](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L154)

Models a fixed true numeric element in an iXBRL document

Always returns True

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtFixedTrue(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtFixedTrue().parse_value

[Show source in transform.py:169](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L169)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `bool` - The converted value (always True)

#### Signature

```python
def parse_value(self, value):
    ...
```



## ixtNoContent

[Show source in transform.py:100](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L100)

Models a no content numeric element in an iXBRL document

Always returns None

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtNoContent(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtNoContent().parse_value

[Show source in transform.py:115](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L115)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `None` - The converted value (always None)

#### Signature

```python
def parse_value(self, value):
    ...
```



## ixtNumComma

[Show source in transform.py:181](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L181)

Models a comma separated numeric element in an iXBRL document

This element is used for numbers where a comma is used as the decimal
separator. For example, 100,00 would be converted to 100.00.

It also assumes that any full stops are used as thousands separators.
For example, 1.000,00 would be converted to 1000.00.

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtNumComma(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtNumComma().parse_value

[Show source in transform.py:200](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L200)

Converts a string to a number

First removes any full stops, and then replaces any commas with
full stops. It then converts the string to a float.

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `float` - The converted value

#### Signature

```python
def parse_value(self, value):
    ...
```



## ixtNumWordsEn

[Show source in transform.py:217](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L217)

Models a numeric element in an iXBRL document that is written in words

Uses the [word2number](https://pypi.org/project/word2number/) library to
convert the words to a number.

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtNumWordsEn(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtNumWordsEn().parse_value

[Show source in transform.py:233](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L233)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `float` - The converted value

#### Signature

```python
def parse_value(self, value):
    ...
```



## ixtZeroDash

[Show source in transform.py:73](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L73)

Models a zero numeric element in an iXBRL document

Always returns 0

#### Attributes

dictionary containing the following keys:
    - `context` *ixbrlContext* - The context of the numeric element
    - `name` *str* - The name of the numeric element
    - `format` *ixbrlFormat* - The format of the numeric element
    - `value` *float* - The value of the numeric element
    - `unit` *str* - The unit of the numeric element
    - `text` *str* - The text of the numeric element

#### Signature

```python
class ixtZeroDash(ixbrlFormat):
    ...
```

#### See also

- [ixbrlFormat](#ixbrlformat)

### ixtZeroDash().parse_value

[Show source in transform.py:88](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L88)

Converts a string to a number

#### Arguments

- `value` *str* - The string to convert

#### Returns

- `int` - The converted value (always 0)

#### Signature

```python
def parse_value(self, value):
    ...
```



## get_format

[Show source in transform.py:250](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/transform.py#L250)

Returns the correct format class for the given format

Only particular formats are supported. If the format is not supported
then a NotImplementedError is raised.

#### Signature

```python
def get_format(format_):
    ...
```


