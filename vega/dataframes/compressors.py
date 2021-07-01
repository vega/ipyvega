from abc import ABCMeta, abstractmethod
import zlib
import lz4.frame


class BaseCompressor(metaclass=ABCMeta):
    def __init__(self, level=None):
        self._level = level

    @property
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def compress(self, data):
        ...


class ZLibCompressor(BaseCompressor):
    name = "zlib"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def compress(self, data):
        return zlib.compress(data, level=self._level)


class LZ4Compressor(BaseCompressor):
    name = "lz4"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def compress(self, data):
        return lz4.frame.compress(data, compression_level=self._level)

DEFAULT_COMPRESSORS = {'zlib': ZLibCompressor(level=-1), 'lz4': LZ4Compressor(level=0)}
