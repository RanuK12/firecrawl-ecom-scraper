# firecrawl‑ecom‑scraper

Scrape product catalogs from any e‑commerce site using **Firecrawl**.

## Quick start (under 2 min)

```bash
# 1️⃣ Clone & enter repo
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git && cd firecrawl-ecom-scraper

# 2️⃣ Install deps
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 3️⃣ Copy env template & edit
cp .env.example .env   # edit .env with your Firecrawl API key & target URL

# 4️⃣ Run scraper
python scraper.py
```

The script writes a CSV (`output.csv` by default) with columns `title,price,url,image`.

## Sample output

```csv
title,price,url,image
"Sample Product",19.99,https://example.com/p/1,https://example.com/img/1.jpg
```
---