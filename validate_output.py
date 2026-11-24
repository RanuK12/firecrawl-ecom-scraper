#!/usr/bin/env python3
"""Valida que un CSV de salida tenga las columnas esperadas del scraper.

Uso:
    python validate_output.py [archivo.csv]
"""

import csv
import sys
from pathlib import Path

EXPECTED_COLUMNS = ["name", "price", "stock", "description"]


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("demo_output.csv")
    if not csv_path.exists():
        print(f"❌ No se encontró el archivo: {csv_path}")
        return 1

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

    if header is None:
        print("❌ El CSV está vacío.")
        return 1

    missing = [c for c in EXPECTED_COLUMNS if c not in header]
    if missing:
        print(f"❌ Columnas faltantes: {missing}")
        print(f"   Columnas encontradas: {header}")
        return 1

    print(f"✅ {csv_path} es válido (columnas: {header})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
