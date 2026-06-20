import unittest
from scraper import extract_product_fields

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

def test_find_products_flat_keys():
    '''_find_products finds products at top-level keys like 'products', 'items', 'results'.'''
    from scraper import _find_products
    data = {'products': [{'name': 'A', 'price': '10'}, {'name': 'B', 'price': '20'}]}
    result = _find_products(data)
    assert len(result) == 2
    assert result[0]['name'] == 'A'

def test_find_products_deep_nested():
    '''_find_products finds products nested deep like data.products.nodes.'''
    from scraper import _find_products
    data = {'data': {'category': {'products': {'nodes': [{'name': 'X', 'price': '100'}, {'name': 'Y', 'price': '200'}]}}}}
    result = _find_products(data)
    assert len(result) == 2
    assert result[0]['name'] == 'X'

def test_find_products_with_edges():
    '''_find_products finds products inside edges[].node structure (GraphQL style).'''
    from scraper import _find_products
    data = {'data': {'products': {'edges': [{'node': {'name': 'P1', 'price': '50'}}, {'node': {'name': 'P2', 'price': '60'}}]}}}
    result = _find_products(data)
    assert len(result) == 2
    assert result[0]['name'] == 'P1'

def test_find_products_prefers_product_lists():
    '''_find_products prefers lists with product-like items over empty or non-product lists.'''
    from scraper import _find_products
    data = {
        'products': [],
        'items': [{'not_a_product': 1}, {'not_a_product': 2}],
        'deeper': {'results': [{'name': 'Real', 'price': '30', 'sku': '001'}]}
    }
    result = _find_products(data)
    assert len(result) == 1
    assert result[0]['name'] == 'Real'

def test_find_products_returns_empty():
    '''_find_products returns empty list when no product-like data exists.'''
    from scraper import _find_products
    data = {'some': {'random': {'nested': {'stuff': [1, 2, 3]}}}}
    result = _find_products(data)
    assert result == []

def test_looks_like_product_true():
    '''_looks_like_product returns True for dicts with at least 2 product key groups.'''
    from scraper import _find_products
    # Access the inner function via closure trick
    import scraper
    # Re-create the logic inline
    item = {'name': 'Test', 'price': '10'}
    # Just call _find_products with a structure that exercises it
    data = {'items': [item]}
    result = _find_products(data)
    assert len(result) == 1

def test_looks_like_product_false():
    '''_looks_like_product returns False for non-product dicts.'''
    from scraper import _find_products
    data = {'items': [{'foo': 'bar', 'baz': 123}]}
    result = _find_products(data)
    assert result == []

if __name__ == '__main__':
    unittest.main()
