from Heksagonal.app.adapters.order_sql import SqlOrderRepositoryAdapter
from Heksagonal.app.adapters.users_http import HttpUserAdapter
from Heksagonal.app.application.create_order import CreateOrderUseCase

if __name__ == "__main__":
    user_adapter = HttpUserAdapter()
    order_adapter = SqlOrderRepositoryAdapter()

    use_case = CreateOrderUseCase(user_adapter, order_adapter)
    order = use_case.execute(1, "Laptop")

    print(order.user_name, order.product)

