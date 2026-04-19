class SqlOrderRepositoryAdapter:
    def save(self, order):
        print(
            "INSERT INTO orders (user_id, user_name, product)",
            f"VALUES ({order.user_id}, '{order.user_name}', '{order.product}')"
        )