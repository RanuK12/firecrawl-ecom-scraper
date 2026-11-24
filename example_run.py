#!/usr/bin/env python3
"""Ejemplo de uso del Firecrawl E-commerce Scraper en modo demo.

Corre sin API key y genera un CSV de salida en ~2 minutos.
Uso:
    python example_run.py
"""

import subprocess
import sys
from pathlib import Path

SCRAPER = Path(__file__).with_name("scraper.py")
OUTPUT_CSV = Path(__file__).with_name("demo_output.csv")


def main() -> int:
    print("🚀 Ejecutando scraper en modo demo (sin API key)...")
    cmd = [
        sys.executable, str(SCRAPER),
        "--demo",
        "--output", str(OUTPUT_CSV),
        "--no-rich",
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("❌ El scraper falló.")
        return result.returncode

    print(f"✅ Listo: {OUTPUT_CSV}")
    print("\n📋 Primeras líneas del CSV:")
    print(OUTPUT_CSV.read_text(encoding="utf-8")[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
