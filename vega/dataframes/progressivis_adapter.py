from .source_adapter import SourceAdapter


class ProgressivisAdapter(SourceAdapter):
    """
    Actually this adapter requires a dict of ndarrays
    """

    def __init__(self, source, *args, **kw):
        from progressivis.table import BaseTable
        assert source is None or isinstance(
            source, BaseTable
        )
        super().__init__(source, *args, **kw)

    @property
    def columns(self):
        return self._columns or self._source.columns

    def to_array(self, col):
        return self._source[col].values

    def equals(self, other):
        from progressivis.table import BaseTable
        if isinstance(other, SourceAdapter):
            other = other._source
        assert isinstance(other, BaseTable)
        return self._source.equals(other)
