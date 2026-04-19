class FileOrderRepositoryAdapter:
    def save(self, order):
        with open("orders.txt", "a", encoding="utf-8") as file:
            file.write(f"{order.user_id};{order.user_name};{order.product}\n")