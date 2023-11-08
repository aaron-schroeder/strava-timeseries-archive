import abc


class AbstractActivityDataTranslator(abc.ABC):
    @abc.abstractmethod
    def to_activity_data(self, *args, **kwargs):
        raise NotImplementedError
