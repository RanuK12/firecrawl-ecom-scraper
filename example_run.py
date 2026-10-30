import os
from scraper import scrape_ecommerce, main as scraper_main

# Cargar .env si existe (fallback a variables de entorno)
from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.getenv('FIRECRAWL_API_KEY')
url = os.getenv('TARGET_URL')
output = os.getenv('OUTPUT_CSV', 'sample_output.csv')

# MODO DEMO: si no hay API key o es 'demo', usa datos de muestra
if not api_key or api_key == 'demo':
    print('🎯 MODO DEMO: Generando CSV con datos de muestra (sin API key)...')
    import sys
    sys.argv = ['scraper', '--url', 'https://demo.example.com', '--output', output, '--demo']
    scraper_main()
    print(f'✅ CSV generado (demo): {output}')
else:
    # Modo normal con Firecrawl API
    print(f'🚀 Modo producción: Scrapeando {url}...')
    scrape_ecommerce(api_key, url, output)
    print(f'✅ CSV generado: {output}')