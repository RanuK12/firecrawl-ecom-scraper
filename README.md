# firecrawl‑ecom‑scraper

A quick scraper for e‑commerce sites using **Firecrawl**.

## Quick start (≈2 min)

```bash
# 1️⃣ Clone & enter repo
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git && cd firecrawl-ecom-scraper

# 2️⃣ Install deps (Python 3.10+)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3️⃣ Prepare env vars
cp .env.example .env   # edit with your Firecrawl API key and target URL

# 4️⃣ Run scraper
python -m scraper   # produces output.csv
```

The command creates `output.csv` with columns `id,name,price,url`.

## Sample output

```csv
id,name,price,url
1,Wireless Headphones,89.99,https://example-store.com/wireless-headphones
2,Smart Watch,149.50,https://example-store.com/smart-watch
```

---

*If you see errors, ensure your API key is valid and the target site allows crawling.*