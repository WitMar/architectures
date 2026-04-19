from abc import ABC, abstractmethod


class UserQueryPort(ABC):
    @abstractmethod
    def get_user_for_order(self, user_id: int):
        raise NotImplementedError

