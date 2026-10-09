import os
from scraper import scrape

# Cargar .env si existe (fallback a variables de entorno)
from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.getenv('FIRECRAWL_API_KEY')
url = os.getenv('TARGET_URL')
output = os.getenv('OUTPUT_CSV', 'sample_output.csv')

if not api_key or not url:
    raise SystemExit('Configura FIRECRAWL_API_KEY y TARGET_URL en .env o variables de entorno')

# Ejecutar scraper
scrape(api_key, url, output)
print(f'✅ CSV generado: {output}')