# Context

[Ixbrl-parse Index](../../README.md#ixbrl-parse-index) /
[Ixbrlparse](../index.md#ixbrlparse) /
[Components](./index.md#components) /
Context

> Auto-generated documentation for [ixbrlparse.components.context](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/context.py) module.

- [Context](#context)
  - [ixbrlContext](#ixbrlcontext)
    - [ixbrlContext().to_json](#ixbrlcontext()to_json)

## ixbrlContext

[Show source in context.py:5](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/context.py#L5)

Models a context in an iXBRL document

#### Attributes

- `id` *str* - The id of the context
- `entity` *str* - The entity of the context
- `segments` *list* - A list of segments
- `instant` *datetime.date* - The instant of the context
- `startdate` *datetime.date* - The start date of the context
- `enddate` *datetime.date* - The end date of the context

#### Signature

```python
class ixbrlContext:
    def __init__(self, _id, entity, segments, instant, startdate, enddate):
        ...
```

### ixbrlContext().to_json

[Show source in context.py:46](https://github.com/drkane/ixbrl-parse/blob/main/ixbrlparse/components/context.py#L46)

#### Signature

```python
def to_json(self):
    ...
```


