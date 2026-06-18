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

if __name__ == '__main__':
    unittest.main()
