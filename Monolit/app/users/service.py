from .model import User


class UserService:
    def get_user(self, user_id: int) -> User:
        return User(user_id, "Marcin")

