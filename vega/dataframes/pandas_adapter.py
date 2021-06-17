import pandas as pd
from .source_adapter import SourceAdapter


class PandasAdapter(SourceAdapter):
    def __init__(self, source, *args, **kw):
        assert source is None or isinstance(source, pd.DataFrame)
        super().__init__(source, *args, **kw)

    @property
    def columns(self):
        return self._columns or self._source.columns

    def to_array(self, col):
        return self._source[col].to_numpy()

    def equals(self, other):
        if isinstance(other, SourceAdapter):
            other = other._source
        assert isinstance(other, pd.DataFrame)
        return self._source.equals(other)
"""
    @classmethod
    def create(cls, data):
        df = pd.DataFrame(data)
        return PandasAdapter(df)
"""
