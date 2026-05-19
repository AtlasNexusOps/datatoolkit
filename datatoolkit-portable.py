#!/usr/bin/env python3
"""
Atlas Data Toolkit — Portable Edition
========================================
Single-file CLI for converting, validating, cleaning and batching data.
NO pip required — just Python 3.9+.

Windows:  python datatoolkit-portable.py convert data.csv -o data.json
Android:  python datatoolkit-portable.py validate data.csv
Linux:    python3 datatoolkit-portable.py clean messy.json -o clean.json

Formats: JSON, CSV. YAML and XML are optional (require pip install pyyaml xmltodict).
"""

import argparse
import csv
import io
import json
import sys
import os
from pathlib import Path

# ── Vendor imports (no pip needed) ──────────────────────────
_VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
if (_VENDOR_DIR / "xmltodict.py").exists():
    sys.path.insert(0, str(_VENDOR_DIR))

HAS_YAML = False
try:
    import yaml
    HAS_YAML = True
except ImportError:
    pass

HAS_XML = False
try:
    import xmltodict
    HAS_XML = True
except ImportError:
    pass


# ── Loaders ─────────────────────────────────────────────────
def load_json(path: str) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def load_csv(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_yaml(path: str) -> list[dict]:
    if not HAS_YAML:
        raise ImportError("YAML support requires: pip install pyyaml")
    with open(path) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else [data]


def load_xml(path: str) -> list[dict]:
    if not HAS_XML:
        raise ImportError("XML support requires: pip install xmltodict")
    with open(path) as f:
        raw = xmltodict.parse(f.read())
    root_key = list(raw.keys())[0]
    items = raw[root_key]
    if isinstance(items, dict):
        items = [items]
    return items


# ── Savers ──────────────────────────────────────────────────
def save_json(data: list[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def save_csv(data: list[dict], path: str) -> None:
    if not data:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_yaml(data: list[dict], path: str) -> None:
    if not HAS_YAML:
        raise ImportError("YAML support requires: pip install pyyaml")
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def save_xml(data: list[dict], path: str, root_name: str = "root", item_name: str = "item") -> None:
    if not HAS_XML:
        raise ImportError("XML support requires: pip install xmltodict")
    with open(path, "w") as f:
        xmltodict.unparse({root_name: {item_name: data}}, output=f, pretty=True)


# ── Detection ──────────────────────────────────────────────
def detect_format(path: str) -> str:
    ext = Path(path).suffix.lower()
    mapping = {".json": "json", ".csv": "csv", ".yaml": "yaml", ".yml": "yaml", ".xml": "xml"}
    if ext in mapping:
        return mapping[ext]
    raise ValueError(f"Unknown format: {ext}")


# ── Operations ─────────────────────────────────────────────
def clean_data(data: list[dict], dedup: bool = True, normalize: bool = True) -> list[dict]:
    result = []
    seen = set()

    for row in data:
        if normalize:
            cleaned = {}
            for k, v in row.items():
                if v is None:
                    cleaned[k] = ""
                elif isinstance(v, str):
                    cleaned[k] = v.strip()
                elif isinstance(v, (int, float)):
                    cleaned[k] = v
                else:
                    cleaned[k] = str(v)
            row = cleaned

        if dedup:
            key = json.dumps(row, sort_keys=True, default=str)
            if key in seen:
                continue
            seen.add(key)

        result.append(row)

    return result


def validate_data(data: list[dict]) -> dict:
    report = {
        "total_rows": len(data),
        "total_columns": len(data[0]) if data else 0,
        "columns": list(data[0].keys()) if data else [],
        "null_counts": {},
        "empty_strings": {},
    }

    for col in report["columns"]:
        nulls = sum(1 for row in data if row.get(col) is None)
        empties = sum(1 for row in data if row.get(col) == "")
        if nulls:
            report["null_counts"][col] = nulls
        if empties:
            report["empty_strings"][col] = empties

    return report


# ── CLI Commands ────────────────────────────────────────────
LOADERS = {"json": load_json, "csv": load_csv, "yaml": load_yaml, "xml": load_xml}
SAVERS = {"json": save_json, "csv": save_csv, "yaml": save_yaml, "xml": save_xml}


def cmd_convert(args) -> None:
    fmt_in = detect_format(args.input)
    fmt_out = args.output_format or fmt_in
    data = LOADERS[fmt_in](args.input)

    if args.clean:
        data = clean_data(data, dedup=not args.no_dedup, normalize=not args.no_normalize)

    out_path = args.output or f"{Path(args.input).stem}.{fmt_out}"
    SAVERS[fmt_out](data, out_path)
    print(f"✅ Converted {len(data)} rows → {out_path}")


def cmd_validate(args) -> None:
    fmt_in = detect_format(args.input)
    data = LOADERS[fmt_in](args.input)
    report = validate_data(data)
    print(json.dumps(report, indent=2))


def cmd_clean(args) -> None:
    fmt_in = detect_format(args.input)
    fmt_out = args.output_format or fmt_in
    data = LOADERS[fmt_in](args.input)
    data = clean_data(data, dedup=not args.no_dedup, normalize=not args.no_normalize)

    out_path = args.output or f"{Path(args.input).stem}_clean.{fmt_out}"
    SAVERS[fmt_out](data, out_path)
    print(f"✅ Cleaned {len(data)} rows → {out_path}")


def cmd_batch(args) -> None:
    fmt_in = detect_format(args.input)
    fmt_out = args.output_format or fmt_in
    data = LOADERS[fmt_in](args.input)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = Path(args.input).stem

    for i in range(0, len(data), args.size):
        chunk = data[i : i + args.size]
        chunk_num = (i // args.size) + 1
        out_path = out_dir / f"{base}_{chunk_num:04d}.{fmt_out}"
        SAVERS[fmt_out](chunk, str(out_path))

    print(f"✅ Split {len(data)} rows into {(len(data) + args.size - 1) // args.size} batches")


def main():
    parser = argparse.ArgumentParser(
        description="Atlas Data Toolkit — Portable Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  datatoolkit convert data.csv -o data.json
  datatoolkit validate messy.csv
  datatoolkit clean dirty.json -o clean.json
  datatoolkit batch large.csv 100 ./chunks/
        """,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert
    p = subparsers.add_parser("convert", help="Convert between formats")
    p.add_argument("input")
    p.add_argument("-o", "--output")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"])
    p.add_argument("--clean", action="store_true", help="Clean data during conversion")
    p.add_argument("--no-dedup", action="store_true")
    p.add_argument("--no-normalize", action="store_true")
    p.set_defaults(func=cmd_convert)

    # validate
    p = subparsers.add_parser("validate", help="Validate data quality")
    p.add_argument("input")
    p.set_defaults(func=cmd_validate)

    # clean
    p = subparsers.add_parser("clean", help="Clean and normalize data")
    p.add_argument("input")
    p.add_argument("-o", "--output")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"])
    p.add_argument("--no-dedup", action="store_true")
    p.add_argument("--no-normalize", action="store_true")
    p.set_defaults(func=cmd_clean)

    # batch
    p = subparsers.add_parser("batch", help="Split into smaller files")
    p.add_argument("input")
    p.add_argument("size", type=int, help="Rows per batch")
    p.add_argument("output_dir")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"])
    p.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
