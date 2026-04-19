class OrderRepository:
    def save(self, order):
        print("Saving order:", order.user_id, order.product)

