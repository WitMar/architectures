class OrderService:
    def __init__(self, order_repository, outbox_repository):
        self.order_repository = order_repository
        self.outbox_repository = outbox_repository

    def create_order(self, user_id: int, user_name: str, product: str):
        order = {
            "order_id": 101,
            "user_id": user_id,
            "user_name": user_name,
            "product": product,
            "status": "PENDING_LOYALTY",
        }

        self.order_repository.save(order)
        self.outbox_repository.save(
            {
                "event_name": "OrderCreated",
                "payload": {
                    "order_id": order["order_id"],
                    "user_id": user_id,
                    "user_name": user_name,
                    "product": product,
                    "points_to_add": 10,
                },
                "status": "NEW",
            }
        )

        return order