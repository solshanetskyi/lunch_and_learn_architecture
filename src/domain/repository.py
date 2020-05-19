import abc

from src.domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, profile: model.InvoiceProfile):
        pass

    @abc.abstractmethod
    def get(self, profile_id) -> model.InvoiceProfile:
        pass
