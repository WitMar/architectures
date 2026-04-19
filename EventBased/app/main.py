from functools import partial
from EventBased.app.events.bus import EventBus
from EventBased.app.events.outbox_publisher import OutboxPublisher
from EventBased.app.loyalty.handler import register_loyalty_points
from EventBased.app.notifications.handler import send_order_confirmation
from EventBased.app.orders.handler import mark_order_as_processed, retract_order
from EventBased.app.orders.service import OrderService


class InMemoryOrderRepository:
    def __init__(self):
        self.orders = []

    def save(self, order):
        print("Saving order to DB", order)
        self.orders.append(order)

    def update_status(self, order_id, status):
        for order in self.orders:
            if order["order_id"] == order_id:
                print(f"Updating order {order_id} status to {status}")
                order["status"] = status
                return


class InMemoryOutboxRepository:
    def __init__(self, name="outbox"):
        self.name = name
        self.messages = []

    def save(self, message):
        print(f"Saving {self.name} outbox message to DB", message)
        self.messages.append(message)

    def get_new_messages(self):
        return [message for message in self.messages if message["status"] == "NEW"]

    def mark_as_published(self, message):
        print("Mark as published")
        message["status"] = "PUBLISHED"


def publish_all_pending_events(*publishers):
    while True:
        published_count = 0
        for publisher in publishers:
            published_count += publisher.publish_pending_events()
        if published_count == 0:
            return


def create_example_runtime():
    bus = EventBus()
    order_repository = InMemoryOrderRepository()
    order_outbox_repository = InMemoryOutboxRepository(name="orders")
    loyalty_outbox_repository = InMemoryOutboxRepository(name="loyalty")

    bus.subscribe(
        "OrderCreated",
        partial(register_loyalty_points, outbox_repository=loyalty_outbox_repository),
    )
    bus.subscribe(
        "LoyaltyPointsAdded",
        partial(
            mark_order_as_processed,
            order_repository=order_repository,
            outbox_repository=order_outbox_repository,
        ),
    )
    bus.subscribe(
        "LoyaltyPointsSaveFailed",
        partial(retract_order, order_repository=order_repository),
    )
    bus.subscribe("OrderProcessed", send_order_confirmation)

    return {
        "order_repository": order_repository,
        "order_outbox_repository": order_outbox_repository,
        "loyalty_outbox_repository": loyalty_outbox_repository,
        "orders": OrderService(order_repository, order_outbox_repository),
        "order_outbox_publisher": OutboxPublisher(order_outbox_repository, bus),
        "loyalty_outbox_publisher": OutboxPublisher(loyalty_outbox_repository, bus),
    }


def main():
    runtime = create_example_runtime()
    order = runtime["orders"].create_order(1, "Marcin", "Laptop")
    publish_all_pending_events(
        runtime["order_outbox_publisher"],
        runtime["loyalty_outbox_publisher"],
    )

    print("Order : ", order)


if __name__ == "__main__":
    main()

