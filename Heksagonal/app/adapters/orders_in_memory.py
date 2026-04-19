from Heksagonal.app.ports.order_repository_port import OrderRepositoryPort


class InMemoryOrderRepositoryAdapter(OrderRepositoryPort):
    def __init__(self):
        self.saved_orders = []

    def save(self, order):
        self.saved_orders.append(order)
        print("Saving order:", order.user_id, order.product)

