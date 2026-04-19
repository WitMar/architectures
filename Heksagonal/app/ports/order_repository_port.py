from abc import ABC, abstractmethod


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order):
        raise NotImplementedError

