import csv
from firecrawl import FirecrawlApp
import argparse

def extract_product_fields(product):
    """Return a dict with guaranteed keys: name, price, stock, description."""
    return {
        'name': product.get('name', ''),
        'price': product.get('price', ''),
        'stock': product.get('stock', ''),
        'description': product.get('description', ''),
    }

def scrape_ecommerce(url, api_key, output_file="products_output.csv"):
    app = FirecrawlApp(api_key=api_key)
    
    print(f"🚀 Iniciando scraping de: {url}")
    
    # Usamos el formato JSON para obtener datos estructurados
    scrape_result = app.scrape_url(url, params={'formats': ['json']})
    
    if not scrape_result or 'data' not in scrape_result:
        print("❌ Error: No se pudieron obtener datos del sitio.")
        return

    data = scrape_result['data']
    
    # Intentamos extraer campos comunes (esto puede variar según el sitio)
    # Pero el objetivo es mostrar el uso del SDK de Firecrawl correctamente
    products = data.get('products', [])
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
            print(f"✅ Éxito: Datos guardados en {output_file}")
        else:
            print("⚠️ No se encontraron productos para exportar.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firecrawl E-commerce Scraper")
    parser.add_argument("--url", required=True, help="URL de la tienda")
    parser.add_argument("--key", required=True, help="Firecrawl API Key")
    parser.add_argument("--output", default="products_output.csv",
                        help="Nombre del archivo CSV de salida")
    
    args = parser.parse_args()
    scrape_ecommerce(args.url, args.key, args.output)
