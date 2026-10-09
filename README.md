# firecrawl-ecom-scraper

A quick scraper for e-commerce sites using **Firecrawl**.

## Quick start

1. Clona el repositorio:
   ```bash
   git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git && cd firecrawl-ecom-scraper
   ```

2. Configura tu clave API de Firecrawl:
   ```bash
   cp .env.example .env
   ```
   
   Edita `.env` y agrega tu clave API y la URL del sitio:
   ```
   FIRECRAWL_API_KEY=your_api_key_here
   TARGET_URL=https://webscraper.io/test-sites/e-commerce/static
   OUTPUT_CSV=output.csv
   ```

3. Ejecuta el ejemplo:
   ```bash
   python3 example_run.py
   ```
   
   El CSV de muestra se encontrará en `sample_output.csv`.

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
