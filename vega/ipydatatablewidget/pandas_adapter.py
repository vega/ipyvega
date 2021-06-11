import pandas as pd
form .source_adapter import SourceAdapter


class PandasAdapter(SourceAdapter):
    def __init__(self, source):
        assert isinstance(source, pd.DataFrame)
        super().__init__(source)

    @property
    def columns(self):
        return self._source.columns

    @abstractmethod
    def to_array(self, col):
        self._source[col].to_numpy()
