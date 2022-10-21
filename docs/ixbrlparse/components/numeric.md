# Numeric

[Ixbrl-parse Index](../../README.md#ixbrl-parse-index) /
[Ixbrlparse](../index.md#ixbrlparse) /
[Components](./index.md#components) /
Numeric

> Auto-generated documentation for [ixbrlparse.components.numeric](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/numeric.py) module.

- [Numeric](#numeric)
  - [ixbrlNumeric](#ixbrlnumeric)
    - [ixbrlNumeric().to_json](#ixbrlnumeric()to_json)

## ixbrlNumeric

[Show source in numeric.py:6](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/numeric.py#L6)

Models a numeric element in an iXBRL document

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
class ixbrlNumeric:
    def __init__(self, attrs):
        ...
```

### ixbrlNumeric().to_json

[Show source in numeric.py:45](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/numeric.py#L45)

#### Signature

```python
def to_json(self):
    ...
```


