from Heksagonal.app.application.user_for_order_dto import UserForOrderDto
from Heksagonal.app.ports.user_query_port import UserQueryPort

class HttpUserAdapter(UserQueryPort):
    def get_user_for_order(self, user_id: int) -> UserForOrderDto:
        print("GET http://users-service/users/{user_id}")
        return UserForOrderDto(
            user_id=user_id,
            user_name="Marcin"
        )