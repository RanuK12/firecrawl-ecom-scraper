import unittest
from scraper import _price_style, _stock_style

class TestPriceAndStockStyle(unittest.TestCase):
    def test_price_style_high_value(self):
        """High price (>100) should return bold green."""
        self.assertEqual(_price_style("150.00"), "bold green")
        self.assertEqual(_price_style("120"), "bold green")
    
    def test_price_style_normal_value(self):
        """Normal price (<=100) should return green."""
        self.assertEqual(_price_style("99.99"), "green")
        self.assertEqual(_price_style("50"), "green")
        self.assertEqual(_price_style("0"), "green")
        self.assertEqual(_price_style("100"), "green")
    
    def test_price_style_invalid(self):
        """Invalid price should return dim yellow."""
        self.assertEqual(_price_style("abc"), "dim yellow")
        self.assertEqual(_price_style(""), "dim yellow")
        self.assertEqual(_price_style("not_a_number"), "dim yellow")
    
    def test_price_style_european_format(self):
        """European decimal comma should work."""
        self.assertEqual(_price_style("99,99"), "green")
        self.assertEqual(_price_style("150,00"), "bold green")
    
    def test_stock_style_out_of_stock(self):
        """Out of stock indicators should return red."""
        self.assertEqual(_stock_style("0"), "red")
        self.assertEqual(_stock_style("out of stock"), "red")
        self.assertEqual(_stock_style("agotado"), "red")
        self.assertEqual(_stock_style("sin stock"), "red")
        self.assertEqual(_stock_style("no disponible"), "red")
        self.assertEqual(_stock_style("unavailable"), "red")
        self.assertEqual(_stock_style("sold out"), "red")
        self.assertEqual(_stock_style(""), "red")
    
    def test_stock_style_in_stock(self):
        """In stock indicators should return yellow."""
        self.assertEqual(_stock_style("in stock"), "yellow")
        self.assertEqual(_stock_style("disponible"), "yellow")
        self.assertEqual(_stock_style("available"), "yellow")
        self.assertEqual(_stock_style("en stock"), "yellow")
        self.assertEqual(_stock_style("contact us"), "yellow")
        self.assertEqual(_stock_style("consultar"), "yellow")
        self.assertEqual(_stock_style("n/a"), "yellow")
    
    def test_stock_style_numeric(self):
        """Numeric stock should return green for >0, red for 0."""
        self.assertEqual(_stock_style("5"), "green")
        self.assertEqual(_stock_style("10"), "green")
        self.assertEqual(_stock_style("100"), "green")
        self.assertEqual(_stock_style("0"), "red")
    
    def test_stock_style_numeric_with_text(self):
        """Numeric stock with text should be parsed."""
        self.assertEqual(_stock_style("5 in stock"), "green")
        self.assertEqual(_stock_style("10 disponibles"), "green")
        self.assertEqual(_stock_style("0 left"), "red")
    
    def test_stock_style_unknown_numeric(self):
        """Non-numeric strings should return yellow."""
        # These will not be numeric after removing non-digits
        self.assertEqual(_stock_style("abc"), "yellow")
        self.assertEqual(_stock_style("n/a"), "yellow")
        self.assertEqual(_stock_style("ask at store"), "yellow")
    
    def test_stock_style_mixed_case(self):
        """Stock status should be case insensitive."""
        self.assertEqual(_stock_style("IN STOCK"), "yellow")
        self.assertEqual(_stock_style("OUT OF STOCK"), "red")
        self.assertEqual(_stock_style("5"), "green")

if __name__ == '__main__':
    unittest.main()