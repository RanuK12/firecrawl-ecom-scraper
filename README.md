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

## Demo mode (no API key needed)

```bash
python -m scraper --demo --output demo_output.csv
```

This generates a sample CSV with mock data so you can verify the script works before obtaining a Firecrawl API key.

## Output format

The scraper creates `output.csv` (or the file you specify) with columns:

- `name` – product name
- `price` – price as a number
- `stock` – available stock (integer)
- `description` – short product description

## Sample output

```csv
name,price,stock,description
Sample Shirt,19.99,100,A comfortable cotton shirt
Sample Shoes,49.99,50,Durable running shoes
```

---

*If you see errors, ensure your API key is valid and the target site allows crawling.*