# Firecrawl E-commerce Scraper 🛒

A professional Python tool designed to extract structured product data from e-commerce websites using the **Firecrawl SDK**. This scraper handles complex web structures and exports clean, structured data directly to CSV.

## 🚀 Features
- **Robust Scraping**: Powered by [Firecrawl](https://www.firecrawl.dev/) to bypass complex web structures.
- **Structured Data**: Automatically extracts JSON data and flattens it for easy use.
- **CSV Export**: Direct export to CSV for immediate integration with spreadsheets or databases.
- **Secure Config**: Supports environment variables for safe API key management.

## 🛠️ Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
   cd firecrawl-ecom-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file based on the provided example:
   ```bash
   cp .env.example .env
   ```
   *Replace `your_api_key_here` with your actual Firecrawl API key.*

## 💻 Usage

Run the scraper by providing the target URL:

```bash
python scraper.py --url "https://example-ecommerce-store.com"
```

The script will automatically detect your API key from the `.env` file.

## 📄 License
MIT
