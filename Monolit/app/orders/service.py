from .model import Order


class OrderService:
    def create_order(self, user_id: int, product: str) -> Order:
        return Order(user_id, product)

