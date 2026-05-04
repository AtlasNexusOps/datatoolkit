# Data Toolkit

Convert, validate, clean. JSON ↔ CSV ↔ YAML ↔ XML.
Batch processing, dedup, normalization. Python CLI. MIT license.

## Install

```bash
pip install -r requirements.txt
```

## Usage

### Convert

```bash
# JSON → CSV
python dtk.py convert data.json -o data.csv

# CSV → JSON with cleaning
python dtk.py convert data.csv -o data.json --clean

# YAML → XML
python dtk.py convert config.yaml -f xml -o config.xml
```

### Validate

```bash
python dtk.py validate data.csv
# → {"total_rows": 342, "columns": ["name","price"], "null_counts": ...}
```

### Clean

```bash
# Dedup + normalize numbers
python dtk.py clean messy.csv -o clean.csv

# No dedup, normalize only
python dtk.py clean data.json -o data.json --no-dedup
```

### Batch split

```bash
# Split into 100-line chunks
python dtk.py batch big.csv 100 ./chunks/
# → chunk_001.csv, chunk_002.csv, ...
```

## Supported Formats

| Format | Read | Write |
|--------|------|-------|
| JSON   | ✓    | ✓     |
| CSV    | ✓    | ✓     |
| YAML   | ✓    | ✓     |
| XML    | ✓    | ✓     |

## Cleaning Features

- **Dedup** — remove duplicate rows
- **Normalize** — auto-detect numbers, strip whitespace, handle nulls

Built by Atlas Nexus. MIT License.
