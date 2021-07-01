import numpy as np
from .source_adapter import SourceAdapter


class NumpyAdapter(SourceAdapter):
    """
    Actually this adapter requires a dict of ndarrays
    """

    def __init__(self, source, *args, **kw):
        assert source is None or isinstance(
            source, dict
        )  # TODO: check values are ndarrays
        super().__init__(source, *args, **kw)
        if not self._touch_mode:
            self._source = {k:v.copy() for (k, v) in self._source.items()}

    @property
    def columns(self):
        return self._columns or self._source.keys()

    def to_array(self, col):
        return self._source[col]

    def equals(self, other):
        if isinstance(other, SourceAdapter):
            other = other._source
        for k, v in self._source.items():
            if not np.array_equal(v, other[k]):
                return False
        return True
