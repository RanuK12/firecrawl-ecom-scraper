"""Ejemplo de uso del Firecrawl E-commerce Scraper en modo demo.

Este script NO requiere API key de Firecrawl: ejecuta scraper.py en modo demo
con datos de prueba y genera un CSV de salida listo para inspeccionar.
Sirve para que un comprador vea el resultado antes de instalar/configurar nada.

Uso:
    python3 example_run.py
"""
import csv
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SCRAPER = Path(__file__).resolve().parent / "scraper.py"
OUTPUT_CSV = Path(__file__).resolve().parent / "example_output.csv"


def main() -> int:
    if not SCRAPER.exists():
        logger.error("No se encontró scraper.py junto a este archivo.")
        return 1

    logger.info("Ejecutando scraper en modo demo (sin API key)...")
    result = subprocess.run(
        [sys.executable, str(SCRAPER), "--demo", "--output", str(OUTPUT_CSV)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("scraper.py falló:")
        logger.error(result.stderr)
        return 1

    logger.info(result.stdout.strip())

    if not OUTPUT_CSV.exists():
        logger.error("No se generó el archivo de salida.")
        return 1

    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    logger.info("Columnas del CSV: %s", ", ".join(reader.fieldnames or []))
    logger.info("Productos generados: %d", len(rows))
    for row in rows:
        logger.info("  - %(name)s | %(price)s | stock=%(stock)s | %(description)s", row)

    logger.info("✅ Listo: %s", OUTPUT_CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())
