"""
Atlas Data Toolkit — CLI for converting, validating, cleaning and batching operational data files.

Convert between JSON, CSV, YAML, and XML. Validate data quality. Clean and normalize.
"""

from datatoolkit.cli import (
    load_json,
    load_csv,
    load_yaml,
    load_xml,
    save_json,
    save_csv,
    save_yaml,
    save_xml,
    detect_format,
    clean_data,
    validate_data,
    main,
)

__version__ = "0.1.0"
__all__ = [
    "load_json", "load_csv", "load_yaml", "load_xml",
    "save_json", "save_csv", "save_yaml", "save_xml",
    "detect_format", "clean_data", "validate_data", "main",
]
