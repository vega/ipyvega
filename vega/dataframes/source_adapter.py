from abc import ABCMeta, abstractmethod, abstractproperty

class SourceAdapter(metaclass=ABCMeta):
    def __init__(self, source, columns=None, compression=None):
        self._source = source
        self._columns = None
        self._compression = compression

    @abstractproperty
    def columns(self):
        ...

    @abstractmethod
    def to_array(self, col):
        ...

    @abstractmethod
    def equals(self, other):
        ...
"""
    @classmethod
    @abstractmethod
    def create(cls, data):
        ...
"""
