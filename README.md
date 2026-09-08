# Firecrawl E-commerce Scraper

A powerful e-commerce scraper built with Firecrawl that extracts product information from online stores and exports it to CSV or JSON format.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

Get the scraper running in under 2 minutes!

### Step 1: Clone & Setup

```bash
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add: FIRECRAWL_API_KEY=your_actual_firecrawl_api_key_here
```

### Step 2: Run the Scraper

```bash
python3 scraper.py --url "https://example-ecommerce-store.com"
```

### Step 3: Check the Results

The scraper creates a CSV file with product data (first 5 rows shown):

```csv
url,title,price,currency,availability,description,images,sku,category,brand,rating,review_count
https://example-store.com/product/1,"Wireless Headphones Pro",149.99,USD,In Stock,"Premium wireless headphones with active noise cancellation and 30-hour battery life",https://example-store.com/images/headphones-pro.jpg,WH-PRO-001,Electronics,SoundMax,4.5,1234
https://example-store.com/product/2,"Smart Watch Series 5",299.00,USD,In Stock,"Latest smartwatch with health monitoring, GPS, and cellular connectivity",https://example-store.com/images/smartwatch-5.jpg,SW-5-002,Wearables,TechWear,4.7,892
https://example-store.com/product/3,"USB-C Hub 7-in-1",49.99,USD,In Stock,"Multi-port adapter with HDMI, USB-A, USB-C, SD card reader, and Ethernet",https://example-store.com/images/usb-hub.jpg,USB-HUB-7,Accessories,ConnectPro,4.3,567
https://example-store.com/product/4,"Mechanical Keyboard RGB",129.99,USD,Out of Stock,"RGB mechanical keyboard with hot-swappable switches and PBT keycaps",https://example-store.com/images/kb-rgb.jpg,MK-RGB-003,Electronics,KeyMaster,4.6,2103
https://example-store.com/product/5,"Portable SSD 2TB",189.99,USD,In Stock,"High-speed portable SSD with USB 3.2 Gen 2x2 and hardware encryption",https://example-store.com/images/ssd-2tb.jpg,SSD-2TB-004,Storage,DataVault,4.8,1456
```

Full sample: [`examples/sample_output.csv`](examples/sample_output.csv) (15 rows)

## 📦 Install as CLI

```bash
pip install .
firecrawl-scraper --url "https://example-store.com"
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
├── examples/
│   └── sample_output.csv  # Sample output file (15 rows)
└── README.md           # This file
```

## 🚀 Usage Examples

### Basic Usage

```bash
python3 scraper.py --url "https://example-ecommerce-store.com"
```

### Save to Custom File

```bash
python3 scraper.py --url "https://example-store.com" --output "my_products.csv"
```

### Export as JSON

```bash
python3 scraper.py --url "https://example-store.com" --format json
```

### Limit Results

```bash
python3 scraper.py --url "https://example-store.com" --limit 20
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