import csv
import os
import tempfile
import unittest

from validate_output import validate_csv, parse_price


class TestValidateOutput(unittest.TestCase):
    def _write_csv(self, rows, header=None):
        header = header or ["name", "price", "stock", "description"]
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
        return path

    def test_valid_csv(self):
        path = self._write_csv([
            ["Sample Shirt", "19.99", "100", "A comfortable cotton shirt"],
            ["Wireless Headphones", "89,50", "30", "Noise-cancelling headphones"],
        ])
        self.assertEqual(validate_csv(path), [])
        os.unlink(path)

    def test_missing_columns(self):
        path = self._write_csv([["foo", "bar"]], header=["foo", "bar"])
        errors = validate_csv(path)
        self.assertTrue(any("Columnas faltantes" in e for e in errors))
        os.unlink(path)

    def test_empty_cell(self):
        path = self._write_csv([["", "19.99", "100", "shirt"]])
        errors = validate_csv(path)
        self.assertTrue(any("vacía" in e for e in errors))
        os.unlink(path)

    def test_invalid_price(self):
        path = self._write_csv([["Shirt", "abc", "100", "shirt"]])
        errors = validate_csv(path)
        self.assertTrue(any("precio inválido" in e for e in errors))
        os.unlink(path)

    def test_european_price(self):
        path = self._write_csv([["Shirt", "1.200,50", "100", "shirt"]])
        self.assertEqual(validate_csv(path), [])
        os.unlink(path)

    def test_non_integer_stock(self):
        path = self._write_csv([["Shirt", "19.99", "veinte", "shirt"]])
        errors = validate_csv(path)
        self.assertTrue(any("stock no es entero" in e for e in errors))
        os.unlink(path)

    def test_file_not_found(self):
        errors = validate_csv("/no/existe.csv")
        self.assertTrue(any("no encontrado" in e for e in errors))

    def test_parse_price_variants(self):
        self.assertAlmostEqual(parse_price("19.99"), 19.99)
        self.assertAlmostEqual(parse_price("19,99"), 19.99)
        self.assertAlmostEqual(parse_price("1.200,50"), 1200.50)
        self.assertAlmostEqual(parse_price("$1,200.50"), 1200.50)
        self.assertIsNone(parse_price("abc"))
        self.assertIsNone(parse_price(""))


if __name__ == "__main__":
    unittest.main()
