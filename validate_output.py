"""Validador de archivo CSV de salida del Firecrawl E-commerce Scraper.

Comprueba que el CSV tenga exactamente las columnas esperadas
(name, price, stock, description), sin columnas inexistentes (p. ej. product_id,
title, url), sin celdas vacías y con price como número válido.

Uso:
    python3 validate_output.py <archivo.csv>
"""
import csv
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

EXPECTED_COLUMNS = ["name", "price", "stock", "description"]
PRICE_RE = re.compile(r"^\d+(\.\d+)?$")


def validate(csv_path: Path) -> bool:
    if not csv_path.exists():
        logger.error("El archivo no existe: %s", csv_path)
        return False

    errors = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        # 1) Columnas esperadas y sin columnas de más / de menos
        if set(fieldnames) != set(EXPECTED_COLUMNS):
            extra = set(fieldnames) - set(EXPECTED_COLUMNS)
            missing = set(EXPECTED_COLUMNS) - set(fieldnames)
            if extra:
                errors.append(f"Columnas inexistentes no esperadas: {sorted(extra)}")
            if missing:
                errors.append(f"Columnas faltantes: {sorted(missing)}")

        # 2) Filas: sin celdas vacías y price válido
        for i, row in enumerate(reader, start=2):
            for col in EXPECTED_COLUMNS:
                val = (row.get(col) or "").strip()
                if val == "":
                    errors.append(f"Fila {i}: celda vacía en '{col}'")
            price = (row.get("price") or "").strip()
            if price and not PRICE_RE.match(price):
                errors.append(f"Fila {i}: price inválido '{price}' (esperado número decimal)")

    if errors:
        logger.error("❌ Validación falló (%d error(es)):", len(errors))
        for err in errors:
            logger.error("  - %s", err)
        return False

    logger.info("✅ CSV válido: %s", csv_path)
    return True


def main() -> int:
    if len(sys.argv) != 2:
        logger.error("Uso: python3 validate_output.py <archivo.csv>")
        return 1
    ok = validate(Path(sys.argv[1]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
