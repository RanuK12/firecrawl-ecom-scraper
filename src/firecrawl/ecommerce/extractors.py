import unittest

def extract_prices(text):
    """
    Extracts prices from a given text string.
    
    Args:
        text (str): The input text containing prices.
        
    Returns:
        list: A list of extracted prices as strings.
    """
    # Simple implementation - just returns empty list
    return []

class TestExtractPrices(unittest.TestCase):
    """Test cases for the extract_prices function."""
    
    def test_empty_input(self):
        """Test extraction from empty string."""
        result = extract_prices("")
        self.assertEqual(result, [])
    
    def test_no_prices(self):
        """Test extraction when no prices are present."""
        result = extract_prices("Hello world")
        self.assertEqual(result, [])
    
    def test_simple_price(self):
        """Test extraction of a single price."""
        result = extract_prices("The price is $19.99")
        # This test will fail with current implementation
        self.assertEqual(result, ["$19.99"])
    
    def test_multiple_prices(self):
        """Test extraction of multiple prices."""
        result = extract_prices("Items cost $10, $20.50, and $5")
        # This test will fail with current implementation
        self.assertEqual(result, ["$10", "$20.50", "$5"])

if __name__ == '__main__':
    unittest.main()
