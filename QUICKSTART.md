# Quick Start Guide - Firecrawl E-commerce Scraper

Get the scraper running in under 2 minutes!

## 🚀 Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add: FIRECRAWL_API_KEY=your_actual_firecrawl_api_key_here
```

### 💡 Optional: Install as CLI tool

```bash
pip install .
# Then run from anywhere:
firecrawl-scraper --url "https://example-store.com" --key "your_api_key"
```

## 🚀 Step 2: Run the Scraper

```bash
# Run on an e-commerce site
python3 scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

## 📁 Check the Results

The scraper creates a CSV file with product data:
- `name`: Product name
- `price`: Price (cleaned of currency symbols)
- `stock`: Stock information
- `description`: Product description

## 📋 Sample Output

```csv
name,price,stock,description
"Wireless Headphones","99.99","25","High-quality wireless headphones with noise cancellation"
"Smartphone","599.99","15","Latest smartphone with advanced camera system"
"Laptop","1299.99","8","Powerful laptop for professionals and gamers"
```

## 🎯 Next Steps

1. Get your Firecrawl API key at [https://www.firecrawl.dev/](https://www.firecrawl.dev/)
2. Try on your target e-commerce site
3. Check `examples.md` for more usage examples
4. See `README.md` for advanced options

That's it! You're ready to scrape e-commerce data.