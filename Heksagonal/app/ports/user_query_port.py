from abc import ABC, abstractmethod
from Heksagonal.app.application.user_for_order_dto import UserForOrderDto

class UserQueryPort(ABC):
    @abstractmethod
    def get_user_for_order(self, user_id: int) -> UserForOrderDto:
        pass

