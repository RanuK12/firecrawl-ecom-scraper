# Firecrawl E-commerce Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-v4.30.2%2B-green.svg)](https://firecrawl.dev)

Un scraper de e-commerce profesional que extrae catálogos de productos, precios e información de stock usando la API de Firecrawl. Ideal para análisis de mercado, comparación de precios y monitoreo de inventario.

## Características

- 🚀 Extracción rápida de datos de productos mediante API Firecrawl
- 💰 Manejo automático de múltiples formatos de precios (€, $, € con comas decimales)
- 📊 Exportación a CSV con estructura limpia y organizada
- 🔒 Manejo robusto de errores con reintentos automáticos
- 🎯 Soporte para sitios de prueba y producción
- 💻 Interfaz de línea de comandos intuitiva
- 🎨 Salida en terminal con formato agradable (opcional)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/RanuK12/firecrawl-ecom-scraper.git
cd firecrawl-ecom-scraper
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Obtén tu clave API de Firecrawl:
   - Visita [https://firecrawl.dev](https://firecrawl.dev)
   - Regístrate y obtén tu clave API gratuita

2. Crea un archivo `.env` en la raíz del proyecto:
```bash
cp .env.example .env
```

3. Edita el archivo `.env` con tus datos:
```env
FIRECRAWL_API_KEY=your_api_key_here
TARGET_URL=https://webscraper.io/test-sites/e-commerce/static
OUTPUT_CSV=output.csv
```

## Uso

### Ejemplo Básico

Ejecuta el scraper en un sitio de prueba:
```bash
python scraper.py
```

### Ejemplo con Parámetros Personalizados

Scrapea un sitio específico con salida personalizada:
```bash
python scraper.py --url https://example.com/products --output custom_products.csv --no-rich
```

### Ejemplo con Script de Demostración

Usa el script de ejemplo para probar rápidamente:
```bash
python example_run.py
```

## Formato de Salida CSV

El scraper genera un archivo CSV con la siguiente estructura:

| product_id | title | price | stock | url |
|------------|-------|-------|-------|-----|
| 1 | Sample Shirt | 19.99 | 100 | https://webscraper.io/test-sites/e-commerce/static/products/1 |
| 2 | Sample Shoes | 49.99 | 50 | https://webscraper.io/test-sites/e-commerce/static/products/2 |

**Columnas:**
- `product_id`: Identificador único del producto
- `title`: Nombre del producto
- `price`: Precio formateado (sin símbolos de moneda)
- `stock`: Cantidad disponible en inventario
- `url`: URL del producto

## Requisitos

- Python 3.8+
- Clave API de Firecrawl (gratis disponible)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Autor

[RanuK12](https://github.com/RanuK12)