# Nonnumeric

[Ixbrl-parse Index](../../README.md#ixbrl-parse-index) /
[Ixbrlparse](../index.md#ixbrlparse) /
[Components](./index.md#components) /
Nonnumeric

> Auto-generated documentation for [ixbrlparse.components.nonnumeric](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/nonnumeric.py) module.

- [Nonnumeric](#nonnumeric)
  - [ixbrlNonNumeric](#ixbrlnonnumeric)
    - [ixbrlNonNumeric().to_json](#ixbrlnonnumeric()to_json)

## ixbrlNonNumeric

[Show source in nonnumeric.py:4](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/nonnumeric.py#L4)

Models a non-numeric element in an iXBRL document

Non-numeric elements are used to store information such as the name of the
entity, the name of the reporting period, etc.

The value of non-numeric elements is always a string, so we don't need to
worry about parsing the string.

#### Attributes

- `context` *ixbrlContext* - The context of the non-numeric element
- `name` *str* - The name of the non-numeric element
- `format` *str* - The format of the non-numeric element
- `value` *str* - The value of the non-numeric element

#### Signature

```python
class ixbrlNonNumeric:
    def __init__(self, context, name, format_, value):
        ...
```

### ixbrlNonNumeric().to_json

[Show source in nonnumeric.py:33](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/nonnumeric.py#L33)

#### Signature

```python
def to_json(self):
    ...
```


