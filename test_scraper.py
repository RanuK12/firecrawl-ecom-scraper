import unittest
import os
import tempfile
import csv
import json
from scraper import extract_product_fields, save_results, _infer_format

class TestExtractProductFields(unittest.TestCase):

    def test_all_fields_present(self):
        product = {
            'name': 'Laptop',
            'price': '999.99',
            'stock': '10',
            'description': 'High performance laptop'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Laptop')
        self.assertEqual(result['price'], '999.99')
        self.assertEqual(result['stock'], '10')
        self.assertEqual(result['description'], 'High performance laptop')

    def test_missing_price(self):
        product = {
            'name': 'Phone',
            'stock': '5',
            'description': 'Smartphone'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Phone')
        self.assertEqual(result['price'], '')
        self.assertEqual(result['stock'], '5')
        self.assertEqual(result['description'], 'Smartphone')

    def test_missing_stock(self):
        product = {
            'name': 'Tablet',
            'price': '299.99',
            'description': 'A nice tablet'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Tablet')
        self.assertEqual(result['price'], '299.99')
        self.assertEqual(result['stock'], '')
        self.assertEqual(result['description'], 'A nice tablet')

    def test_missing_description(self):
        product = {
            'name': 'Monitor',
            'price': '199.99',
            'stock': '3'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Monitor')
        self.assertEqual(result['price'], '199.99')
        self.assertEqual(result['stock'], '3')
        self.assertEqual(result['description'], '')

    def test_european_price_formats(self):
        # Precios con separador de miles y coma como decimal (formato europeo)
        product = {
            'name': 'Smartphone',
            'price': '1.200,50',  # 1200.50
            'stock': '25',
            'description': 'Smartphone de alta gama'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Smartphone')
        self.assertEqual(result['price'], '1200.50')
        self.assertEqual(result['stock'], '25')
        self.assertEqual(result['description'], 'Smartphone de alta gama')

        # Precio sin separador de miles
        product = {
            'name': 'Tablet',
            'price': '499,99',  # 499.99
            'stock': '12',
            'description': 'Tablet con pantalla táctil'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Tablet')
        self.assertEqual(result['price'], '499.99')
        self.assertEqual(result['stock'], '12')
        self.assertEqual(result['description'], 'Tablet con pantalla táctil')

        # Precio con separador de miles y sin decimales
        product = {
            'name': 'Televisor',
            'price': '1.599',  # 1599
            'stock': '8',
            'description': 'Televisor 4K 55"'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Televisor')
        self.assertEqual(result['price'], '1599')
        self.assertEqual(result['stock'], '8')
        self.assertEqual(result['description'], 'Televisor 4K 55"')

    def test_missing_name(self):
        product = {
            'price': '49.99',
            'stock': '20',
            'description': 'Wireless mouse'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], '')
        self.assertEqual(result['price'], '49.99')
        self.assertEqual(result['stock'], '20')
        self.assertEqual(result['description'], 'Wireless mouse')

    def test_empty_dict(self):
        product = {}
        result = extract_product_fields(product)
        self.assertEqual(result['name'], '')
        self.assertEqual(result['price'], '')
        self.assertEqual(result['stock'], '')
        self.assertEqual(result['description'], '')

    def test_special_characters_and_currency(self):
        product = {
            'name': '  Laptop Pro  ',
            'price': '  $1,299.99  ',
            'stock': '  10  ',
            'description': '  High-end laptop  '
        }
        result = extract_product_fields(product)
        self.assertEqual(result['name'], 'Laptop Pro')
        self.assertEqual(result['price'], '1299.99')
        self.assertEqual(result['stock'], '10')
        self.assertEqual(result['description'], 'High-end laptop')

class TestFindAndSaveProducts(unittest.TestCase):

    def test_find_products_flat_keys(self):
        '''_find_products finds products at top-level keys like 'products', 'items', 'results'.'''
        from scraper import _find_products
        data = {'products': [{'name': 'A', 'price': '10'}, {'name': 'B', 'price': '20'}]}
        result = _find_products(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'A')

    def test_find_products_deep_nested(self):
        '''_find_products finds products nested deep like data.products.nodes.'''
        from scraper import _find_products
        data = {'data': {'category': {'products': {'nodes': [{'name': 'X', 'price': '100'}, {'name': 'Y', 'price': '200'}]}}}}
        result = _find_products(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'X')

    def test_find_products_with_edges(self):
        '''_find_products finds products inside edges[].node structure (GraphQL style).'''
        from scraper import _find_products
        data = {'data': {'products': {'edges': [{'node': {'name': 'P1', 'price': '50'}}, {'node': {'name': 'P2', 'price': '60'}}]}}}
        result = _find_products(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'P1')

    def test_find_products_prefers_product_lists(self):
        '''_find_products prefers lists with product-like items over empty or non-product lists.'''
        from scraper import _find_products
        data = {
            'products': [],
            'items': [{'not_a_product': 1}, {'not_a_product': 2}],
            'deeper': {'results': [{'name': 'Real', 'price': '30', 'sku': '001'}]}
        }
        result = _find_products(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Real')

    def test_find_products_returns_empty(self):
        '''_find_products returns empty list when no product-like data exists.'''
        from scraper import _find_products
        data = {'some': {'random': {'nested': {'stuff': [1, 2, 3]}}}}
        result = _find_products(data)
        self.assertEqual(result, [])

    def test_looks_like_product_true(self):
        '''_looks_like_product returns True for dicts with at least 2 product key groups.'''
        from scraper import _find_products
        # Access the inner function via closure trick
        import scraper
        # Re-create the logic inline
        item = {'name': 'Test', 'price': '10'}
        # Just call _find_products with a structure that exercises it
        data = {'items': [item]}
        result = _find_products(data)
        self.assertEqual(len(result), 1)

    def test_looks_like_product_false(self):
        '''_looks_like_product returns False for non-product dicts.'''
        from scraper import _find_products
        data = {'items': [{'foo': 'bar', 'baz': 123}]}
        result = _find_products(data)
        self.assertEqual(result, [])

    def test_save_results_csv(self):
        '''save_results writes CSV with correct fields.'''
        from scraper import save_results
        products = [
            {'name': 'Laptop', 'price': '999.99', 'stock': '10', 'description': 'High performance laptop'},
            {'name': 'Phone', 'price': '499.99', 'stock': '5', 'description': 'Smartphone'},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='csv', pretty=False)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['name'], 'Laptop')
            self.assertEqual(rows[0]['price'], '999.99')
            self.assertEqual(rows[0]['stock'], '10')
            self.assertEqual(rows[0]['description'], 'High performance laptop')
            self.assertEqual(rows[1]['name'], 'Phone')
            self.assertEqual(rows[1]['price'], '499.99')
            self.assertEqual(rows[1]['stock'], '5')
            self.assertEqual(rows[1]['description'], 'Smartphone')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save_results_json(self):
        '''save_results writes JSON with correct fields.'''
        from scraper import save_results
        products = [
            {'name': 'Laptop', 'price': '999.99', 'stock': '10', 'description': 'High performance laptop'},
            {'name': 'Phone', 'price': '499.99', 'stock': '5', 'description': 'Smartphone'},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='json', pretty=False)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, encoding='utf-8') as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Laptop')
            self.assertEqual(data[0]['price'], '999.99')
            self.assertEqual(data[0]['stock'], '10')
            self.assertEqual(data[0]['description'], 'High performance laptop')
            self.assertEqual(data[1]['name'], 'Phone')
            self.assertEqual(data[1]['price'], '499.99')
            self.assertEqual(data[1]['stock'], '5')
            self.assertEqual(data[1]['description'], 'Smartphone')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save_results_json_pretty(self):
        '''save_results with pretty=True produces indented JSON (contains newlines).'''
        from scraper import save_results
        products = [{'name': 'Test', 'price': '10', 'stock': '1', 'description': 'desc'}]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='json', pretty=True)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, encoding='utf-8') as f:
                content = f.read()
            self.assertIn('\n', content)
            data = json.loads(content)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['name'], 'Test')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save_results_non_dict(self):
        '''save_results skips non-dict items with a warning.'''
        from scraper import save_results
        products = [
            {'name': 'Valid', 'price': '10', 'stock': '1', 'description': 'ok'},
            'not a dict',
            123,
            {'name': 'Also valid', 'price': '20', 'stock': '2', 'description': 'good'},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='csv', pretty=False)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            # Only the two dict items should be written
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['name'], 'Valid')
            self.assertEqual(rows[1]['name'], 'Also valid')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save_results_empty(self):
        '''save_results with empty list creates CSV with only headers or JSON [].'''
        from scraper import save_results
        products = []
        # CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        try:
            save_results(products, csv_path, fmt='csv', pretty=False)
            self.assertTrue(os.path.exists(csv_path))
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(rows, [])  # only headers, no data rows
        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)
        # JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_path = f.name
        try:
            save_results(products, json_path, fmt='json', pretty=False)
            self.assertTrue(os.path.exists(json_path))
            with open(json_path, encoding='utf-8') as f:
                data = json.load(f)
            self.assertEqual(data, [])
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_save_results_limit(self):
        '''save_results with limit parameter restricts rows.'''
        from scraper import save_results
        products = [
            {'name': 'Prod1', 'price': '10', 'stock': '1', 'description': 'desc1'},
            {'name': 'Prod2', 'price': '20', 'stock': '2', 'description': 'desc2'},
            {'name': 'Prod3', 'price': '30', 'stock': '3', 'description': 'desc3'},
            {'name': 'Prod4', 'price': '40', 'stock': '4', 'description': 'desc4'},
            {'name': 'Prod5', 'price': '50', 'stock': '5', 'description': 'desc5'},
        ]
        # Test limit=3
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='csv', pretty=False, limit=3)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['name'], 'Prod1')
            self.assertEqual(rows[1]['name'], 'Prod2')
            self.assertEqual(rows[2]['name'], 'Prod3')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        # Test limit=0 (no limit)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp_path = f.name
        try:
            save_results(products, tmp_path, fmt='csv', pretty=False, limit=0)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(len(rows), 5)
            self.assertEqual(rows[0]['name'], 'Prod1')
            self.assertEqual(rows[4]['name'], 'Prod5')
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_price_dash_only(self):
        """Price with just a dash should return empty string."""
        product = {
            'name': 'Product',
            'price': '-',
            'stock': '5',
            'description': 'Test'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['price'], '')

    def test_price_non_numeric(self):
        """Price with no digits at all should return empty string."""
        product = {
            'name': 'Product',
            'price': 'Free',
            'stock': '5',
            'description': 'Test'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['price'], '')

    def test_price_contact_us(self):
        """Price like 'Contact us' should return empty string."""
        product = {
            'name': 'Product',
            'price': 'Contact us for price',
            'stock': '5',
            'description': 'Test'
        }
        result = extract_product_fields(product)
        self.assertEqual(result['price'], '')

class TestInferFormat(unittest.TestCase):
    """Tests for _infer_format auto-detection from file extension."""

    def test_json_extension(self):
        self.assertEqual(_infer_format("output.json"), "json")
        self.assertEqual(_infer_format("data/products.json"), "json")

    def test_csv_extension(self):
        self.assertEqual(_infer_format("output.csv"), "csv")
        self.assertEqual(_infer_format("data/products.csv"), "csv")

    def test_no_extension_defaults_csv(self):
        self.assertEqual(_infer_format("output"), "csv")
        self.assertEqual(_infer_format("products"), "csv")

    def test_explicit_fmt_priority(self):
        self.assertEqual(_infer_format("output.json", explicit_fmt="csv"), "csv")
        self.assertEqual(_infer_format("output.csv", explicit_fmt="json"), "json")

    def test_unknown_extension_defaults_csv(self):
        self.assertEqual(_infer_format("output.txt"), "csv")
        self.assertEqual(_infer_format("data.xyz"), "csv")

if __name__ == '__main__':
    unittest.main()
