# Atlas Data Toolkit

[![CI](https://github.com/AtlasNexusOps/datatoolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/AtlasNexusOps/datatoolkit/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/atlas-datatoolkit?color=blue)](https://pypi.org/project/atlas-datatoolkit/)


Small, dependency-light CLI for converting, validating, cleaning and batching operational data files.

Atlas Data Toolkit is the productized version of the earlier `datatoolkit` prototype. It is intentionally simple: one Python CLI that helps turn messy CSV/JSON/YAML/XML files into clean handoff artifacts for dashboards, automations and client data pipelines.

## Use cases

- Convert client exports between CSV, JSON, YAML and XML.
- Validate row counts, columns, nulls and empty strings before delivery.
- Normalize whitespace and numeric values.
- Remove duplicate rows.
- Split large files into smaller batches for review or processing.

## Install

```bash
git clone https://github.com/AtlasNexusOps/datatoolkit.git
cd datatoolkit
pip install -r requirements.txt
```

## CLI examples

### Convert files

```bash
# JSON → CSV
python dtk.py convert data.json -o data.csv

# CSV → JSON with cleanup
python dtk.py convert messy.csv -o clean.json --clean

# YAML → XML
python dtk.py convert config.yaml -f xml -o config.xml
```

### Validate a dataset

```bash
python dtk.py validate data.csv
```

Example output:

```json
{
  "total_rows": 342,
  "total_columns": 5,
  "columns": ["name", "price", "category", "url", "updated_at"],
  "null_counts": {
    "name": 0,
    "price": 2
  },
  "empty_strings": {
    "name": 0,
    "price": 2
  }
}
```

### Clean a file

```bash
# Deduplicate + normalize numeric strings
python dtk.py clean messy.csv -o clean.csv

# Normalize only, keep duplicates
python dtk.py clean data.json -o normalized.json --no-dedup
```

### Split into batches

```bash
python dtk.py batch big.csv 100 ./chunks/
```

Output:

```text
chunks/chunk_001.csv
chunks/chunk_002.csv
...
```

## Supported formats

| Format | Read | Write |
|---|---:|---:|
| JSON | yes | yes |
| CSV | yes | yes |
| YAML | yes | yes |
| XML | yes | yes |

## Repository structure

```text
.
├── dtk.py              # CLI implementation
├── requirements.txt    # pyyaml + xmltodict
├── README.md           # product documentation
└── LICENSE             # MIT
```

## Design principles

- **Boring is good** — standard formats, simple CLI, no service dependency.
- **Pipeline-friendly** — commands can be used inside cron jobs, scripts and agent workflows.
- **Client-delivery oriented** — outputs are easy to inspect and hand off.
- **Small surface area** — suitable for quick customization during micro-builds.

## Atlas Nexus context

This repository supports Atlas Nexus data-operation offers:

- data cleanup;
- dashboard preparation;
- conversion of client exports;
- repeatable micro-pipelines;
- pre-validation before automation.

Main Atlas Nexus site:

https://atlasnexusops.github.io/

## License

MIT — Atlas Nexus, 2026
