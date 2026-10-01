import os, csv
from firecrawl import FirecrawlApp

# Cargar .env si existe
from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.getenv('FIRECRAWL_API_KEY')
url = os.getenv('TARGET_URL', 'https://example.com')
output = os.getenv('OUTPUT_CSV', 'sample_output.csv')

app = FirecrawlApp(api_key=api_key)

# Simple scrape: get product titles & prices (adjust selector as needed)
result = app.scrape(url, mode='scrape', params={'extract': {'selector': '.product', 'attributes': ['title','price']}})

with open(output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title','price'])
    for item in result.get('data', []):
        writer.writerow([item.get('title'), item.get('price')])

print(f'✅ CSV generado: {output}')