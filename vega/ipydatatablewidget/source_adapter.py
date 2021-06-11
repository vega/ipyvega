from abc import ABCMeta, abstractmethod, abstractproperty

class SourceAdapter(metaclass=ABCMeta):
    def __init__(self, source):
        self._source = source

    @abstractproperty
    def columns(self):
        ...

    @abstractmethod
    def to_array(self, col):
        ...
