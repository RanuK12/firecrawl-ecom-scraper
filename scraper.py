import csv
import logging
import argparse
from typing import List, Dict, Any
from typing_extensions import TypedDict
from firecrawl import FirecrawlApp

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
    """Return a dict with guaranteed keys: name, price, stock, description."""
    return {
        'name': str(product.get('name', '')),
        'price': str(product.get('price', '')),
        'stock': str(product.get('stock', '')),
        'description': str(product.get('description', '')),
    }

def scrape_ecommerce(url: str, api_key: str, output_file: str = "products_output.csv"):
    try:
        app = FirecrawlApp(api_key=api_key)
        logger.info(f"🚀 Iniciando scraping de: {url}")
        
        # Usamos el formato JSON para obtener datos estructurados
        scrape_result = app.scrape_url(url, params={'formats': ['json']})
        
        if not scrape_result or 'data' not in scrape_result:
            logger.error("❌ Error: No se pudieron obtener datos del sitio.")
            return

        data = scrape_result['data']
        
        # Intentamos extraer campos comunes
        products: List[Dict[str, Any]] = data.get('products', [])
        if not products:
            # Si no hay lista de productos, guardamos el objeto principal
            products = [data]

        fieldnames = ['name', 'price', 'stock', 'description']
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            if products:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for product in products:
                    writer.writerow(extract_product_fields(product))
                logger.info(f"✅ Éxito: Datos guardados en {output_file}")
            else:
                logger.warning("⚠️ No se encontraron productos para exportar.")
                
    except Exception as e:
        logger.error(f"💥 Error inesperado durante el scraping: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firecrawl E-commerce Scraper")
    parser.add_argument("--url", required=True, help="URL de la tienda")
    parser.add_argument("--key", required=True, help="Firecrawl API Key")
    parser.add_argument("--output", default="products_output.csv",
                        help="Nombre del archivo CSV de salida")
    
    args = parser.parse_args()
    scrape_ecommerce(args.url, args.key, args.output)