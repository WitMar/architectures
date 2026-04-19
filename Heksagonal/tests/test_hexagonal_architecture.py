import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.adapters.orders_in_memory import InMemoryOrderRepositoryAdapter
from app.adapters.users_in_memory import InMemoryUserAdapter
from app.application.create_order import CreateOrderUseCase


class HexagonalArchitectureTests(unittest.TestCase):
    def test_create_order_use_case_returns_and_saves_order(self):
        user_adapter = InMemoryUserAdapter()
        order_adapter = InMemoryOrderRepositoryAdapter()
        use_case = CreateOrderUseCase(user_adapter, order_adapter)

        order = use_case.execute(1, "Laptop")

        self.assertEqual(order.user_id, 1)
        self.assertEqual(order.user_name, "Marcin")
        self.assertEqual(order.product, "Laptop")
        self.assertEqual(len(order_adapter.saved_orders), 1)
        self.assertIs(order_adapter.saved_orders[0], order)


if __name__ == "__main__":
    unittest.main()

