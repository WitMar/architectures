class OrderService:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def create_order(self, user_id: int, user_name: str, product: str):
        order = {
            "user_id": user_id,
            "user_name": user_name,
            "product": product,
        }

        self.event_bus.publish("OrderCreated", order)
        return order

