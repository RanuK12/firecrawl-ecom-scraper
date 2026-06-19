# Firecrawl E-commerce Scraper 🛒

A professional Python tool designed to extract structured product data from e-commerce websites using the **Firecrawl SDK**. This scraper handles complex web structures and exports clean, structured data directly to CSV.

## 🚀 Features
- **Robust Scraping**: Powered by [Firecrawl](https://www.firecrawl.dev/) to bypass complex web structures.
- **Structured Data**: Automatically extracts JSON data and flattens it for easy use.
- **CSV Export**: Direct export to CSV for immediate integration with spreadsheets or databases.

## 🛠️ Setup

1. **Clone the repository**:
   \`\`\`bash
   git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
   cd firecrawl-ecom-scraper
   \`\`\`

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Get your API Key** from [Firecrawl](https://www.firecrawl.dev/).

## 💻 Usage

Run the scraper by providing the target URL and your API key:

\`\`\`bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY"
\`\`\`

Optional: specify a custom output filename:

\`\`\`bash
python scraper.py --url "https://example-ecommerce-store.com" --key "YOUR_API_KEY" --output "results.csv"
\`\`\`

## 📄 License
MIT
