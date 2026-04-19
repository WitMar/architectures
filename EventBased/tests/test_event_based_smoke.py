import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.events.bus import EventBus
from app.notifications.handler import send_order_confirmation
from app.orders.service import OrderService


class EventBasedSmokeTests(unittest.TestCase):
    def test_create_order_publishes_event_and_calls_handler(self):
        bus = EventBus()
        bus.subscribe("OrderCreated", send_order_confirmation)
        orders = OrderService(bus)

        output = io.StringIO()
        with redirect_stdout(output):
            order = orders.create_order(1, "Marcin", "Laptop")

        self.assertEqual(
            order,
            {"user_id": 1, "user_name": "Marcin", "product": "Laptop"},
        )
        self.assertIn(
            "Sending notification for Marcin and product Laptop",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()

