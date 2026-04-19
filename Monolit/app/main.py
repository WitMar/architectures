from users.service import UserService
from orders.service import OrderService

users = UserService()
orders = OrderService()

user_dto = users.get_user_for_order(1)
order = orders.create_order(user_dto, "Laptop")

print(f"Order: user={order.user_name} (id={order.user_id}), product={order.product}")
