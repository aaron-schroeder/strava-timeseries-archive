import abc

from dddhns.domain.model import ActivityData


class AbstractExportRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, activity_data: ActivityData) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def exists(self, key) -> bool:
        raise NotImplementedError

