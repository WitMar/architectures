from Monolit.app.contracts.user_for_order_dto import UserForOrderDto
from .model import Order

class OrderService:
    def create_order(self, user: UserForOrderDto, product: str) -> Order:
        return Order(user.user_id, user.user_name, product)
