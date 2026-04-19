from ..domain.order import Order


class CreateOrderUseCase:
    def __init__(self, user_query_port, order_repository_port):
        self.user_query_port = user_query_port
        self.order_repository_port = order_repository_port

    def execute(self, user_id: int, product: str) -> Order:
        user = self.user_query_port.get_user_for_order(user_id)
        order = Order(user["user_id"], user["user_name"], product)
        self.order_repository_port.save(order)
        return order

