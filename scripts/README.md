# scripts/

This directory contains **utility scripts, CLI tools, and batch jobs** for data processing and automation.

## Purpose

- Place all **standalone Python scripts** here.
- Scripts are intended to be executed directly from the command line.
- Scripts may import reusable logic from `/src/`, but should not duplicate it.

## Usage Example

```bash
# With Rye-managed virtual environment:
rye run python scripts/generate_sample_data.py --file "data/raw/input.xlsx" --out "data/processed/output.json"
```

## Guidelines

- Use `argparse` or `click` for command-line argument parsing.
- Focus each script on one main task.
- For shared logic (e.g., data extraction), **always import from `/src/` modules** instead of duplicating code.
- Clearly document each script’s expected arguments, input/output, and dependencies in the header docstring.
- Do **not** import or call other scripts from this directory. Only use modules from `/src/`.

## Structure Example

```
scripts/
  generate_sample_data.py  # calls functions from src/myproject/data_extraction.py
  batch_convert.py
  ...
```

## Further Reading

- All core logic and reusable code is in `/src/` (see `/src/README.md`).
- Tests for reusable modules should be placed in `/tests/`.
