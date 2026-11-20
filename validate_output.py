"""Valida que un CSV de salida del scraper cumpla el esquema esperado.

Uso:
    python validate_output.py output.csv

Devuelve código de salida 0 si el CSV es válido, 1 si hay errores.
"""

import argparse
import csv
import logging
import re
import sys
from pathlib import Path

EXPECTED_COLUMNS = ["name", "price", "stock", "description"]
log = logging.getLogger("validate_output")


def parse_price(raw: str) -> float | None:
    """Convierte un precio a float.

    Acepta formato europeo (puntos de miles, coma decimal) y formato
    estadounidense (coma de miles, punto decimal).
    Devuelve None si no se puede parsear.
    """
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    # Quitar símbolos de moneda y espacios
    s = re.sub(r"[€$£¥\s]", "", s)
    if not s:
        return None
    # Detectar el separador decimal: es el ÚLTIMO de , o .
    last_comma = s.rfind(",")
    last_dot = s.rfind(".")
    if last_comma == -1 and last_dot == -1:
        try:
            return float(s)
        except ValueError:
            return None
    decimal_sep = "," if last_comma > last_dot else "."
    thousands_sep = "." if decimal_sep == "," else ","
    # Quitar separadores de miles y normalizar decimal a punto
    s = s.replace(thousands_sep, "").replace(decimal_sep, ".")
    try:
        return float(s)
    except ValueError:
        return None


def validate_csv(path: str) -> list[str]:
    """Valida el CSV. Devuelve lista de mensajes de error (vacía si es válido)."""
    errors: list[str] = []
    p = Path(path)

    if not p.exists():
        return [f"Archivo no encontrado: {path}"]

    try:
        with p.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return ["El CSV está vacío o no tiene encabezados."]
            missing = [c for c in EXPECTED_COLUMNS if c not in reader.fieldnames]
            if missing:
                errors.append(f"Columnas faltantes: {', '.join(missing)}")

            for i, row in enumerate(reader, start=2):  # fila 1 = encabezado
                row_errors = []
                for col in EXPECTED_COLUMNS:
                    if col not in reader.fieldnames:
                        continue
                    val = (row.get(col) or "").strip()
                    if val == "":
                        row_errors.append(f"columna '{col}' vacía")
                    if col == "price":
                        if parse_price(val) is None:
                            row_errors.append(f"precio inválido: '{val}'")
                    if col == "stock":
                        try:
                            int(val)
                        except (ValueError, TypeError):
                            row_errors.append(f"stock no es entero: '{val}'")
                if row_errors:
                    errors.append(f"Fila {i}: " + "; ".join(row_errors))
    except (UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"Error leyendo el CSV: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un CSV de salida del scraper de e-commerce."
    )
    parser.add_argument("csv", help="Ruta al archivo CSV a validar")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Mostrar detalle de validación"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    errors = validate_csv(args.csv)
    if errors:
        print(f"❌ CSV inválido ({len(errors)} error(es)):")
        for err in errors:
            print(f"   - {err}")
        return 1

    print(f"✅ CSV válido: {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
