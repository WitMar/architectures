from EventBased.app.events.bus import EventBus
from EventBased.app.notifications.handler import send_order_confirmation
from EventBased.app.orders.service import OrderService


def main():
    bus = EventBus()
    bus.subscribe("OrderCreated", send_order_confirmation)

    orders = OrderService(bus)
    order = orders.create_order(1, "Marcin", "Laptop")

    print(order)


if __name__ == "__main__":
    main()

