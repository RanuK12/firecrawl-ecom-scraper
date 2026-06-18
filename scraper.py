import csv
import logging
import argparse
import sys
import re
import requests
from typing import List, Dict, Any
from typing_extensions import TypedDict
from firecrawl import FirecrawlApp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, retry_if_exception

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Product(TypedDict):
    name: str
    price: str
    stock: str
    description: str

def extract_product_fields(product: Dict[str, Any]) -> Product:
    """Return a dict with guaranteed keys: name, price, stock, description.
    Strips whitespace from all fields and removes currency symbols from price.
    Handles European decimal commas (e.g., 1.200,50 → 1200.50).
    """
    name = str(product.get('name', '')).strip()
    price_raw = str(product.get('price', '')).strip()
    # Remove common currency symbols and any non-digit, non-dot, non-comma, non-minus characters
    price_clean = re.sub(r'[^\d.,\-]', '', price_raw)

    # Heuristic to distinguish decimal commas from thousands separators
    if ',' in price_clean:
        parts = price_clean.split(',')
        # Only consider the first comma
        before_comma = parts[0]
        after_comma = parts[1] if len(parts) >= 2 else ''
        # If the part after the comma has 1 or 2 digits (and is not empty),
        # treat the comma as a decimal separator (European style).
        if 1 <= len(after_comma) <= 2:
            # Remove all dots (thousands separators) from the part before the comma
            before_comma = before_comma.replace('.', '')
            price_clean = before_comma + '.' + after_comma
        else:
            # Comma is a thousands separator; remove it
            price_clean = price_clean.replace(',', '')
    else:
        # No comma present; decide whether dots are thousands separators or decimal
        dot_count = price_clean.count('.')
        if dot_count == 1:
            # Single dot: check if the part after the dot has at most 2 digits
            parts = price_clean.split('.')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Likely a decimal dot (US style) – keep as is
                pass
            else:
                # Thousands separator – remove the dot
                price_clean = price_clean.replace('.', '')
        elif dot_count > 1:
            # Multiple dots: all are thousands separators – remove them
            price_clean = price_clean.replace('.', '')
        # dot_count == 0: nothing to do

    stock = str(product.get('stock', '')).strip()
    description = str(product.get('description', '')).strip()
    return {
        'name': name,
        'price': price_clean,
        'stock': stock,
        'description': description,
    }

def _find_products(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Try multiple common keys to locate a list of product dicts."""
    candidates = [
        data.get('products', []),
        data.get('items', []),
        data.get('results', []),
        data.get('data', {}).get('products', []),
        data.get('data', {}).get('items', []),
        data.get('data', {}).get('results', []),
    ]
    for candidate in candidates:
        if isinstance(candidate, list) and len(candidate) > 0:
            return candidate
    return []

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=(retry_if_exception_type(requests.exceptions.RequestException) |
           retry_if_exception(lambda e: isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429))
)
def _scrape_with_retry(app, url):
    return app.scrape_url(url, params={'formats': ['json']})

def scrape_ecommerce(url: str, api_key: str, output_file: str = "products_output.csv") -> bool:
    try:
        app = FirecrawlApp(api_key=api_key)
        logger.info(f"🚀 Iniciando scraping de: {url}")
        
        # Usamos el formato JSON para obtener datos estructurados
        try:
            scrape_result = _scrape_with_retry(app, url)
        except Exception as conn_err:
            logger.error(f"❌ Error de conexión con FirecrawlApp: {conn_err}")
            return False
        
        if not scrape_result or 'data' not in scrape_result:
            logger.error("❌ Error: No se pudieron obtener datos del sitio.")
            return False

        data = scrape_result['data']
        
        # Intentamos extraer campos comunes
        products: List[Dict[str, Any]] = _find_products(data)
        if not products:
            logger.warning("⚠️ No se encontraron productos en los datos obtenidos. No se guardará ningún archivo.")
            return False

        fieldnames = ['name', 'price', 'stock', 'description']
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                if not isinstance(product, dict):
                    logger.warning(f"⚠️ Elemento no es un diccionario, se omite: {product}")
                    continue
                writer.writerow(extract_product_fields(product))
            logger.info(f"✅ Éxito: Datos guardados en {output_file}")
        return True
                
    except Exception as e:
        logger.error(f"💥 Error inesperado durante el scraping: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firecrawl E-commerce Scraper")
    parser.add_argument("--url", required=True, help="URL de la tienda")
    parser.add_argument("--key", required=True, help="Firecrawl API Key")
    parser.add_argument("--output", default="products_output.csv",
                        help="Nombre del archivo CSV de salida")
    
    args = parser.parse_args()
    success = scrape_ecommerce(args.url, args.key, args.output)
    if not success:
        sys.exit(1)
