import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.application.create_order import create_order


class LayeredArchitectureTests(unittest.TestCase):
    def test_create_order_returns_order(self):
        order = create_order(1, "Marcin", "Laptop")

        self.assertEqual(order.user_id, 1)
        self.assertEqual(order.user_name, "Marcin")
        self.assertEqual(order.product, "Laptop")


if __name__ == "__main__":
    unittest.main()

