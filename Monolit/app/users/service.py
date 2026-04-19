from Monolit.app.contracts.user_for_order_dto import UserForOrderDto
from .model import User

class UserService:
    def get_user_for_order(self, user_id: int) -> UserForOrderDto:
        #Normalnie w tym miejscu byłoby pobranie danych z bazy i złożenie obiektu User, ale dla uproszczenia:
        user = User(user_id, "Marcin", "marcin@example.com", ["customer"])
        return UserForOrderDto(
            user_id=user.user_id,
            user_name=user.name,
            user_email=user.email,
        )
