# Firecrawl E-commerce Scraper 🛒

[![CI](https://github.com/RanuK12/firecrawl-ecom-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/RanuK12/firecrawl-ecom-scraper/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c.svg)](https://github.com/RanuK12/firecrawl-ecom-scraper/network/dependencies)

A professional Python tool designed to extract structured product data from e-commerce websites using the **Firecrawl SDK**. Handles complex web structures and exports clean, structured data directly to CSV or JSON.

## 🚀 Quick Start (2 minutes setup)

Get the scraper running in under 2 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp .env.example .env
# Edit .env and add your Firecrawl API key: FIRECRAWL_API_KEY=your_key_here

# 4. Run the scraper on an e-commerce site
python scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

See the `sample_products.csv` file to see what the output looks like!

## 🚀 Features

- **Robust Scraping**: Powered by [Firecrawl](https://www.firecrawl.dev/) to bypass complex web structures.
- **Smart Field Detection**: Automatically finds product arrays in nested JSON responses.
- **European Price Parsing**: Handles both `.` and `,` decimal separators (e.g., `1.200,50` → `1200.50`).
- **Rich Terminal Output**: Pretty-printed tables and summary panels via [Rich](https://github.com/Textualize/rich) (disable with `--no-rich`).
- **Multiple Output Formats**: CSV and JSON (pretty-printed) export.
- **Resilient**: Retry logic with exponential backoff via `tenacity`.

## 🛠️ Detailed Setup

### Prerequisites
- Python 3.10 or higher
- Firecrawl API key (get one from [Firecrawl](https://www.firecrawl.dev/))

### Installation

```bash
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper
pip install -r requirements.txt
```

### Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Firecrawl API key:
   ```
   FIRECRAWL_API_KEY=your_actual_firecrawl_api_key_here
   ```

3. The `sample_products.csv` file shows what the output looks like when the scraper runs successfully.

## 💻 Usage

### Basic scraping

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY"
```

### Custom output filename (`--output`)

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --output "results.csv"
```

### Choose output format (`--format`)

Export as CSV (default) or JSON:

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --format csv
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --format json
```

### Pretty-print JSON (`--pretty`)

Indent JSON output for readability (only applies with `--format json`):

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --format json --pretty
```

### Limit products (`--limit`)

Cap the number of products saved (0 = no limit, default):

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --limit 50
```

### Quiet mode (`--quiet`)

Suppress INFO messages, only show warnings and errors:

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --quiet
```

### Disable Rich output (`--no-rich`)

Use plain text instead of Rich-formatted tables and panels:

```bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --no-rich
```

### Show version (`--version`)

Print the current version and exit:

```bash
python scraper.py --version
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
