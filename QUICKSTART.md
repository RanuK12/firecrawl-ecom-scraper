# Quick Start Guide - Firecrawl E-commerce Scraper

Get the scraper running in under 2 minutes!

## 🚀 Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper

# Install dependencies
pip install -r requirements.txt

# Set up your API key (optional for demo mode!)
cp .env.example .env
# Edit .env and add: FIRECRAWL_API_KEY=your_actual_firecrawl_api_key_here
# OR leave it empty and run in DEMO MODE!
```

### 💡 Optional: Install as CLI tool

```bash
pip install .
# Then run from anywhere:
firecrawl-scraper --url "https://example-store.com" --key "your_api_key"
```

## 🚀 Step 2: Run the Scraper

### 🎯 MODO DEMO (¡Sin API Key!)
```bash
# Opción 1: Script de ejemplo (recomendado)
python3 example_run.py

# Opción 2: Directo con flag --demo
python3 scraper.py --url https://demo.example.com --output demo_output.csv --demo
```
**¡Esto genera un CSV real en 2 minutos sin registrarte en Firecrawl!**

### 🚀 Modo Producción (con API Key)
```bash
# Run on an e-commerce site
python3 scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

## 📁 Check the Results

The scraper creates a CSV file with product data:
- `product_id`: Unique product identifier
- `title`: Product name
- `price`: Price (cleaned of currency symbols)
- `stock`: Stock information
- `url`: Product URL

## 📋 Sample Output

```csv
product_id,title,price,stock,url
1,Sample Shirt,19.99,100,https://webscraper.io/test-sites/e-commerce/static/products/1
2,Sample Shoes,49.99,50,https://webscraper.io/test-sites/e-commerce/static/products/2
```

## 🎯 Next Steps

1. Get your Firecrawl API key at [https://www.firecrawl.dev/](https://www.firecrawl.dev/)
2. Try on your target e-commerce site
3. Check `examples.md` for more usage examples
4. See `README.md` for advanced options

That's it! You're ready to scrape e-commerce data.