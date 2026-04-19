from LayeredArchitecture.app.application.create_order import create_order


if __name__ == "__main__":
    order = create_order(1, "Marcin", "Laptop")
    print(order.user_name, order.product)
    #order2 = create_order(1, "Marcin", None)
    #print(order2.user_name, order2.product)


