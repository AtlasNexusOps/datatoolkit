# Atlas Data Toolkit — Portable Edition

**ZERO install. Just Python 3.9+.** Works on Windows, Android (Termux), Linux, macOS.

## Download

Go to [Releases](https://github.com/AtlasNexusTech/datatoolkit/releases) and grab `datatoolkit-portable-v0.1.0.zip`.

## Quick Start

### Windows
```batch
python datatoolkit-portable.py convert data.csv -o data.json
```
Or just double-click `datatoolkit.bat` with your arguments.

### Android (Termux)
```bash
pkg install python
python datatoolkit-portable.py validate data.csv
```

### Linux / macOS
```bash
python3 datatoolkit-portable.py clean messy.json -o clean.json
```

## Commands

| Command | What it does |
|---|---|
| `convert` | Convert between JSON ↔ CSV (YAML/XML with pip) |
| `validate` | Check data quality — nulls, empties, row counts |
| `clean` | Normalize whitespace, remove duplicates |
| `batch` | Split large files into smaller chunks |

## Formats

- **JSON** and **CSV** — work out of the box, zero dependencies
- **YAML** — requires `pip install pyyaml`
- **XML** — bundled vendor/xmltodict.py included, zero extra deps

## vs pip version

| | `pip install atlas-datatoolkit` | Portable |
|---|---|---|
| JSON/CSV | ✅ | ✅ |
| YAML | ✅ (auto-installed) | ❌ (needs `pip install pyyaml`) |
| XML | ✅ (auto-installed) | ✅ (bundled) |
| Global command `datatoolkit` | ✅ | ❌ (use `python datatoolkit-portable.py`) |
| Needs pip | Yes | **No** |
