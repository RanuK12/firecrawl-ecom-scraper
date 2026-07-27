import csv
import json
import logging
import argparse
import sys
import re
import os
import requests
from typing import List, Dict, Any
from typing_extensions import TypedDict
from firecrawl import FirecrawlApp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, retry_if_exception

# Rich imports for pretty terminal output (optional — gated by --no-rich)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console() if RICH_AVAILABLE else None

class Product(TypedDict):
    name: str
    price: str
    stock: str
    description: str

def extract_product_fields(product: Dict[str, Any]) -> Product:
    """Return a dict with guaranteed keys: name, price, stock, description.
    Strips whitespace from all fields and removes currency symbols from price.
    Handles European decimal commas (e.g., 1.200,50 → 1200.50).
    """
    name = str(product.get('name', '')).strip()
    price_raw = str(product.get('price', '')).strip()
    # Remove common currency symbols and any non-digit, non-dot, non-comma, non-minus characters
    price_clean = re.sub(r'[^\d.,\-]', '', price_raw)

    # Handle negative prices
    is_negative = price_clean.startswith('-')
    if is_negative:
        price_clean = price_clean[1:]

    # Heuristic to distinguish decimal commas from thousands separators
    if ',' in price_clean:
        parts = price_clean.split(',')
        # Only consider the first comma
        before_comma = parts[0]
        after_comma = parts[1] if len(parts) >= 2 else ''
        # If the part after the comma has 1 or 2 digits (and is not empty),
        # treat the comma as a decimal separator (European style).
        if 1 <= len(after_comma) <= 2:
            # Remove all dots (thousands separators) from the part before the comma
            before_comma = before_comma.replace('.', '')
            price_clean = before_comma + '.' + after_comma
        else:
            # Comma is a thousands separator; remove it
            price_clean = price_clean.replace(',', '')
    
    # Handle multiple decimal points (e.g., '19.99.99' → '19.99')
    if price_clean.count('.') > 1:
        parts = price_clean.split('.')
        price_clean = '.'.join(parts[:2])

    # Restore negative sign if needed
    if is_negative:
        price_clean = '-' + price_clean
    else:
        # No comma present; decide whether dots are thousands separators or decimal
        dot_count = price_clean.count('.')
        if dot_count == 1:
            # Single dot: check if the part after the dot has at most 2 digits
            parts = price_clean.split('.')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Likely a decimal dot (US style) – keep as is
                pass
            else:
                # Thousands separator – remove the dot
                price_clean = price_clean.replace('.', '')
        elif dot_count > 1:
            # Multiple dots: all are thousands separators – remove them
            price_clean = price_clean.replace('.', '')
        # dot_count == 0: nothing to do

    # If after all processing the price is empty, just '-' (a dash), or non-numeric, return empty string
    if not price_clean or price_clean in ('-', '--', '-.', '.-') or not re.search(r'\d', price_clean):
        price_clean = ''

    stock = str(product.get('stock', '')).strip()
    description = str(product.get('description', '')).strip()
    return {
        'name': name,
        'price': price_clean,
        'stock': stock,
        'description': description,
    }

def save_results(products: List[Dict[str, Any]], output_file: str, fmt: str, pretty: bool, limit: int = 0, use_rich: bool = True) -> None:
    """Write products to output_file in CSV or JSON format.
    If limit > 0, only the first `limit` products are saved."""
    if limit > 0:
        products = products[:limit]
    if fmt == "csv":
        fieldnames = ['name', 'price', 'stock', 'description']
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                if not isinstance(product, dict):
                    logger.warning(f"⚠️ Elemento no es un diccionario, se omite: {product}")
                    continue
                writer.writerow(extract_product_fields(product))
    elif fmt == "json":
        # Extract fields for each product
        extracted = [extract_product_fields(p) if isinstance(p, dict) else {} for p in products]
        indent = 2 if pretty else None
        with open(output_file, mode='w', encoding='utf-8') as file:
            json.dump(extracted, file, indent=indent, ensure_ascii=False)
    else:
        raise ValueError(f"Formato no soportado: {fmt}")

    # Rich terminal output
    if use_rich and RICH_AVAILABLE and console is not None:
        _print_rich_output(products, output_file, fmt)
    else:
        logger.info(f"✅ Éxito: {len(products)} productos guardados en {output_file}")


def _price_style(price_str: str) -> str:
    """Return a Rich style string for a price based on its value."""
    try:
        val = float(price_str.replace(',', '.'))
    except (ValueError, TypeError):
        return "dim yellow"
    if val > 100:
        return "bold green"
    return "green"

def _stock_style(stock_str: str) -> str:
    """Return a Rich style string for stock status: green=in stock, red=out, yellow=unknown."""
    s = stock_str.lower().strip()
    if not s or s in ('0', 'out of stock', 'agotado', 'sin stock', 'no disponible', 'unavailable', 'sold out'):
        return "red"
    if s in ('in stock', 'disponible', 'available', 'en stock', 'contact us', 'consultar', 'n/a'):
        return "yellow"
    # Numeric: >0 means in stock
    try:
        n = int(re.sub(r'[^\d]', '', s))
        return "green" if n > 0 else "red"
    except ValueError:
        return "yellow"

def _print_rich_output(products: List[Dict[str, Any]], output_file: str, fmt: str) -> None:
    """Print a Rich table of products and a summary panel with stats."""
    from datetime import datetime

    # Table of first 10 products
    table = Table(title="💰🛒 Productos Encontrados", box=box.ROUNDED,
                  header_style="bold cyan", title_style="bold white",
                  row_styles=["dim", ""])
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Nombre", style="white", max_width=50, overflow="ellipsis")
    table.add_column("Precio", justify="right", width=14)
    table.add_column("Stock", width=14)
    table.add_column("Descripción", style="dim", max_width=60, overflow="ellipsis")

    displayed = products[:10]
    numeric_prices = []
    in_stock_count = 0
    out_stock_count = 0

    for i, product in enumerate(displayed, 1):
        fields = extract_product_fields(product) if isinstance(product, dict) else {'name': '', 'price': '', 'stock': '', 'description': ''}
        price = fields.get('price', '')
        stock = fields.get('stock', '')

        # Track stats across ALL products (not just displayed)
        pstyle = _price_style(price)
        sstyle = _stock_style(stock)
        table.add_row(
            str(i),
            fields.get('name', '')[:46],
            f"[{pstyle}]{price}[/]",
            f"[{sstyle}]{stock[:12]}[/]",
            fields.get('description', '')[:56],
        )

    # Stats across all products
    for product in products:
        fields = extract_product_fields(product) if isinstance(product, dict) else {'name': '', 'price': '', 'stock': '', 'description': ''}
        price = fields.get('price', '')
        stock = fields.get('stock', '')
        try:
            numeric_prices.append(float(price.replace(',', '.')))
        except (ValueError, TypeError):
            pass
        s = stock.lower().strip()
        if s and s not in ('0', 'out of stock', 'agotado', 'sin stock', 'no disponible', 'unavailable', 'sold out'):
            try:
                n = int(re.sub(r'[^\d]', '', s))
                if n > 0:
                    in_stock_count += 1
                else:
                    out_stock_count += 1
            except ValueError:
                in_stock_count += 1  # assume ambiguous = in stock
        else:
            out_stock_count += 1

    console.print(table)

    # Summary panel with stats
    total = len(products)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary_text = (
        f"[bold white]Archivo:[/] [cyan]{output_file}[/]\n"
        f"[bold white]Formato:[/] [cyan]{fmt.upper()}[/]\n"
        f"[bold white]Productos:[/] [green]{total}[/]"
    )
    if len(products) > 10:
        summary_text += f"\n[dim](mostrando primeros 10 de {total})[/]"
    if numeric_prices:
        avg_price = sum(numeric_prices) / len(numeric_prices)
        min_price = min(numeric_prices)
        max_price = max(numeric_prices)
        summary_text += (
            f"\n[bold white]Precio prom.:[/] [green]${avg_price:,.2f}[/]"
            f"\n[bold white]Rango:[/] [dim]${min_price:,.2f}[/] – [bold green]${max_price:,.2f}[/]"
        )
        # Mini bar chart: top 5 most expensive products
        if len(displayed) >= 2 and numeric_prices:
            summary_text += "\n\n[bold white]Top precios:[/]"
            # Build list of (name, price) from displayed, sort by price desc
            priced_items = []
            for product in displayed:
                fields = extract_product_fields(product) if isinstance(product, dict) else {}
                p = fields.get('price', '')
                n = fields.get('name', '')
                try:
                    p_val = float(p.replace(',', '.'))
                except (ValueError, TypeError):
                    continue
                priced_items.append((n, p_val))
            priced_items.sort(key=lambda x: x[1], reverse=True)
            top5 = priced_items[:5]
            if top5:
                max_p = top5[0][1]
                bar_colors = ["bold green", "green", "yellow", "yellow", "dim yellow"]
                for idx, (pname, pval) in enumerate(top5):
                    name_trunc = pname[:20].ljust(20)
                    bar_width = max(1, int((pval / max_p) * 30)) if max_p > 0 else 1
                    bar = "█" * bar_width
                    color = bar_colors[min(idx, len(bar_colors) - 1)]
                    summary_text += f"\n  [dim]{name_trunc}[/] [bold ${color}]{bar}[/] [green]${pval:,.2f}[/]"
    summary_text += (
        f"\n\n[bold white]Con stock:[/] [green]{in_stock_count}[/]  "
        f"[bold white]Sin stock:[/] [red]{out_stock_count}[/]"
        f"\n\n[dim]⏱️  Scrapeado: {now}[/]"
    )

    console.print(Panel(summary_text, title="📦 Resumen", border_style="cyan", box=box.HEAVY))

def _find_products(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Try multiple common keys to locate a list of product dicts.
    If not found, perform a recursive deep search through all dicts/arrays
    looking for any list where the items look like products.
    Returns the deepest/most relevant list found.
    """
    # Helper to decide if a dict looks like a product
    def _looks_like_product(item: Any) -> bool:
        if not isinstance(item, dict):
            return False
        # Define groups of keys that indicate a product
        name_keys = {'name', 'title'}
        price_keys = {'price', 'amount', 'cost', 'salePrice'}
        sku_keys = {'sku', 'id', 'productId'}
        desc_keys = {'description', 'desc', 'shortDescription'}
        stock_keys = {'stock', 'availability', 'inventory', 'quantity'}
        # Count how many groups have at least one key present
        count = 0
        if any(k in item for k in name_keys):
            count += 1
        if any(k in item for k in price_keys):
            count += 1
        if any(k in item for k in sku_keys):
            count += 1
        if any(k in item for k in desc_keys):
            count += 1
        if any(k in item for k in stock_keys):
            count += 1
        return count >= 2

    # Helper to unwrap GraphQL edges[].node
    def _unwrap(item: Any) -> Any:
        if isinstance(item, dict) and 'node' in item:
            return item['node']
        return item

    # Recursive DFS to find product-like lists
    best_list: List[Dict[str, Any]] = []
    best_depth = -1
    best_score = -1

    def _dfs(obj: Any, depth: int) -> None:
        nonlocal best_list, best_depth, best_score
        if isinstance(obj, dict):
            for value in obj.values():
                _dfs(value, depth + 1)
        elif isinstance(obj, list):
            # Evaluate this list
            if len(obj) > 0:
                # Unwrap nodes before counting product-like items
                unwrapped_items = [_unwrap(item) for item in obj]
                product_count = sum(1 for item in unwrapped_items if _looks_like_product(item))
                # Score: product_count, with tie‑breaker on depth (deeper is better)
                # We'll prefer higher product_count, then higher depth
                if product_count > 0 and (product_count > best_score or (product_count == best_score and depth > best_depth)):
                    best_score = product_count
                    best_depth = depth
                    best_list = unwrapped_items
            # Recurse into each element (unwrapped for deeper search)
            for item in obj:
                _dfs(_unwrap(item), depth + 1)

    _dfs(data, 0)

    # Only return a list if at least one product‑like item was found
    if best_score > 0:
        return best_list
    return []

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=(retry_if_exception_type(requests.exceptions.RequestException) |
           retry_if_exception(lambda e: isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429))
)
def _scrape_with_retry(app, url):
    return app.scrape_url(url, params={'formats': ['json']})

def _infer_format(output_file: str, explicit_fmt: str | None = None) -> str:
    """Infer output format from file extension. explicit_fmt (if not None) takes priority."""
    if explicit_fmt is not None and explicit_fmt in ("csv", "json"):
        return explicit_fmt
    ext = os.path.splitext(output_file)[1].lower()
    if ext == ".json":
        return "json"
    return "csv"

def scrape_ecommerce(url: str, api_key: str, output_file: str = "products_output.csv", fmt: str = "csv", pretty: bool = False, limit: int = 0, use_rich: bool = True) -> bool:
    """Scrape product data from an e-commerce URL using Firecrawl API.
    
    This is the main entry point for the scraper. It fetches structured data from the
    given URL, automatically detects product listings in the response (handling various
    JSON structures including GraphQL edges), normalizes the extracted fields, and saves
    the results to a file.
    
    Args:
        url: The e-commerce URL to scrape.
        api_key: Firecrawl API key for authentication.
        output_file: Path to the output file. Defaults to "products_output.csv".
        fmt: Output format, either "csv" or "json". Defaults to "csv".
        pretty: If True, indent JSON output. Only applies when fmt is "json". Defaults to False.
        limit: Maximum number of products to save. 0 means no limit. Defaults to 0.
        use_rich: If True and Rich is installed, use pretty terminal output. Defaults to True.
    
    Returns:
        True if scraping and saving succeeded, False otherwise.
    """
    try:
        app = FirecrawlApp(api_key=api_key)

        if use_rich and RICH_AVAILABLE and console is not None:
            from datetime import datetime
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            header_text = f"[bold white]URL:[/] [cyan]{url}[/]\n[dim cyan]v1.2.0[/] [dim]— {now}[/]"
            console.print(Panel(header_text, title="🚀 Firecrawl E-commerce Scraper", border_style="cyan", box=box.HEAVY))
            with Progress(SpinnerColumn(spinner_name="dots12"), TextColumn("[cyan]Scrapeando...[/]"), transient=True) as progress:
                progress.add_task("scraping", total=None)
                try:
                    scrape_result = _scrape_with_retry(app, url)
                except Exception as conn_err:
                    logger.error(f"❌ Error de conexión con FirecrawlApp: {conn_err}")
                    return False
        else:
            logger.info(f"🚀 Iniciando scraping de: {url}")
            try:
                scrape_result = _scrape_with_retry(app, url)
            except Exception as conn_err:
                logger.error(f"❌ Error de conexión con FirecrawlApp: {conn_err}")
                return False
        
        if not scrape_result or 'data' not in scrape_result:
            logger.error("❌ Error: No se pudieron obtener datos del sitio.")
            return False

        data = scrape_result['data']
        if not isinstance(data, dict):
            logger.error(f"❌ Error: Los datos obtenidos no tienen el formato esperado (dict), se recibió {type(data).__name__}.")
            return False
        
        # Intentamos extraer campos comunes
        products: List[Dict[str, Any]] = _find_products(data)
        if not products:
            logger.warning("⚠️ No se encontraron productos en los datos obtenidos. No se guardará ningún archivo.")
            return False

        save_results(products, output_file, fmt, pretty, limit=limit, use_rich=use_rich)
        return True
                
    except Exception as e:
        logger.error(f"💥 Error inesperado durante el scraping: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firecrawl E-commerce Scraper")
    parser.add_argument("--url", required=True, help="URL de la tienda")
    parser.add_argument("--key", required=True, help="Firecrawl API Key")
    parser.add_argument("--output", default="products_output.csv",
                        help="Nombre del archivo CSV de salida")
    parser.add_argument("--format", choices=["csv","json"], default="csv",
                        help="Formato de salida (csv o json)")
    parser.add_argument("--pretty", action="store_true",
                        help="Indentar JSON (solo aplica con --format json)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Número máximo de productos a guardar (0 = sin límite)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suprimir mensajes INFO, solo mostrar advertencias y errores")
    parser.add_argument("--no-rich", action="store_true",
                        help="Desactivar salida formateada con Rich (usar texto plano)")
    parser.add_argument("--version", action="version",
                        version="firecrawl-ecom-scraper 1.0.0",
                        help="Mostrar la versión y salir")
    
    args = parser.parse_args()
    if args.quiet:
        logger.setLevel(logging.WARNING)
    use_rich = not args.no_rich and not args.quiet
    # Invert format from file extension if --format is default "csv" and extension is .json
    fmt = _infer_format(args.output, args.format)
    try:
        success = scrape_ecommerce(args.url, args.key, args.output, fmt, args.pretty, limit=args.limit, use_rich=use_rich)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Scraping interrumpido por el usuario.")
        sys.exit(130)
