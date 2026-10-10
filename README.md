# firecrawl-ecom-scraper

A quick scraper for e-commerce sites using **Firecrawl**.

## Quick Start (2 minutes)

1. **Get a Firecrawl API key**  
   Sign up at [https://firecrawl.dev](https://firecrawl.dev) for a free API key.

2. **Set up environment**  
   Copy the example env file and add your key:
   ```bash
   cp .env.example .env
   # Edit .env and replace 'your_api_key_here' with your actual key
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper on the sample e-commerce site (as defined in .env.example)**  
   ```bash
   python scraper.py --output sample_output.csv
   ```
   (This uses the TARGET_URL from .env.example: https://webscraper.io/test-sites/e-commerce/static)

5. **Check the output**  
   Open `sample_output.csv` to see the extracted product data. A sample output file is already included in the repo for reference.


## Demo mode

Para probar el scraper sin necesidad de una clave API:
   ```bash
   python3 -m scraper --demo --output demo_output.csv
   ```

## Output format

El scraper genera un archivo CSV con las siguientes columnas:
- `product_id` – Identificador del producto
- `title` – Nombre del producto
- `price` – Precio del producto
- `stock` – Stock disponible
- `url` – Enlace al producto

## Sample output

```csv
product_id,title,price,stock,url
1,Sample Shirt,19.99,100,https://webscraper.io/test-sites/e-commerce/static/products/1
2,Sample Shoes,49.99,50,https://webscraper.io/test-sites/e-commerce/static/products/2
```