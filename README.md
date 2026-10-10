# firecrawl-ecom-scraper

A quick scraper for e-commerce sites using **Firecrawl**.

## Quick Start (2 minutes)

1. **Get a Firecrawl API key (optional for demo)**
   Sign up at [https://firecrawl.dev](https://firecrawl.dev) for a free API key if you want to scrape real sites.

2. **Set up environment (optional)**
   Copy the example env file if you plan to use a real API key:
   ```bash
   cp .env.example .env
   # Edit .env and replace 'your_api_key_here' with your actual key
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper in demo mode (no API key needed)**
   ```bash
   python scraper.py --demo --output sample_output.csv
   ```

5. **Check the output**
   Open `sample_output.csv` to see the extracted product data. A sample output file is already included in the repo for reference.

## Demo mode

To test the scraper without needing an API key:
   ```bash
   python3 -m scraper --demo --output demo_output.csv
   ```

## Output format

The scraper generates a CSV file with the following columns:
- `product_id` – Identifier of the product
- `title` – Product name
- `price` – Product price
- `stock` – Available stock
- `url` – Link to the product

## Sample output

```csv
product_id,title,price,stock,url
1,Sample Shirt,19.99,100,https://webscraper.io/test-sites/e-commerce/static/products/1
2,Sample Shoes,49.99,50,https://webscraper.io/test-sites/e-commerce/static/products/2
```