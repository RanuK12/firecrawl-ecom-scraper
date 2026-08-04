# Firecrawl E-commerce Scraper

A powerful e-commerce scraper built with Firecrawl that extracts product information from online stores and exports it to CSV or JSON format.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

Get the scraper running in under 2 minutes!

### Step 1: Clone & Setup

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

### Step 2: Run the Scraper

```bash
# Run on an e-commerce site
python3 scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

### Step 3: Check the Results

The scraper creates a CSV file with product data:
- `name`: Product name
- `price`: Price (cleaned of currency symbols)
- `stock`: Stock information
- `description`: Product description

## 📋 Sample Output

See `sample_products.csv` for an example of the output format:

```csv
name,price,stock,description
"Wireless Headphones","99.99","25","High-quality wireless headphones with noise cancellation"
"Smartphone","599.99","15","Latest smartphone with advanced camera system"
"Laptop","1299.99","8","Powerful laptop for professionals and gamers"
```

## 🎯 Features

- ✅ **Fast Setup**: Running in under 2 minutes
- ✅ **Multiple Output Formats**: CSV or JSON
- ✅ **Clean Data**: Automatically removes currency symbols and handles European decimal commas
- ✅ **Error Handling**: Robust error handling with retry logic
- ✅ **Progress Tracking**: Beautiful terminal progress (with Rich)
- ✅ **Flexible Output**: Custom output filenames and formats

## 📁 Project Structure

```
firecrawl-ecom-scraper/
├── scraper.py          # Main scraper script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── sample_products.csv # Sample output file
└── README.md           # This file
```

## 🚀 Usage Examples

### Basic Usage

```bash
# Run on a simple e-commerce site
python3 scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

### Save to Custom File

```bash
# Save results to a specific filename
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --output "my_products.csv"
```

### Export as JSON

```bash
# Export results in JSON format
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --format json
```

### Limit Results

```bash
# Only save the first 20 products
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --limit 20
```

## 🔧 Requirements

- Python 3.7+
- Firecrawl API key (get one at [https://www.firecrawl.dev/](https://www.firecrawl.dev/))

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.