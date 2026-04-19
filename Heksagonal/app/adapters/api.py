from Heksagonal.app.application.create_order import CreateOrderUseCase
from Heksagonal.app.adapters.orders_in_memory import InMemoryOrderRepositoryAdapter
from Heksagonal.app.adapters.users_in_memory import InMemoryUserAdapter


if __name__ == "__main__":
    user_adapter = InMemoryUserAdapter()
    order_adapter = InMemoryOrderRepositoryAdapter()

    use_case = CreateOrderUseCase(user_adapter, order_adapter)
    order = use_case.execute(1, "Laptop")

    print(order.user_name, order.product)

