import os, csv
from dotenv import load_dotenv
from scraper import scrape_ecommerce

def main():
    load_dotenv()  # take environment variables from .env
    api_key = os.getenv('FIRECRAWL_API_KEY')
    url = os.getenv('TARGET_URL')
    out = os.getenv('OUTPUT_CSV', 'sample_output.csv')
    if not api_key or not url:
        raise SystemExit('Set FIRECRAWL_API_KEY and TARGET_URL in .env')
    data = scrape_ecommerce(url, api_key, out, fmt='csv', pretty=False)
    # write first 5 rows to CSV for demo
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=data[0].keys())
        w.writeheader()
        for row in data[:5]:
            w.writerow(row)
    print(f'Demo CSV written to {out}')

if __name__ == '__main__':
    main()