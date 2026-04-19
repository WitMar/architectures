import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.loyalty import handler as loyalty_handler
from app.loyalty.handler import register_loyalty_points, saved_points
from app.main import InMemoryOutboxRepository, create_example_runtime, publish_all_pending_events


class EventBasedSmokeTests(unittest.TestCase):
    def setUp(self):
        saved_points.clear()
        loyalty_handler.should_fail_to_save_points = False

    def test_create_order_publishes_event_and_calls_handler(self):
        runtime = create_example_runtime()

        output = io.StringIO()
        with redirect_stdout(output):
            order = runtime["orders"].create_order(1, "Marcin", "Laptop")
            publish_all_pending_events(
                runtime["order_outbox_publisher"],
                runtime["loyalty_outbox_publisher"],
            )

        self.assertEqual(
            order,
            {
                "order_id": 101,
                "user_id": 1,
                "user_name": "Marcin",
                "product": "Laptop",
                "status": "PROCESSED",
            },
        )
        self.assertIn(
            "Sending notification for done order for Marcin and product Laptop",
            output.getvalue(),
        )
        self.assertEqual(
            saved_points,
            [{"user_id": 1, "points": 10, "source_order_id": 101}],
        )
        self.assertEqual(runtime["order_repository"].orders[0]["status"], "PROCESSED")
        self.assertEqual(runtime["order_outbox_repository"].messages[0]["status"], "PUBLISHED")
        self.assertEqual(runtime["order_outbox_repository"].messages[1]["event_name"], "OrderProcessed")
        self.assertEqual(runtime["order_outbox_repository"].messages[1]["status"], "PUBLISHED")
        self.assertEqual(runtime["loyalty_outbox_repository"].messages[0]["event_name"], "LoyaltyPointsAdded")
        self.assertEqual(runtime["loyalty_outbox_repository"].messages[0]["status"], "PUBLISHED")

    def test_register_loyalty_points_saves_points_and_writes_follow_up_outbox_event_only_once(self):
        loyalty_outbox_repository = InMemoryOutboxRepository(name="loyalty")

        event = {
            "order_id": 101,
            "user_id": 1,
            "user_name": "Marcin",
            "product": "Laptop",
            "points_to_add": 10,
        }

        register_loyalty_points(event, outbox_repository=loyalty_outbox_repository)
        register_loyalty_points(event, outbox_repository=loyalty_outbox_repository)

        self.assertEqual(
            saved_points,
            [{"user_id": 1, "points": 10, "source_order_id": 101}],
        )
        self.assertEqual(
            loyalty_outbox_repository.messages,
            [
                {
                    "event_name": "LoyaltyPointsAdded",
                    "payload": {
                        "order_id": 101,
                        "user_id": 1,
                        "user_name": "Marcin",
                        "product": "Laptop",
                        "points_added": 10,
                    },
                    "status": "NEW",
                }
            ],
        )

    def test_if_loyalty_points_save_fails_order_is_retracted_and_not_confirmed(self):
        loyalty_handler.should_fail_to_save_points = True
        runtime = create_example_runtime()

        output = io.StringIO()
        with redirect_stdout(output):
            order = runtime["orders"].create_order(1, "Marcin", "Laptop")
            publish_all_pending_events(
                runtime["order_outbox_publisher"],
                runtime["loyalty_outbox_publisher"],
            )

        self.assertEqual(order["status"], "RETRACTED")
        self.assertEqual(saved_points, [])
        self.assertNotIn("Sending notification", output.getvalue())
        self.assertEqual(runtime["order_outbox_repository"].messages, [{
            "event_name": "OrderCreated",
            "payload": {
                "order_id": 101,
                "user_id": 1,
                "user_name": "Marcin",
                "product": "Laptop",
                "points_to_add": 10,
            },
            "status": "PUBLISHED",
        }])
        self.assertEqual(runtime["loyalty_outbox_repository"].messages, [{
            "event_name": "LoyaltyPointsSaveFailed",
            "payload": {
                "order_id": 101,
                "user_id": 1,
                "user_name": "Marcin",
                "product": "Laptop",
                "reason": "Could not save loyalty points",
            },
            "status": "PUBLISHED",
        }])


if __name__ == "__main__":
    unittest.main()

