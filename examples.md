# Firecrawl E-commerce Scraper - Usage Examples

This file provides practical examples to help users understand how to use the scraper effectively.

## Basic Usage

### Example 1: Scraping a Simple E-commerce Site

```bash
# First, copy the environment file and add your API key
cp .env.example .env
# Edit .env and add: FIRECRAWL_API_KEY=your_actual_api_key

# Run the scraper on a sample e-commerce site
python3 scraper.py --url "https://example-ecommerce-store.com" --key "your_firecrawl_api_key"
```

### Example 2: Saving Results to a Custom File

```bash
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --output "my_products.csv"
```

### Example 3: Exporting as JSON

```bash
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --format json
```

### Example 4: Pretty-printed JSON Output

```bash
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --format json --pretty
```

### Example 5: Limiting Results

```bash
# Only save the first 20 products
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --limit 20
```

### Example 6: Quiet Mode

```bash
# Only show warnings and errors
python3 scraper.py --url "https://example-store.com" --key "your_api_key" --quiet
```

## Sample Output

The scraper produces a CSV file with the following columns:

```csv
name,price,stock,description
"Wireless Headphones","99.99","25","High-quality wireless headphones with noise cancellation"
"Smartphone","599.99","15","Latest smartphone with advanced camera system"
"Laptop","1299.99","8","Powerful laptop for professionals and gamers"
"Smart Watch","249.99","32","Feature-rich smartwatch with health tracking"
"Tablet","399.99","12","10-inch tablet perfect for work and entertainment"
```

## Troubleshooting

### Common Error Messages

1. **"Unauthorized: Invalid token"**
   - Solution: Make sure your Firecrawl API key is correct in the `.env` file.

2. **"Failed to scrape"**
   - Solution: The website may be blocking requests or may not be compatible with Firecrawl.

3. **"No products found"**
   - Solution: The website may not have a product structure that the scraper can detect.

### Getting a Firecrawl API Key

1. Visit [https://www.firecrawl.dev/](https://www.firecrawl.dev/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your `.env` file: `FIRECRAWL_API_KEY=your_key_here`

## Next Steps

1. Try the scraper on a real e-commerce site
2. Modify the output format for your specific needs
3. Integrate the scraper into your data pipeline
4. Extend the functionality for custom data extraction