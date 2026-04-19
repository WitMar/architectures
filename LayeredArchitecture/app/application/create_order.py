from ..domain.order import Order


def create_order(user_id: int, user_name: str, product: str) -> Order:
    return Order(user_id, user_name, product)

