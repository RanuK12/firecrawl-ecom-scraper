# Firecrawl E-commerce Scraper 🛒

[![CI](https://github.com/RanuK12/firecrawl-ecom-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/RanuK12/firecrawl-ecom-scraper/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c.svg)](https://github.com/RanuK12/firecrawl-ecom-scraper/network/dependencies)

A professional Python tool designed to extract structured product data from e-commerce websites using the **Firecrawl SDK**. Handles complex web structures and exports clean, structured data directly to CSV or JSON.

## 🚀 Features

- **Robust Scraping**: Powered by [Firecrawl](https://www.firecrawl.dev/) to bypass complex web structures.
- **Smart Field Detection**: Automatically finds product arrays in nested JSON responses.
- **European Price Parsing**: Handles both `.` and `,` decimal separators (e.g., `1.200,50` → `1200.50`).
- **Multiple Output Formats**: CSV and JSON (pretty-printed) export.
- **Resilient**: Retry logic with exponential backoff via `tenacity`.

## 🛠️ Setup

```bash
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper
pip install -r requirements.txt
```

Get your API key from [Firecrawl](https://www.firecrawl.dev/).

## 💻 Usage

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY"
```

Custom output filename:

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --output "results.csv"
```

## 🧪 Running Tests

```bash
python -m unittest test_scraper.py -v
```

The test suite covers field extraction, price parsing with European locales, product detection in nested JSON, and output formatting — all without requiring a Firecrawl API key.

## 📁 Output

The scraper produces a CSV file with columns: `name`, `price`, `stock`, `description`. Each product found on the page becomes a row.

## 📄 License

MIT
