import abc


class CacheEngine(abc.ABC):
    @abc.abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def set(self, *args, **kwargs):
        pass
