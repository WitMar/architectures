from users.service import UserService
from orders.service import OrderService

users = UserService()
orders = OrderService()

user = users.get_user(1)
order = orders.create_order(user.user_id, "Laptop")

print(user.user_id,user.name)
print(order.user_id, order.product)

