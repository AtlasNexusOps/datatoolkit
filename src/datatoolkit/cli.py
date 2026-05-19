#!/usr/bin/env python3
"""Data Toolkit — Convert, validate, clean. JSON ↔ CSV ↔ YAML ↔ XML."""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import xmltodict
    HAS_XML = True
except ImportError:
    HAS_XML = False


def load_json(path: str) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def load_csv(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_yaml(path: str) -> list[dict]:
    with open(path) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else [data]


def load_xml(path: str) -> list[dict]:
    with open(path) as f:
        data = xmltodict.parse(f.read())
    root = list(data.values())[0]
    items = root if isinstance(root, list) else [root]
    return items


LOADERS = {
    "json": load_json,
    "csv": load_csv,
    "yaml": load_yaml,
    "yml": load_yaml,
    "xml": load_xml,
}


def save_json(data: list[dict], path: str):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(data: list[dict], path: str):
    if not data:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_yaml(data: list[dict], path: str):
    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def save_xml(data: list[dict], path: str, root_name: str = "root", item_name: str = "item"):
    wrapped = {root_name: {item_name: data}} if data else {root_name: None}
    with open(path, "w") as f:
        xmltodict.unparse(wrapped, f, pretty=True)


SAVERS = {
    "json": save_json,
    "csv": save_csv,
    "yaml": save_yaml,
    "yml": save_yaml,
    "xml": save_xml,
}


def detect_format(path: str) -> str:
    ext = Path(path).suffix.lower().lstrip(".")
    if ext in LOADERS:
        return ext
    raise ValueError(f"Format non supporté : .{ext}")


def clean_data(data: list[dict], dedup: bool = True, normalize: bool = True) -> list[dict]:
    if normalize:
        for row in data:
            for k, v in row.items():
                if v is None:
                    row[k] = ""
                elif isinstance(v, str):
                    v = v.strip()
                    try:
                        v_int = int(v)
                        row[k] = v_int
                        continue
                    except (ValueError, TypeError):
                        pass
                    try:
                        v_float = float(v.replace(",", "."))
                        row[k] = v_float
                        continue
                    except (ValueError, TypeError):
                        pass
                    row[k] = v
    if dedup:
        seen = set()
        unique = []
        for row in data:
            key = json.dumps(row, sort_keys=True, default=str)
            if key not in seen:
                seen.add(key)
                unique.append(row)
        data = unique
    return data


def validate_data(data: list[dict]) -> dict:
    report = {
        "total_rows": len(data),
        "total_columns": len(data[0]) if data else 0,
        "columns": list(data[0].keys()) if data else [],
        "null_counts": {},
        "empty_strings": {},
    }
    for col in report["columns"]:
        nulls = sum(1 for r in data if r.get(col) is None)
        empties = sum(1 for r in data if r.get(col) == "")
        report["null_counts"][col] = nulls
        report["empty_strings"][col] = empties
    return report


def cmd_convert(args):
    in_fmt = detect_format(args.input)
    data = LOADERS[in_fmt](args.input)
    if args.clean:
        data = clean_data(data, dedup=not args.no_dedup, normalize=not args.no_normalize)
    out_fmt = args.output_format or (detect_format(args.output) if args.output else "json")
    if args.output:
        SAVERS[out_fmt](data, args.output)
        print(f"✓ {len(data)} lignes → {args.output}")
    else:
        SAVERS[out_fmt](data, "-")


def cmd_validate(args):
    in_fmt = detect_format(args.input)
    data = LOADERS[in_fmt](args.input)
    report = validate_data(data)
    print(json.dumps(report, indent=2))


def cmd_clean(args):
    in_fmt = detect_format(args.input)
    data = LOADERS[in_fmt](args.input)
    before = len(data)
    data = clean_data(data, dedup=not args.no_dedup, normalize=not args.no_normalize)
    after = len(data)
    out_fmt = args.output_format or in_fmt
    if args.output:
        SAVERS[out_fmt](data, args.output)
    else:
        SAVERS[out_fmt](data, "-")
    if before != after:
        print(f"✓ {before} → {after} lignes ({before - after} doublons supprimés)", file=sys.stderr)


def cmd_batch(args):
    in_fmt = detect_format(args.input)
    data = LOADERS[in_fmt](args.input)
    if not data:
        print("Aucune donnée à splitter.", file=sys.stderr)
        return
    size = args.size
    total = len(data)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_fmt = args.output_format or in_fmt
    for i in range(0, total, size):
        chunk = data[i : i + size]
        out_path = out_dir / f"chunk_{i // size + 1:03d}.{out_fmt}"
        SAVERS[out_fmt](chunk, str(out_path))
        print(f"✓ {out_path} ({len(chunk)} lignes)")
    print(f"{total} lignes → {(total + size - 1) // size} fichiers")


def main():
    parser = argparse.ArgumentParser(
        description="Data Toolkit — Convert, validate, clean. JSON ↔ CSV ↔ YAML ↔ XML.",
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("convert", help="Convertir entre formats")
    p.add_argument("input", help="Fichier source")
    p.add_argument("-o", "--output", help="Fichier de sortie (stdout si absent)")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"], help="Format de sortie")
    p.add_argument("--clean", action="store_true", help="Nettoyer avant conversion")
    p.add_argument("--no-dedup", action="store_true", help="Désactiver déduplication")
    p.add_argument("--no-normalize", action="store_true", help="Désactiver normalisation")
    p.set_defaults(func=cmd_convert)

    p = sub.add_parser("validate", help="Valider un fichier")
    p.add_argument("input", help="Fichier à valider")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("clean", help="Nettoyer un fichier")
    p.add_argument("input", help="Fichier source")
    p.add_argument("-o", "--output", help="Fichier de sortie")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"], help="Format de sortie")
    p.add_argument("--no-dedup", action="store_true")
    p.add_argument("--no-normalize", action="store_true")
    p.set_defaults(func=cmd_clean)

    p = sub.add_parser("batch", help="Splitter en lots")
    p.add_argument("input", help="Fichier source")
    p.add_argument("size", type=int, help="Taille des lots (lignes)")
    p.add_argument("output_dir", help="Dossier de sortie")
    p.add_argument("-f", "--output-format", choices=["json", "csv", "yaml", "xml"], help="Format de sortie")
    p.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
