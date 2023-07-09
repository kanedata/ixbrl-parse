# Development

The module is setup for development using [hatch](https://hatch.pypa.io/latest/).

## Run tests

Tests can be run with `pytest`:

```bash
hatch run test
```

## Test coverage

Run tests then report on coverage

```bash
hatch run cov
```

Run tests then run a server showing where coverage is missing

```bash
hatch run cov-html
```

## Run typing checks

```bash
hatch run lint:typing
```

## Linting

Black and ruff should be run before committing any changes.

To check for any changes needed:

```bash
hatch run lint:style
```

To run any autoformatting possible:

```sh
hatch run lint:fmt
```

## Run all checks at once

```sh
hatch run lint:all
```

# Publish to pypi

```bash
hatch build
hatch publish
git tag v<VERSION_NUMBER>
git push origin v<VERSION_NUMBER>
```