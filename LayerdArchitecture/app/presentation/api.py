from LayerdArchitecture.app.application.create_order import create_order


if __name__ == "__main__":
    order = create_order(1, "Marcin", "Laptop")
    print(order.user_name, order.product)

