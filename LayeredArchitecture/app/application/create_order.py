from ..domain.order import Order
from ..infrastructure.order_repository import OrderRepository

def create_order(user_id: int, user_name: str, product: str) -> Order:
    order = Order(user_id, user_name, product)
    repository = OrderRepository()
    repository.save(order)
    return order

